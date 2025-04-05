from database import load_data, save_data
from models import Turma, Aluno, Presenca
from utils import gerar_id
from datetime import datetime


def validar_data(data_str):
    """Valida se a data está no formato correto yyyy-mm-dd"""
    if len(data_str) != 10:
        return False
    
    partes = data_str.split('-')
    if len(partes) != 3:
        return False
    
    try:
        ano, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
        return True
    except ValueError:
        return False

def cadastrar_turma(nome):
    if not nome or len(nome.strip()) == 0:
        raise ValueError("Nome da turma não pode ser vazio")
    
    data = load_data()
    turma = Turma(id=gerar_id(data["turmas"]), nome=nome)
    data["turmas"].append(turma.__dict__)
    if save_data(data):
        return turma
    else:
        raise Exception("Não foi possível salvar a turma")

def cadastrar_aluno(nome, turma_id):
    if not nome or len(nome.strip()) == 0:
        raise ValueError("Nome do aluno não pode ser vazio")
    
    data = load_data()
    # Verificar se a turma existe
    turma_existe = any(t["id"] == turma_id for t in data["turmas"])
    if not turma_existe:
        raise ValueError(f"Turma com ID {turma_id} não existe")
    
    aluno = Aluno(id=gerar_id(data["alunos"]), nome=nome, turma_id=turma_id)
    data["alunos"].append(aluno.__dict__)
    if save_data(data):
        return aluno
    else:
        raise Exception("Não foi possível salvar o aluno")

def marcar_presenca(aluno_id, data_str, presente):
    if not validar_data(data_str):
        raise ValueError("Formato de data inválido. Use yyyy-mm-dd")
    
    data = load_data()
    # Verificar se o aluno existe
    aluno_existe = any(a["id"] == aluno_id for a in data["alunos"])
    if not aluno_existe:
        raise ValueError(f"Aluno com ID {aluno_id} não existe")
    
    # Verificar se já existe registro para este aluno nesta data
    registro_existente = next((
        i for i, p in enumerate(data["presencas"]) 
        if p["aluno_id"] == aluno_id and p["data"] == data_str
    ), None)
    
    presenca = Presenca(aluno_id=aluno_id, data=data_str, presente=presente)
    
    if registro_existente is not None:
        # Atualizar registro existente
        data["presencas"][registro_existente] = presenca.__dict__
    else:
        # Criar novo registro
        data["presencas"].append(presenca.__dict__)
    
    if not save_data(data):
        raise Exception("Não foi possível salvar a presença")

def consultar_frequencia_por_turma(turma_id):
    data = load_data()
    # Verificar se a turma existe
    turma = next((t for t in data["turmas"] if t["id"] == turma_id), None)
    if turma is None:
        raise ValueError(f"Turma com ID {turma_id} não existe")
    
    alunos = [a for a in data["alunos"] if a["turma_id"] == turma_id]
    presencas = data["presencas"]
    result = {}
    for aluno in alunos:
        freq = [p for p in presencas if p["aluno_id"] == aluno["id"]]
        result[aluno["nome"]] = freq
    return result, turma["nome"]

def relatorio_por_aluno(aluno_id):
    data = load_data()
    # Verificar se o aluno existe
    aluno = next((a for a in data["alunos"] if a["id"] == aluno_id), None)
    if aluno is None:
        raise ValueError(f"Aluno com ID {aluno_id} não existe")
    
    presencas = [p for p in data["presencas"] if p["aluno_id"] == aluno_id]
    return presencas, aluno["nome"]

def listar_turmas():
    return load_data()["turmas"]

def listar_alunos(turma_id=None):
    data = load_data()
    alunos = data["alunos"]
    
    if turma_id is not None:
        # Verificar se a turma existe
        turma = next((t for t in data["turmas"] if t["id"] == turma_id), None)
        if turma is None:
            raise ValueError(f"Turma com ID {turma_id} não existe")
        return [a for a in alunos if a["turma_id"] == turma_id], turma["nome"]
    
    return alunos, None

def obter_nome_turma(turma_id):
    data = load_data()
    turma = next((t for t in data["turmas"] if t["id"] == turma_id), None)
    if turma is None:
        raise ValueError(f"Turma com ID {turma_id} não existe")
    return turma["nome"]

def obter_nome_aluno(aluno_id):
    data = load_data()
    aluno = next((a for a in data["alunos"] if a["id"] == aluno_id), None)
    if aluno is None:
        raise ValueError(f"Aluno com ID {aluno_id} não existe")
    return aluno["nome"]