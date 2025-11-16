# cli.py
#!/usr/bin/env python3
"""
Interface de linha de comando para o simulador de transferência de calor.
"""

import click
import numpy as np
from pathlib import Path
from corpo_termico import CorpoTermico
from simulador import SimuladorTermico
from visualizacao import plotar_resultados, plotar_energia
from banco_materiais import BancoMateriais


def parse_floats(ctx, param, value):
    """Parse string de números separados por vírgula."""
    if not value:
        return None
    try:
        return np.array([float(x.strip()) for x in value.split(",") if x.strip()])
    except ValueError:
        raise click.BadParameter(f"Valores inválidos em '{value}'. Use formato: 1.0,2.0,3.0")


def parse_matrix(ctx, param, value):
    """Parse string de matriz separada por ';' para linhas e ',' para colunas."""
    if not value:
        return None
    try:
        rows = [row.strip() for row in value.split(";") if row.strip()]
        matrix = []
        for row in rows:
            matrix.append([float(x.strip()) for x in row.split(",") if x.strip()])
        return np.array(matrix)
    except ValueError:
        raise click.BadParameter(f"Matriz inválida: '{value}'. Use formato: '1,2;3,4'")


@click.group()
def cli():
    """Simulador de Transferência de Calor - SEFITEL Inatel"""
    pass


@cli.command()
@click.option("--t-init", callback=parse_floats, required=True,
              help="Temperaturas iniciais dos corpos (ex: '80,30,10')")
@click.option("--t-amb", type=float, default=25.0,
              help="Temperatura ambiente (°C)")
@click.option("--m", callback=parse_floats, required=True,
              help="Massas dos corpos em kg (ex: '2,1,0.5')")
@click.option("--c", callback=parse_floats, required=True,
              help="Calores específicos em J/(kg·K) (ex: '900,900,900')")
@click.option("--g", callback=parse_matrix,
              help="Matriz de condutâncias (ex: '0,5,0;5,0,3;0,3,0')")
@click.option("--g-env", callback=parse_floats,
              help="Condutâncias com ambiente (ex: '1,0.5,0.2')")
@click.option("--dt", type=float, default=1.0,
              help="Passo de tempo (s)")
@click.option("--t-max", type=float, default=600.0,
              help="Tempo total de simulação (s)")
@click.option("--output", type=click.Path(),
              help="Arquivo para salvar resultados")
@click.option("--no-plot", is_flag=True,
              help="Desabilita gráficos")
def multicorpo(t_init, t_amb, m, c, g, g_env, dt, t_max, output, no_plot):
    """Simula troca de calor entre múltiplos corpos acoplados."""
    
    # Validação de entradas
    num_corpos = len(t_init)
    if len(m) != num_corpos or len(c) != num_corpos:
        raise click.BadParameter("Número inconsistente de corpos nos parâmetros")
    
    if g is not None and g.shape != (num_corpos, num_corpos):
        raise click.BadParameter(f"Matriz G deve ser {num_corpos}x{num_corpos}")
    
    if g_env is not None and len(g_env) != num_corpos:
        raise click.BadParameter(f"G_env deve ter {num_corpos} elementos")
    
    # Criar corpos
    corpos = []
    for i in range(num_corpos):
        corpo = CorpoTermico(
            nome=f"Corpo_{i+1}",
            massa=m[i],
            calor_especifico=c[i],
            area_superficie=0.1,  # Valor padrão, pode ser parametrizado
            temperatura_inicial=t_init[i]
        )
        corpos.append(corpo)
    
    # Configurar simulador
    simulador = SimuladorTermico(delta_t=dt)
    for corpo in corpos:
        simulador.adicionar_corpo(corpo)
    
    simulador.configurar_ambiente(t_amb)
    
    # Configurar condutâncias se fornecidas
    if g is not None:
        simulador.definir_matriz_condutancia(g)
    
    if g_env is not None:
        simulador.definir_condutancia_ambiente(g_env)
    
    # Executar simulação
    click.echo(f"Executando simulação com {num_corpos} corpos...")
    resultados = simulador.simular_multiplos_corpos(tempo_total=t_max)
    
    # Exibir resultados
    click.echo("\n" + "="*50)
    click.echo("RESULTADOS FINAIS")
    click.echo("="*50)
    for i, corpo in enumerate(corpos):
        click.echo(f"Corpo {i+1}: {corpo.temperatura:.2f} °C")
    
    # Plotar resultados
    if not no_plot:
        plotar_resultados(resultados)
        plotar_energia(resultados, corpos)
    
    # Salvar resultados se especificado
    if output:
        salvar_resultados(resultados, output)
        click.echo(f"\nResultados salvos em {output}")


@cli.command()
@click.option("--material", type=str, required=True,
              help="Nome do material ou ID")
@click.option("--massa", type=float, required=True,
              help="Massa do corpo (kg)")
@click.option("--area", type=float, required=True,
              help="Área da superfície (m²)")
@click.option("--t-init", type=float, required=True,
              help="Temperatura inicial (°C)")
@click.option("--t-amb", type=float, default=25.0,
              help="Temperatura ambiente (°C)")
@click.option("--coef-conv", type=float, default=10.0,
              help="Coeficiente de convecção (W/m²·K)")
@click.option("--dt", type=float, default=1.0,
              help="Passo de tempo (s)")
@click.option("--t-max", type=float, default=600.0,
              help="Tempo total de simulação (s)")
def simples(material, massa, area, t_init, t_amb, coef_conv, dt, t_max):
    """Simulação simples de um corpo com ambiente."""
    
    banco = BancoMateriais()
    
    # Tentar encontrar material por ID ou nome
    try:
        material_id = int(material)
        material_obj = banco.obter_material(material_id)
    except ValueError:
        material_obj = banco.obter_material_por_nome(material)
    
    if not material_obj:
        raise click.BadParameter(f"Material '{material}' não encontrado")
    
    # Criar corpo e simulador
    corpo = CorpoTermico(
        nome=material_obj['nome'],
        massa=massa,
        calor_especifico=material_obj['calor_especifico'],
        area_superficie=area,
        temperatura_inicial=t_init
    )
    
    simulador = SimuladorTermico(delta_t=dt)
    simulador.adicionar_corpo(corpo)
    simulador.configurar_ambiente(t_amb, coef_conv)
    
    # Executar simulação
    resultados = simulador.simular(tempo_total=t_max, modo='ambiente')
    
    # Exibir resultados
    click.echo(f"\nMaterial: {material_obj['nome']}")
    click.echo(f"Temperatura final: {corpo.temperatura:.2f} °C")
    click.echo(f"Variação: {corpo.temperatura - t_init:+.2f} °C")
    
    plotar_resultados(resultados)


@cli.command()
def listar_materiais():
    """Lista todos os materiais disponíveis."""
    banco = BancoMateriais()
    banco.exibir_materiais()


@cli.command()
def listar_coeficientes():
    """Lista coeficientes de convecção disponíveis."""
    banco = BancoMateriais()
    banco.exibir_coeficientes()


def salvar_resultados(resultados, arquivo):
    """Salva resultados em arquivo CSV."""
    import csv
    with open(arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tempo(s)'] + [f'{res["nome"]}_T(°C)' for res in resultados])
        
        num_pontos = len(resultados[0]['tempo'])
        for i in range(num_pontos):
            linha = [resultados[0]['tempo'][i]]
            for res in resultados:
                linha.append(res['temperatura'][i])
            writer.writerow(linha)


if __name__ == "__main__":
    cli()