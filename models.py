from dataclasses import dataclass

@dataclass
class Turma:
    id: int
    nome: str

@dataclass
class Aluno:
    id: int
    nome: str
    turma_id: int

@dataclass
class Presenca:
    aluno_id: int
    data: str  # yyyy-mm-dd
    presente: bool