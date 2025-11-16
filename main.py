"""
Simulador interativo de transferência de calor.
O usuário escolhe todos os parâmetros.
"""

from corpo_termico import CorpoTermico
from simulador import SimuladorTermico
from visualizacao import plotar_resultados
from banco_materiais import BancoMateriais


def ler_numero(mensagem, tipo=float, minimo=None, maximo=None):
    """
    Lê um número do usuário com validação.
    
    Args:
        mensagem: Mensagem a exibir
        tipo: Tipo do número (int ou float)
        minimo: Valor mínimo aceitável
        maximo: Valor máximo aceitável
        
    Returns:
        Número validado
    """
    while True:
        try:
            valor = tipo(input(mensagem))
            
            if minimo is not None and valor < minimo:
                print(f"ERRO: Valor deve ser maior ou igual a {minimo}")
                continue
            
            if maximo is not None and valor > maximo:
                print(f"ERRO: Valor deve ser menor ou igual a {maximo}")
                continue
            
            return valor
        except ValueError:
            print(f"ERRO: Por favor, digite um numero valido")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SIMULADOR DE TRANSFERENCIA DE CALOR")
    print("=" * 70)
    print("\nBem-vindo! Vamos configurar sua simulacao.\n")
    
    # Inicializar banco de materiais
    banco = BancoMateriais()
    
    # PASSO 1: Escolher material
    print("=" * 70)
    print("PASSO 1: Escolha o material do corpo")
    print("=" * 70)
    banco.exibir_materiais()
    
    materiais = banco.listar_materiais()
    ids_validos = [mat['id'] for mat in materiais]
    
    while True:
        material_id = ler_numero(
            "\n> Digite o numero do material: ",
            tipo=int,
            minimo=1
        )
        
        if material_id in ids_validos:
            material = banco.obter_material(material_id)
            break
        else:
            print(f"ERRO: Material {material_id} nao existe. Escolha entre {ids_validos}")
    
    print(f"\nMaterial selecionado: {material['nome']}")
    
    # PASSO 2: Configurar corpo
    print("\n" + "=" * 70)
    print(f"PASSO 2: Configure as propriedades do corpo")
    print("=" * 70)
    print(f"\nMaterial: {material['nome']}")
    print(f"Calor especifico: {material['calor_especifico']} {material['unidade']}")
    
    massa = ler_numero(
        "Massa do objeto (kg): ",
        tipo=float,
        minimo=0.001
    )
    
    area = ler_numero(
        "Area da superficie exposta (m²): ",
        tipo=float,
        minimo=0.0001
    )
    
    temp_inicial = ler_numero(
        "Temperatura inicial (°C): ",
        tipo=float,
        minimo=-273
    )
    
    corpo = CorpoTermico(
        nome=material['nome'],
        massa=massa,
        calor_especifico=material['calor_especifico'],
        area_superficie=area,
        temperatura_inicial=temp_inicial
    )
    
    print(f"\nCorpo configurado: {corpo.nome}")
    
    # PASSO 3: Configurar ambiente
    print("\n" + "=" * 70)
    print("PASSO 3: Configure o ambiente")
    print("=" * 70)
    
    temp_ambiente = ler_numero(
        "\nTemperatura do ambiente (°C): ",
        tipo=float,
        minimo=-273
    )
    
    print("\nEscolha o tipo de conveccao:")
    banco.exibir_coeficientes()
    
    coefs = banco.listar_coeficientes_conveccao()
    lista_coefs = list(coefs.items())
    
    print("\nOpcoes:")
    for i, (chave, dados) in enumerate(lista_coefs, 1):
        print(f"  [{i}] {dados['descricao']} - {dados['valor']} W/m²·K")
    print(f"  [0] Inserir valor personalizado")
    
    escolha = ler_numero(
        "\n> Escolha uma opcao: ",
        tipo=int,
        minimo=0,
        maximo=len(lista_coefs)
    )
    
    if escolha == 0:
        coef_conveccao = ler_numero(
            "Digite o coeficiente de conveccao (W/m²·K): ",
            tipo=float,
            minimo=0
        )
    else:
        chave, dados = lista_coefs[escolha - 1]
        coef_conveccao = dados['valor']
        print(f"Selecionado: {dados['descricao']}")
    
    print(f"\nAmbiente configurado: {temp_ambiente}°C")
    
    # PASSO 4: Configurar simulação
    print("\n" + "=" * 70)
    print("PASSO 4: Configure os parametros de simulacao")
    print("=" * 70)
    
    print("\nPor quanto tempo deseja simular?")
    tempo_minutos = ler_numero(
        "Tempo total (minutos): ",
        tipo=float,
        minimo=0.1
    )
    tempo_total = tempo_minutos * 60  # converter para segundos
    
    print("\nQual a precisao da simulacao?")
    print("  - Valores menores = maior precisao, mas mais lento")
    print("  - Valores tipicos: 1-10 segundos")
    
    delta_t = ler_numero(
        "Intervalo de calculo (segundos): ",
        tipo=float,
        minimo=0.1,
        maximo=60
    )
    
    print(f"\nSimulacao configurada: {tempo_total/60:.1f} minutos")
    
    # Exibir resumo
    print("\n" + "=" * 70)
    print("RESUMO DA SIMULACAO")
    print("=" * 70)
    
    print(f"\nCORPO:")
    print(f"  - Nome: {corpo.nome}")
    print(f"  - Massa: {corpo.massa} kg")
    print(f"  - Calor especifico: {corpo.calor_especifico} J/(kg·K)")
    print(f"  - Area: {corpo.area_superficie} m²")
    print(f"  - Temperatura inicial: {corpo.temperatura}°C")
    
    print(f"\nAMBIENTE:")
    print(f"  - Temperatura: {temp_ambiente}°C")
    print(f"  - Coeficiente de conveccao: {coef_conveccao} W/m²·K")
    
    print(f"\nSIMULACAO:")
    print(f"  - Tempo total: {tempo_total/60:.1f} minutos ({tempo_total:.0f}s)")
    print(f"  - Intervalo de calculo: {delta_t}s")
    print(f"  - Numero de passos: {int(tempo_total/delta_t)}")
    
    print("\n" + "=" * 70)
    
    # Confirmar execução
    input("\nPressione ENTER para iniciar a simulacao...")
    
    # Executar simulação
    print("\nExecutando simulacao...")
    print("=" * 70)
    
    simulador = SimuladorTermico(delta_t=delta_t)
    simulador.adicionar_corpo(corpo)
    simulador.configurar_ambiente(temp_ambiente, coef_conveccao)
    
    resultados = simulador.simular(tempo_total=tempo_total, modo='ambiente')
    
    # Exibir resultados
    print("\n" + "=" * 70)
    print("SIMULACAO CONCLUIDA!")
    print("=" * 70)
    
    print(f"\nRESULTADOS:")
    print(f"  - Temperatura inicial: {resultados[0]['temperatura'][0]:.2f}°C")
    print(f"  - Temperatura final: {corpo.temperatura:.2f}°C")
    print(f"  - Variacao total: {corpo.temperatura - resultados[0]['temperatura'][0]:+.2f}°C")
    
    diferenca_ambiente = abs(corpo.temperatura - temp_ambiente)
    print(f"  - Diferenca com ambiente: {diferenca_ambiente:.2f}°C")
    
    if diferenca_ambiente < 1:
        print("\nEquilibrio termico atingido!")
    elif diferenca_ambiente < 5:
        print("\nProximo do equilibrio termico")
    else:
        print(f"\nAinda ha {diferenca_ambiente:.1f}°C de diferenca com o ambiente")
    
    print("\n" + "=" * 70)
    print("Gerando grafico...")
    print("=" * 70)
    
    plotar_resultados(resultados, f"Simulacao: {corpo.nome}")
    
    print("\nSimulacao finalizada com sucesso!")
