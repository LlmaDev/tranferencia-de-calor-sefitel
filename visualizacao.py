# visualizacao.py (versão melhorada)
"""
Módulo para visualização dos resultados da simulação.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime


def plotar_resultados(resultados, titulo="Simulação de Transferência de Calor", salvar_arquivo=True, nome_arquivo=None):
    """
    Plota os resultados da simulação térmica e salva em pasta imgs.
    
    Args:
        resultados: Lista de dicionários com dados da simulação
        titulo: Título do gráfico
        salvar_arquivo: Se True, salva o gráfico em arquivo
        nome_arquivo: Nome personalizado para o arquivo (opcional)
    """
    # Criar pasta imgs se não existir
    if salvar_arquivo:
        pasta_imgs = "imgs"
        if not os.path.exists(pasta_imgs):
            os.makedirs(pasta_imgs)
    
    plt.figure(figsize=(12, 8))
    
    # Subplot para temperaturas
    plt.subplot(2, 1, 1)
    for resultado in resultados:
        plt.plot(
            resultado['tempo'],
            resultado['temperatura'],
            marker='o',
            markersize=2,
            label=resultado['nome'],
            linewidth=1.5
        )
    
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    plt.title(titulo, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot para taxas de variação
    plt.subplot(2, 1, 2)
    for resultado in resultados:
        tempo = np.array(resultado['tempo'])
        temperatura = np.array(resultado['temperatura'])
        dT_dt = np.gradient(temperatura, tempo)
        plt.plot(tempo, dT_dt, '--', label=f'dT/dt {resultado["nome"]}', alpha=0.7)
    
    plt.xlabel('Tempo (s)')
    plt.ylabel('Taxa de Variação (°C/s)')
    plt.title('Taxa de Variação da Temperatura')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Salvar arquivo se solicitado
    if salvar_arquivo:
        if nome_arquivo is None:
            # Gerar nome automático com timestamp e detalhes
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            corpos = "_".join([res['nome'].replace(" ", "_") for res in resultados])
            nome_arquivo = f"simulacao_{corpos}_{timestamp}.png"
        
        caminho_arquivo = os.path.join(pasta_imgs, nome_arquivo)
        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {caminho_arquivo}")
    
    plt.show()


def plotar_energia(resultados, corpos):
    """
    Plota a energia térmica total do sistema.
    
    Args:
        resultados: Lista de resultados da simulação
        corpos: Lista de objetos CorpoTermico
    """
    if len(resultados) == 0:
        return
        
    tempo = resultados[0]['tempo']
    energia_total = np.zeros(len(tempo))
    
    # Calcular energia para cada passo de tempo
    for i, corpo in enumerate(corpos):
        C = corpo.massa * corpo.calor_especifico  # Capacidade térmica
        # Energia relativa à 0°C: E = C * T
        energia_corpo = C * np.array(resultados[i]['temperatura'])
        energia_total += energia_corpo
    
    plt.figure(figsize=(10, 6))
    plt.plot(tempo, energia_total, 'r-', linewidth=2, label='Energia Total')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Energia Térmica (J)')
    plt.title('Energia Térmica Total do Sistema', fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plotar_multiplos_graficos(lista_resultados, titulos):
    """
    Plota múltiplas simulações em subplots.
    """
    num_plots = len(lista_resultados)
    fig, axes = plt.subplots(num_plots, 1, figsize=(10, 4*num_plots))
    
    if num_plots == 1:
        axes = [axes]
    
    for ax, resultados, titulo in zip(axes, lista_resultados, titulos):
        for resultado in resultados:
            ax.plot(
                resultado['tempo'],
                resultado['temperatura'],
                marker='o',
                markersize=2,
                label=resultado['nome'],
                linewidth=1.5
            )
        
        ax.set_xlabel('Tempo (s)')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title(titulo, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def salvar_grafico(resultados, filename, formato='png'):
    """
    Salva o gráfico em arquivo.
    
    Args:
        resultados: Resultados da simulação
        filename: Nome do arquivo
        formato: Formato do arquivo ('png', 'pdf', 'svg')
    """
    plt.figure(figsize=(10, 6))
    
    for resultado in resultados:
        plt.plot(
            resultado['tempo'],
            resultado['temperatura'],
            marker='o',
            markersize=2,
            label=resultado['nome'],
            linewidth=1.5
        )
    
    plt.xlabel('Tempo (s)')
    plt.ylabel('Temperatura (°C)')
    plt.title('Simulação de Transferência de Calor', fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(f"{filename}.{formato}", dpi=300, bbox_inches='tight')
    plt.close()