"""
Módulo para carregar e gerenciar materiais do banco de dados JSON.
"""

import json
import os


class BancoMateriais:
    """Gerencia o banco de dados de materiais."""
    
    def __init__(self, arquivo_json="materiais.json"):
        """
        Inicializa o banco de materiais.
        
        Args:
            arquivo_json: Caminho para o arquivo JSON com os materiais
        """
        self.arquivo_json = arquivo_json
        self.dados = self._carregar_json()
        
    def _carregar_json(self):
        """Carrega os dados do arquivo JSON."""
        caminho = os.path.join(os.path.dirname(__file__), self.arquivo_json)
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Erro: Arquivo {self.arquivo_json} não encontrado!")
            return {"materiais": [], "coeficientes_conveccao": {}}
        except json.JSONDecodeError:
            print(f"Erro: Arquivo {self.arquivo_json} com formato inválido!")
            return {"materiais": [], "coeficientes_conveccao": {}}
    
    def listar_materiais(self):
        """Retorna a lista de todos os materiais disponíveis."""
        return self.dados.get("materiais", [])
    
    def obter_material(self, material_id):
        """
        Obtém um material específico pelo ID.
        
        Args:
            material_id: ID do material (int)
            
        Returns:
            Dicionário com dados do material ou None se não encontrado
        """
        for material in self.dados.get("materiais", []):
            if material["id"] == material_id:
                return material
        return None
    
    def obter_material_por_nome(self, nome):
        """
        Obtém um material específico pelo nome.
        
        Args:
            nome: Nome do material (str)
            
        Returns:
            Dicionário com dados do material ou None se não encontrado
        """
        for material in self.dados.get("materiais", []):
            if material["nome"].lower() == nome.lower():
                return material
        return None
    
    def listar_coeficientes_conveccao(self):
        """Retorna os coeficientes de convecção disponíveis."""
        return self.dados.get("coeficientes_conveccao", {})
    
    def obter_coeficiente_conveccao(self, tipo):
        """
        Obtém um coeficiente de convecção específico.
        
        Args:
            tipo: Tipo de convecção (ex: 'ar_parado', 'ventilador')
            
        Returns:
            Dicionário com dados do coeficiente ou None
        """
        return self.dados.get("coeficientes_conveccao", {}).get(tipo)
    
    def exibir_materiais(self):
        """Exibe todos os materiais disponíveis de forma formatada."""
        materiais = self.listar_materiais()
        
        if not materiais:
            print("Nenhum material disponivel.")
            return
        
        print("\n" + "=" * 70)
        print("MATERIAIS DISPONIVEIS")
        print("=" * 70)
        
        for mat in materiais:
            print(f"\n[{mat['id']}] {mat['nome']}")
            print(f"    - Calor especifico: {mat['calor_especifico']} {mat['unidade']}")
            print(f"    - Densidade: {mat['densidade']} kg/m³")
            print(f"    - {mat['descricao']}")
            print(f"    - Aplicacoes: {', '.join(mat['aplicacoes'])}")
        
        print("\n" + "=" * 70)
    
    def exibir_coeficientes(self):
        """Exibe os coeficientes de convecção disponíveis."""
        coefs = self.listar_coeficientes_conveccao()
        
        if not coefs:
            print("Nenhum coeficiente disponivel.")
            return
        
        print("\n" + "=" * 70)
        print("COEFICIENTES DE CONVECCAO")
        print("=" * 70)
        
        i = 1
        for chave, dados in coefs.items():
            print(f"\n[{i}] {dados['descricao']}")
            print(f"    - Valor padrao: {dados['valor']} W/m²·K")
            print(f"    - Faixa tipica: {dados['faixa']}")
            print(f"    - Codigo: '{chave}'")
            i += 1
        
        print("\n" + "=" * 70)


# Funções auxiliares para uso direto
def carregar_materiais():
    """Carrega e retorna o banco de materiais."""
    return BancoMateriais()


def obter_calor_especifico(material_id):
    """
    Obtém o calor específico de um material pelo ID.
    
    Args:
        material_id: ID do material
        
    Returns:
        Calor específico em J/(kg·K) ou None
    """
    banco = BancoMateriais()
    material = banco.obter_material(material_id)
    return material["calor_especifico"] if material else None
