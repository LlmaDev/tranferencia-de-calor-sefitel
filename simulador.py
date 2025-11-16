"""
Simulador de transferência de calor entre corpos.
"""

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
        self.coef_conveccao = 10.0  # W/m²·K (típico para convecção natural com ar)
        self.delta_t = delta_t
        self.tempo_atual = 0.0
        
    def adicionar_corpo(self, corpo):
        """Adiciona um corpo à simulação"""
        self.corpos.append(corpo)
        
    def configurar_ambiente(self, temperatura, coef_conveccao=None):
        """
        Configura as propriedades do ambiente.
        
        Args:
            temperatura: Temperatura do ambiente (°C)
            coef_conveccao: Coeficiente de convecção com o ar (W/m²·K)
        """
        self.temperatura_ambiente = temperatura
        if coef_conveccao is not None:
            self.coef_conveccao = coef_conveccao
            
    def simular_conveccao_ambiente(self, corpo):
        """
        Simula a troca de calor por convecção entre um corpo e o ambiente.
        
        Returns:
            Quantidade de calor perdida pelo corpo (J)
        """
        taxa = taxa_conveccao(
            self.coef_conveccao,
            corpo.area_superficie,
            corpo.temperatura,
            self.temperatura_ambiente
        )
        # Taxa positiva = corpo perde calor
        delta_Q = -calcular_delta_Q(taxa, self.delta_t)
        return delta_Q
    
    def simular_conducao_entre_corpos(self, corpo1, corpo2, k, area_contato, espessura):
        """
        Simula a troca de calor por condução entre dois corpos.
        
        Args:
            corpo1, corpo2: Corpos em contato
            k: Condutividade térmica do material entre eles (W/m·K)
            area_contato: Área de contato (m²)
            espessura: Espessura da interface (m)
        
        Returns:
            Tupla (delta_Q1, delta_Q2) com a quantidade de calor para cada corpo
        """
        taxa = taxa_conducao(k, area_contato, espessura, corpo1.temperatura, corpo2.temperatura)
        delta_Q = calcular_delta_Q(taxa, self.delta_t)
        
        # Corpo 1 perde calor, corpo 2 ganha
        return -delta_Q, delta_Q
    
    def executar_passo(self, modo='ambiente', **kwargs):
        """
        Executa um passo da simulação.
        
        Args:
            modo: 'ambiente' para convecção com ambiente, 
                  'conducao' para condução entre dois corpos
            **kwargs: Parâmetros específicos do modo
        """
        if modo == 'ambiente':
            # Cada corpo troca calor com o ambiente
            for corpo in self.corpos:
                delta_Q = self.simular_conveccao_ambiente(corpo)
                corpo.atualizar_temperatura(delta_Q, self.delta_t)
                
        elif modo == 'conducao':
            # Dois corpos trocam calor entre si
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
        
        # Registra o estado de todos os corpos
        for corpo in self.corpos:
            corpo.registrar_estado(self.tempo_atual)
    
    def simular(self, tempo_total, modo='ambiente', **kwargs):
        """
        Executa a simulação por um período de tempo.
        
        Args:
            tempo_total: Tempo total de simulação (s)
            modo: Modo de simulação ('ambiente' ou 'conducao')
            **kwargs: Parâmetros adicionais
        """
        num_passos = int(tempo_total / self.delta_t)
        
        for _ in range(num_passos):
            self.executar_passo(modo, **kwargs)
            
        return self.obter_resultados()
    
    def obter_resultados(self):
        """
        Retorna os resultados da simulação.
        
        Returns:
            Lista de dicionários com histórico de cada corpo
        """
        resultados = []
        for corpo in self.corpos:
            resultados.append({
                'nome': corpo.nome,
                'tempo': corpo.historico_tempo.copy(),
                'temperatura': corpo.historico_temperatura.copy()
            })
        return resultados
