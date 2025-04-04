from utils import print_glitch, loading_bar, show_menu, clear, ascii_art
from controllers import (
    cadastrar_turma, cadastrar_aluno, marcar_presenca,
    consultar_frequencia_por_turma, relatorio_por_aluno,
    listar_turmas, listar_alunos
)

def main():
    clear()
    print_glitch(ascii_art)
    loading_bar()
    while True:
        show_menu()
        op = input()
        clear()
        if op == '1':
            nome = input("Nome da turma: ")
            turma = cadastrar_turma(nome)
            print(f"Turma '{turma.nome}' cadastrada com ID {turma.id}.")
        elif op == '2':
            turmas = listar_turmas()
            for t in turmas:
                print(f"{t['id']} - {t['nome']}")
            turma_id = int(input("ID da turma: "))
            nome = input("Nome do aluno: ")
            aluno = cadastrar_aluno(nome, turma_id)
            print(f"Aluno '{aluno.nome}' cadastrado.")
        elif op == '3':
            turma_id = int(input("ID da turma: "))
            alunos = listar_alunos(turma_id)
            data_str = input("Data (yyyy-mm-dd): ")
            for a in alunos:
                presenca = input(f"{a['nome']} (P/N): ").upper() == 'P'
                marcar_presenca(a['id'], data_str, presenca)
            print("Presença registrada.")
        elif op == '4':
            turma_id = int(input("ID da turma: "))
            freq = consultar_frequencia_por_turma(turma_id)
            for nome, registros in freq.items():
                presencas = sum(1 for r in registros if r['presente'])
                total = len(registros)
                print(f"{nome}: {presencas}/{total} presenças")
        elif op == '5':
            alunos = listar_alunos()
            for a in alunos:
                print(f"{a['id']} - {a['nome']}")
            aluno_id = int(input("ID do aluno: "))
            registros = relatorio_por_aluno(aluno_id)
            for r in registros:
                status = "Presente" if r['presente'] else "Faltou"
                print(f"{r['data']}: {status}")
        elif op == '6':
            turmas = listar_turmas()
            print("\nTurmas cadastradas:")
            for turma in turmas:
                print(f"ID: {turma['id']}, Nome: {turma['nome']}")
        elif op == '7':
            turmas = listar_turmas()
            for t in turmas:
                print(f"{t['id']} - {t['nome']}")
            turma_id = int(input("ID da turma: "))
            alunos = listar_alunos(turma_id)
            print(f"\nAlunos da turma {turma_id}:")
            for a in alunos:
                print(f"ID: {a['id']}, Nome: {a['nome']}")
        elif op == '0':
            break
        else:
            print("Opção inválida!")
        input("\nPressione Enter para continuar...")
        clear()

if __name__ == "__main__":
    main()
