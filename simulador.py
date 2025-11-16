# simulador.py (versão melhorada)
"""
Simulador de transferência de calor entre corpos.
"""

import numpy as np
from corpo_termico import CorpoTermico
from transferencia_calor import taxa_conveccao, taxa_conducao, calcular_delta_Q


class SimuladorTermico:
    """
    Simula a transferência de calor entre corpos e com o ambiente.
    """
    
    def __init__(self, delta_t=1.0):
        """
        Args:
            delta_t: Passo de tempo da simulação (s)
        """
        self.corpos = []
        self.temperatura_ambiente = 25.0  # °C
        self.coef_conveccao = 10.0  # W/m²·K
        self.delta_t = delta_t
        self.tempo_atual = 0.0
        
        # Para simulação com múltiplos corpos
        self.matriz_condutancia = None  # Matriz de condutâncias entre corpos
        self.condutancia_ambiente = None  # Vetor de condutâncias com ambiente
        
    def adicionar_corpo(self, corpo):
        """Adiciona um corpo à simulação"""
        self.corpos.append(corpo)
        
    def configurar_ambiente(self, temperatura, coef_conveccao=None):
        """
        Configura as propriedades do ambiente.
        """
        self.temperatura_ambiente = temperatura
        if coef_conveccao is not None:
            self.coef_conveccao = coef_conveccao
            
    def definir_matriz_condutancia(self, matriz):
        """
        Define a matriz de condutâncias entre corpos.
        
        Args:
            matriz: Matriz numpy onde G[i,j] é a condutância entre corpo i e j
        """
        if len(self.corpos) != matriz.shape[0]:
            raise ValueError("Dimensão da matriz não corresponde ao número de corpos")
        self.matriz_condutancia = matriz
        
    def definir_condutancia_ambiente(self, condutancias):
        """
        Define as condutâncias individuais com o ambiente.
        
        Args:
            condutancias: Lista/array de condutâncias para cada corpo
        """
        if len(self.corpos) != len(condutancias):
            raise ValueError("Número de condutâncias não corresponde ao número de corpos")
        self.condutancia_ambiente = condutancias
        
    def simular_multiplos_corpos(self, tempo_total):
        """
        Simula a troca de calor entre múltiplos corpos acoplados.
        
        Args:
            tempo_total: Tempo total de simulação (s)
            
        Returns:
            Resultados da simulação
        """
        num_corpos = len(self.corpos)
        num_passos = int(tempo_total / self.delta_t)
        
        # Inicializar arrays para cálculo vetorizado
        temperaturas = np.array([corpo.temperatura for corpo in self.corpos])
        capacidades = np.array([corpo.capacidade_termica() for corpo in self.corpos])
        areas = np.array([corpo.area_superficie for corpo in self.corpos])
        
        # Usar condutâncias individuais ou padrão
        if self.condutancia_ambiente is not None:
            coefs_conv = self.condutancia_ambiente
        else:
            coefs_conv = np.full(num_corpos, self.coef_conveccao)
        
        for _ in range(num_passos):
            # Calcular trocas de calor
            delta_Q = np.zeros(num_corpos)
            
            # Convecção com ambiente
            for i in range(num_corpos):
                taxa = taxa_conveccao(
                    coefs_conv[i],
                    areas[i],
                    temperaturas[i],
                    self.temperatura_ambiente
                )
                delta_Q[i] += -calcular_delta_Q(taxa, self.delta_t)
            
            # Condução entre corpos (se matriz definida)
            if self.matriz_condutancia is not None:
                for i in range(num_corpos):
                    for j in range(i + 1, num_corpos):
                        if self.matriz_condutancia[i, j] > 0:
                            # Simular condução entre corpo i e j
                            taxa = taxa_conducao(
                                self.matriz_condutancia[i, j],
                                0.1,  # Área de contato padrão - poderia ser parametrizada
                                0.01, # Espessura padrão - poderia ser parametrizada
                                temperaturas[i],
                                temperaturas[j]
                            )
                            delta_Q_cond = calcular_delta_Q(taxa, self.delta_t)
                            delta_Q[i] -= delta_Q_cond
                            delta_Q[j] += delta_Q_cond
            
            # Atualizar temperaturas
            delta_T = delta_Q / capacidades
            temperaturas += delta_T
            
            # Atualizar objetos corpo e registrar estado
            self.tempo_atual += self.delta_t
            for i, corpo in enumerate(self.corpos):
                corpo.temperatura = temperaturas[i]
                corpo.registrar_estado(self.tempo_atual)
                
        return self.obter_resultados()
    
    # Manter métodos originais para compatibilidade
    def simular_conveccao_ambiente(self, corpo):
        """Mantido para compatibilidade"""
        taxa = taxa_conveccao(
            self.coef_conveccao,
            corpo.area_superficie,
            corpo.temperatura,
            self.temperatura_ambiente
        )
        delta_Q = -calcular_delta_Q(taxa, self.delta_t)
        return delta_Q
    
    def executar_passo(self, modo='ambiente', **kwargs):
        """Mantido para compatibilidade"""
        if modo == 'ambiente':
            for corpo in self.corpos:
                delta_Q = self.simular_conveccao_ambiente(corpo)
                corpo.atualizar_temperatura(delta_Q, self.delta_t)
                
        elif modo == 'conducao':
            corpo1 = kwargs.get('corpo1')
            corpo2 = kwargs.get('corpo2')
            k = kwargs.get('k', 50.0)
            area_contato = kwargs.get('area_contato', 0.01)
            espessura = kwargs.get('espessura', 0.001)
            
            delta_Q1, delta_Q2 = self.simular_conducao_entre_corpos(
                corpo1, corpo2, k, area_contato, espessura
            )
            corpo1.atualizar_temperatura(delta_Q1, self.delta_t)
            corpo2.atualizar_temperatura(delta_Q2, self.delta_t)
        
        self.tempo_atual += self.delta_t
        for corpo in self.corpos:
            corpo.registrar_estado(self.tempo_atual)
    
    def simular(self, tempo_total, modo='ambiente', **kwargs):
        """Mantido para compatibilidade"""
        if len(self.corpos) > 1 and self.matriz_condutancia is not None:
            return self.simular_multiplos_corpos(tempo_total)
        else:
            num_passos = int(tempo_total / self.delta_t)
            for _ in range(num_passos):
                self.executar_passo(modo, **kwargs)
            return self.obter_resultados()
    
    def obter_resultados(self):
        """Retorna os resultados da simulação."""
        resultados = []
        for corpo in self.corpos:
            resultados.append({
                'nome': corpo.nome,
                'tempo': corpo.historico_tempo.copy(),
                'temperatura': corpo.historico_temperatura.copy()
            })
        return resultados
    
    def calcular_energia_total(self):
        """Calcula a energia térmica total do sistema."""
        energia_total = 0.0
        for corpo in self.corpos:
            # E = m * c * T (considerando T em Kelvin relativo)
            energia_total += corpo.massa * corpo.calor_especifico * (corpo.temperatura + 273.15)
        return energia_total