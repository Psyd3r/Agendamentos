import json
import os
from datetime import datetime
import time

# Arquitetura em camadas:
# 1. Camada de Modelo (dados)
# 2. Camada de Serviço (lógica de negócio)
# 3. Camada de Interface (terminal)

# Constantes
DATA_FILE = "dados_frequencia.json"


# Estrutura básica das classes
#############################
# CAMADA DE MODELO (DADOS) #
#############################

class Modelo:
    def __init__(self):
        self.dados = self._carregar_dados()
    
    def _carregar_dados(self):
        """Carrega os dados do arquivo JSON ou cria uma estrutura vazia se não existir."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Erro ao carregar arquivo. Criando nova estrutura de dados.")
        return {"turmas": {}, "alunos": {}, "frequencias": {}}
    
    def _salvar_dados(self):
        """Salva os dados no arquivo JSON."""
        with open(DATA_FILE, 'w') as file:
            json.dump(self.dados, file, indent=4)
    
    def adicionar_turma(self, codigo, nome, periodo):
        """Adiciona uma nova turma."""
        self.dados["turmas"][codigo] = {
            "nome": nome,
            "periodo": periodo
        }
        self._salvar_dados()
    
    def listar_turmas(self):
        """Retorna todas as turmas."""
        return self.dados["turmas"]
    
    def obter_turma(self, codigo):
        """Retorna uma turma específica pelo código."""
        return self.dados["turmas"].get(codigo)
    
    def adicionar_aluno(self, matricula, nome, turma_codigo):
        """Adiciona um novo aluno."""
        if turma_codigo in self.dados["turmas"]:
            self.dados["alunos"][matricula] = {
                "nome": nome,
                "turma": turma_codigo
            }
            self._salvar_dados()
            return True
        return False
    
    def listar_alunos(self, turma_codigo=None):
        """Retorna todos os alunos ou apenas de uma turma específica."""
        if turma_codigo:
            return {k: v for k, v in self.dados["alunos"].items() if v["turma"] == turma_codigo}
        return self.dados["alunos"]
    
    def obter_aluno(self, matricula):
        """Retorna um aluno específico pela matrícula."""
        return self.dados["alunos"].get(matricula)
    
    def registrar_presenca(self, turma_codigo, data, presencas):
        """Registra a presença dos alunos em uma data específica."""
        if turma_codigo not in self.dados["frequencias"]:
            self.dados["frequencias"][turma_codigo] = {}
        
        self.dados["frequencias"][turma_codigo][data] = presencas
        self._salvar_dados()
    
    def consultar_frequencia(self, turma_codigo, data=None):
        """Consulta a frequência de uma turma em uma data específica ou em todas as datas."""
        if turma_codigo not in self.dados["frequencias"]:
            return {}
        
        if data:
            return self.dados["frequencias"][turma_codigo].get(data, {})
        return self.dados["frequencias"][turma_codigo]
    
    def obter_relatorio_aluno(self, matricula):
        """Retorna um relatório de presença de um aluno específico."""
        aluno = self.obter_aluno(matricula)
        if not aluno:
            return None
        
        turma_codigo = aluno["turma"]
        if turma_codigo not in self.dados["frequencias"]:
            return {"aluno": aluno, "presencas": {}, "percentual": 0}
        
        presencas = {}
        total_aulas = 0
        total_presencas = 0
        
        for data, registros in self.dados["frequencias"][turma_codigo].items():
            presente = registros.get(matricula, False)
            presencas[data] = presente
            total_aulas += 1
            if presente:
                total_presencas += 1
        
        percentual = (total_presencas / total_aulas * 100) if total_aulas > 0 else 0
        
        return {
            "aluno": aluno,
            "presencas": presencas,
            "total_aulas": total_aulas,
            "total_presencas": total_presencas,
            "percentual": percentual
        }

##################################
# CAMADA DE SERVIÇO (LÓGICA)     #
##################################

class Servico:
    def __init__(self):
        self.modelo = Modelo()
    
    def adicionar_turma(self, codigo, nome, periodo):
        """Adiciona uma nova turma."""
        if codigo and nome and periodo:
            if not self.modelo.obter_turma(codigo):
                self.modelo.adicionar_turma(codigo, nome, periodo)
                return True, "Turma adicionada com sucesso!"
            return False, "Código de turma já existe!"
        return False, "Todos os campos são obrigatórios!"
    
    def listar_turmas(self):
        """Lista todas as turmas cadastradas."""
        return self.modelo.listar_turmas()
    
    def adicionar_aluno(self, matricula, nome, turma_codigo):
        """Adiciona um novo aluno."""
        if matricula and nome and turma_codigo:
            if not self.modelo.obter_aluno(matricula):
                if self.modelo.obter_turma(turma_codigo):
                    self.modelo.adicionar_aluno(matricula, nome, turma_codigo)
                    return True, "Aluno adicionado com sucesso!"
                return False, "Turma não encontrada!"
            return False, "Matrícula já existe!"
        return False, "Todos os campos são obrigatórios!"
    
    def listar_alunos(self, turma_codigo=None):
        """Lista todos os alunos ou apenas de uma turma específica."""
        return self.modelo.listar_alunos(turma_codigo)
    
    def registrar_presenca(self, turma_codigo, data, presencas):
        """Registra a presença dos alunos."""
        if not self.modelo.obter_turma(turma_codigo):
            return False, "Turma não encontrada!"
        
        self.modelo.registrar_presenca(turma_codigo, data, presencas)
        return True, "Presenças registradas com sucesso!"
    
    def consultar_frequencia(self, turma_codigo, data=None):
        """Consulta a frequência de uma turma."""
        if not self.modelo.obter_turma(turma_codigo):
            return False, "Turma não encontrada!"
        
        frequencia = self.modelo.consultar_frequencia(turma_codigo, data)
        if not frequencia and data:
            return False, "Não há registros para esta data!"
        return True, frequencia
    
    def relatorio_aluno(self, matricula):
        """Gera um relatório de presença de um aluno."""
        relatorio = self.modelo.obter_relatorio_aluno(matricula)
        if not relatorio:
            return False, "Aluno não encontrado!"
        return True, relatorio

class Interface:
    def __init__(self):
        pass

# Execução do programa
if __name__ == "__main__":
    print("Sistema de Controle de Frequência - Inicializado")