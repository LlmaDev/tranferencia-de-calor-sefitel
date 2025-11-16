# Simulador de Transferência de Calor

**Projeto desenvolvido para a disciplina de Física 2 (SEFITEL)**  
**Inatel - 2º Semestre de 2025**

**Tema:** Desenvolvimento de projeto com auxílio de Inteligência Artificial  
**Ferramentas utilizadas:** GitHub Copilot (VS Code) + Claude Sonnet 4.5

---

Sistema para simular transferência de calor entre corpos e com o ambiente.

## 📋 Descrição

Este projeto permite simular:
- **Convecção**: Troca de calor entre um corpo e o ambiente (ar)
- **Condução**: Troca de calor entre dois corpos em contato

## 🚀 Como Usar

### 1. Instalar dependências

```bash
pip install matplotlib numpy
```

### 2. Executar o simulador

```bash
python main.py
```

O programa irá guiá-lo passo a passo:
1. **Escolher material** - Selecione de um banco de 5 materiais (água, alumínio, cobre, ferro, vidro)
2. **Configurar corpo** - Defina massa, área e temperatura inicial
3. **Configurar ambiente** - Escolha temperatura e tipo de convecção
4. **Configurar simulação** - Defina tempo e precisão
5. **Ver resultados** - Gráfico interativo automático

### Exemplo de uso programático

```python
from corpo_termico import CorpoTermico
from simulador import SimuladorTermico
from visualizacao import plotar_resultados

# Criar um corpo
corpo = CorpoTermico(
    nome="Meu Objeto",
    massa=1.0,              # kg
    calor_especifico=900,   # J/(kg·K)
    area_superficie=0.01,   # m²
    temperatura_inicial=80  # °C
)

# Criar simulador
sim = SimuladorTermico(delta_t=10)  # passo de 10 segundos
sim.adicionar_corpo(corpo)
sim.configurar_ambiente(temperatura=25, coef_conveccao=10)

# Simular por 10 minutos
resultados = sim.simular(tempo_total=600, modo='ambiente')

# Plotar resultados
plotar_resultados(resultados)
```

## 📊 Parâmetros Importantes

### Corpo Térmico
- **massa**: Massa do objeto (kg)
- **calor_especifico**: Capacidade do material de armazenar calor (J/kg·K)
  - Água: 4186
  - Alumínio: 900
  - Cobre: 385
  - Ferro: 450
- **area_superficie**: Área exposta para troca de calor (m²)
- **temperatura_inicial**: Temperatura inicial (°C)

### Simulação
- **delta_t**: Intervalo de tempo entre cálculos (segundos)
- **temperatura_ambiente**: Temperatura do ar ao redor (°C)
- **coef_conveccao**: Coeficiente de convecção (W/m²·K)
  - Convecção natural com ar: 5-25
  - Convecção forçada com ar: 25-250

## 🧮 Equações Utilizadas

**Lei de Newton do Resfriamento (Convecção):**
$$\dot{Q} = h \cdot A \cdot (T_{corpo} - T_{ambiente})$$

**Lei de Fourier (Condução):**
$$\dot{Q} = k \cdot A \cdot \frac{(T_1 - T_2)}{L}$$

**Variação de Temperatura:**
$$\Delta T = \frac{\Delta Q}{m \cdot c}$$

## 📁 Estrutura do Projeto

```
sefitel/
├── corpo_termico.py         # Classe para representar corpos
├── transferencia_calor.py   # Funções de física térmica
├── simulador.py             # Motor de simulação
├── visualizacao.py          # Plotagem de gráficos
├── banco_materiais.py       # Gerenciador de materiais
├── materiais.json           # Banco de dados de materiais
├── main.py                  # Programa principal interativo
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md                # Este arquivo
```

## 🗂️ Banco de Materiais

O arquivo `materiais.json` contém 5 materiais predefinidos:

| Material  | Calor Específico | Densidade | Aplicações                    |
|-----------|------------------|-----------|-------------------------------|
| Água      | 4186 J/(kg·K)   | 1000 kg/m³| Bebidas, refrigeração         |
| Alumínio  | 900 J/(kg·K)    | 2700 kg/m³| Panelas, dissipadores         |
| Cobre     | 385 J/(kg·K)    | 8960 kg/m³| Fios, trocadores de calor     |
| Ferro     | 450 J/(kg·K)    | 7874 kg/m³| Estruturas, ferramentas       |
| Vidro     | 840 J/(kg·K)    | 2500 kg/m³| Janelas, recipientes          |

Você pode adicionar mais materiais editando o arquivo `materiais.json`.

## 🎯 Exemplo de Saída

O programa exibe:
1. Condições iniciais da simulação
2. Temperatura final após simulação
3. Gráfico interativo mostrando a evolução da temperatura ao longo do tempo

---

**Desenvolvido para SEFITEL - Física 2**  
**Inatel - 2025/2**  

Este projeto foi desenvolvido como parte do SEFITEL 2025, que propôs o uso de ferramentas de IA para auxiliar no desenvolvimento. Utilizamos o GitHub Copilot integrado ao VS Code com o modelo Claude Sonnet 3.5 para implementação do simulador de transferência de calor.
