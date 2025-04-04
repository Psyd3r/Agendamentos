from database import load_data, save_data
from models import Turma, Aluno, Presenca
from utils import gerar_id

def cadastrar_turma(nome):
    data = load_data()
    turma = Turma(id=gerar_id(data["turmas"]), nome=nome)
    data["turmas"].append(turma.__dict__)
    save_data(data)
    return turma

def cadastrar_aluno(nome, turma_id):
    data = load_data()
    aluno = Aluno(id=gerar_id(data["alunos"]), nome=nome, turma_id=turma_id)
    data["alunos"].append(aluno.__dict__)
    save_data(data)
    return aluno

def marcar_presenca(aluno_id, data_str, presente):
    data = load_data()
    presenca = Presenca(aluno_id=aluno_id, data=data_str, presente=presente)
    data["presencas"].append(presenca.__dict__)
    save_data(data)

def consultar_frequencia_por_turma(turma_id):
    data = load_data()
    alunos = [a for a in data["alunos"] if a["turma_id"] == turma_id]
    presencas = data["presencas"]
    result = {}
    for aluno in alunos:
        freq = [p for p in presencas if p["aluno_id"] == aluno["id"]]
        result[aluno["nome"]] = freq
    return result

def relatorio_por_aluno(aluno_id):
    data = load_data()
    presencas = [p for p in data["presencas"] if p["aluno_id"] == aluno_id]
    return presencas

def listar_turmas():
    return load_data()["turmas"]

def listar_alunos(turma_id=None):
    alunos = load_data()["alunos"]
    return [a for a in alunos if turma_id is None or a["turma_id"] == turma_id]
