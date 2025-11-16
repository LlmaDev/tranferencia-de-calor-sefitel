"""
Módulo para visualização dos resultados da simulação.
"""

import matplotlib.pyplot as plt


def plotar_resultados(resultados, titulo="Simulação de Transferência de Calor"):
    """
    Plota os resultados da simulação térmica.
    
    Args:
        resultados: Lista de dicionários com 'nome', 'tempo' e 'temperatura'
        titulo: Título do gráfico
    """
    plt.figure(figsize=(10, 6))
    
    for resultado in resultados:
        plt.plot(
            resultado['tempo'],
            resultado['temperatura'],
            marker='o',
            markersize=3,
            label=resultado['nome'],
            linewidth=2
        )
    
    plt.xlabel('Tempo (s)', fontsize=12)
    plt.ylabel('Temperatura (°C)', fontsize=12)
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plotar_multiplos_graficos(lista_resultados, titulos):
    """
    Plota múltiplas simulações em subplots.
    
    Args:
        lista_resultados: Lista de resultados de diferentes simulações
        titulos: Lista de títulos para cada subplot
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
                markersize=3,
                label=resultado['nome'],
                linewidth=2
            )
        
        ax.set_xlabel('Tempo (s)', fontsize=11)
        ax.set_ylabel('Temperatura (°C)', fontsize=11)
        ax.set_title(titulo, fontsize=12, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
