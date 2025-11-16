"""
Módulo para representar corpos térmicos e suas propriedades.
"""

class CorpoTermico:
    """
    Representa um corpo com propriedades térmicas.
    
    Parâmetros:
        nome: Nome do corpo
        massa: Massa do corpo (kg)
        calor_especifico: Calor específico do material (J/kg·K)
        area_superficie: Área da superfície exposta (m²)
        temperatura_inicial: Temperatura inicial (°C)
    """
    
    def __init__(self, nome, massa, calor_especifico, area_superficie, temperatura_inicial):
        self.nome = nome
        self.massa = massa  # kg
        self.calor_especifico = calor_especifico  # J/(kg·K)
        self.area_superficie = area_superficie  # m²
        self.temperatura = temperatura_inicial  # °C
        self.historico_temperatura = [temperatura_inicial]
        self.historico_tempo = [0]
        
    def capacidade_termica(self):
        """Retorna a capacidade térmica do corpo (C = m·c)"""
        return self.massa * self.calor_especifico
    
    def atualizar_temperatura(self, delta_Q, delta_t):
        """
        Atualiza a temperatura do corpo após receber/perder calor.
        
        Args:
            delta_Q: Quantidade de calor transferida (J) - positivo se recebe, negativo se perde
            delta_t: Intervalo de tempo (s)
        """
        # ΔT = ΔQ / (m·c)
        delta_T = delta_Q / self.capacidade_termica()
        self.temperatura += delta_T
        
    def registrar_estado(self, tempo):
        """Registra o estado atual no histórico"""
        self.historico_temperatura.append(self.temperatura)
        self.historico_tempo.append(tempo)
    
    def __str__(self):
        return (f"{self.nome}: T={self.temperatura:.2f}°C, "
                f"m={self.massa}kg, c={self.calor_especifico}J/(kg·K)")
