"""
Módulo com funções para calcular transferência de calor.
"""

def taxa_conveccao(h, area, T_corpo, T_ambiente):
    """
    Calcula a taxa de transferência de calor por convecção (Lei de Newton do Resfriamento).
    
    Q̇ = h·A·(T_corpo - T_ambiente)
    
    Args:
        h: Coeficiente de convecção (W/m²·K)
        area: Área da superfície (m²)
        T_corpo: Temperatura do corpo (°C)
        T_ambiente: Temperatura do ambiente (°C)
    
    Returns:
        Taxa de transferência de calor (W = J/s)
        Positivo: corpo perde calor
        Negativo: corpo ganha calor
    """
    return h * area * (T_corpo - T_ambiente)


def taxa_conducao(k, area, espessura, T1, T2):
    """
    Calcula a taxa de transferência de calor por condução (Lei de Fourier).
    
    Q̇ = k·A·(T1 - T2) / L
    
    Args:
        k: Condutividade térmica (W/m·K)
        area: Área da seção transversal (m²)
        espessura: Espessura/distância (m)
        T1: Temperatura da superfície 1 (°C)
        T2: Temperatura da superfície 2 (°C)
    
    Returns:
        Taxa de transferência de calor (W = J/s)
    """
    return k * area * (T1 - T2) / espessura


def calcular_delta_Q(taxa_transferencia, delta_t):
    """
    Calcula a quantidade de calor transferida em um intervalo de tempo.
    
    ΔQ = Q̇·Δt
    
    Args:
        taxa_transferencia: Taxa de transferência de calor (W)
        delta_t: Intervalo de tempo (s)
    
    Returns:
        Quantidade de calor transferida (J)
    """
    return taxa_transferencia * delta_t
