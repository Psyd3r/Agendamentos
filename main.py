from utils import (
    print_glitch, loading_bar, show_menu, clear, ascii_art,
    mostra_titulo, input_com_voltar, input_inteiro, input_data,
    confirmacao, exibir_ajuda
)
from controllers import (
    cadastrar_turma, cadastrar_aluno, marcar_presenca,
    consultar_frequencia_por_turma, relatorio_por_aluno,
    listar_turmas, listar_alunos, obter_nome_turma, obter_nome_aluno
)

def menu_cadastrar_turma():
    mostra_titulo("CADASTRAR TURMA")
    
    try:
        nome = input_com_voltar("Nome da turma:")
        if nome is None:
            return
        
        if not nome or len(nome.strip()) == 0:
            print("Erro: Nome da turma não pode ser vazio")
            input("\nPressione Enter para continuar...")
            return
        
        turma = cadastrar_turma(nome)
        print(f"\nTurma '{turma.nome}' cadastrada com ID {turma.id}.")
    except Exception as e:
        print(f"\nErro ao cadastrar turma: {str(e)}")
    
    input("\nPressione Enter para continuar...")

def menu_cadastrar_aluno():
    mostra_titulo("CADASTRAR ALUNO")
    
    try:
        # Listar turmas disponíveis
        turmas = listar_turmas()
        if not turmas:
            print("Não há turmas cadastradas. Cadastre uma turma primeiro.")
            input("\nPressione Enter para continuar...")
            return
        
        print("Turmas disponíveis:")
        for t in turmas:
            print(f"  {t['id']} - {t['nome']}")
        
        turma_id = input_inteiro("\nID da turma:", min_valor=1)
        if turma_id is None:
            return
        
        nome = input_com_voltar("Nome do aluno:")
        if nome is None:
            return
        
        if not nome or len(nome.strip()) == 0:
            print("Erro: Nome do aluno não pode ser vazio")
            input("\nPressione Enter para continuar...")
            return
        
        aluno = cadastrar_aluno(nome, turma_id)
        nome_turma = obter_nome_turma(turma_id)
        print(f"\nAluno '{aluno.nome}' cadastrado na turma '{nome_turma}'.")
    except Exception as e:
        print(f"\nErro ao cadastrar aluno: {str(e)}")
    
    input("\nPressione Enter para continuar...")

def menu_marcar_presenca():
    mostra_titulo("MARCAR PRESENÇA")
    
    try:
        # Listar turmas disponíveis
        turmas = listar_turmas()
        if not turmas:
            print("Não há turmas cadastradas. Cadastre uma turma primeiro.")
            input("\nPressione Enter para continuar...")
            return
        
        print("Turmas disponíveis:")
        for t in turmas:
            print(f"  {t['id']} - {t['nome']}")
        
        turma_id = input_inteiro("\nID da turma:", min_valor=1)
        if turma_id is None:
            return
        
        alunos, nome_turma = listar_alunos(turma_id)
        if not alunos:
            print(f"Não há alunos cadastrados na turma '{nome_turma}'.")
            input("\nPressione Enter para continuar...")
            return
        
        print(f"\nMarcando presença para a turma '{nome_turma}'")
        data_str = input_data("Data (yyyy-mm-dd) ou 'hoje':")
        if data_str is None:
            return
        
        print("\nRegistrando presença (P = Presente, F = Faltou):")
        for a in alunos:
            while True:
                resp = input_com_voltar(f"  {a['nome']}:")
                if resp is None:
                    return
                
                if resp.upper() in ['P', 'F']:
                    presenca = resp.upper() == 'P'
                    marcar_presenca(a['id'], data_str, presenca)
                    break
                else:
                    print("  Digite P para presente ou F para faltou")
        
        print("\nPresença registrada com sucesso.")
    except Exception as e:
        print(f"\nErro ao marcar presença: {str(e)}")
    
    input("\nPressione Enter para continuar...")

def menu_consultar_frequencia():
    mostra_titulo("CONSULTAR FREQUÊNCIA POR TURMA")
    
    try:
        # Listar turmas disponíveis
        turmas = listar_turmas()
        if not turmas:
            print("Não há turmas cadastradas.")
            input("\nPressione Enter para continuar...")
            return
        
        print("Turmas disponíveis:")
        for t in turmas:
            print(f"  {t['id']} - {t['nome']}")
        
        turma_id = input_inteiro("\nID da turma:", min_valor=1)
        if turma_id is None:
            return
        
        freq, nome_turma = consultar_frequencia_por_turma(turma_id)
        
        if not freq:
            print(f"Não há registros de frequência para a turma '{nome_turma}'.")
            input("\nPressione Enter para continuar...")
            return
        
        print(f"\nRelatório de Frequência - Turma: {nome_turma}\n")
        print("Nome                  Presenças  Faltas    Percentual")
        print("─" * 55)
        
        for nome, registros in freq.items():
            if not registros:
                print(f"{nome[:20]:<20}  0         0         0%")
                continue
                
            presencas = sum(1 for r in registros if r['presente'])
            faltas = len(registros) - presencas
            total = len(registros)
            percentual = int((presencas / total) * 100) if total > 0 else 0
            
            print(f"{nome[:20]:<20}  {presencas:<9} {faltas:<9} {percentual}%")
    except Exception as e:
        print(f"\nErro ao consultar frequência: {str(e)}")
    
    input("\nPressione Enter para continuar...")

def menu_relatorio_aluno():
    mostra_titulo("RELATÓRIO POR ALUNO")
    
    try:
        # Listar turmas disponíveis para filtrar alunos
        turmas = listar_turmas()
        if not turmas:
            print("Não há turmas cadastradas.")
            input("\nPressione Enter para continuar...")
            return
        
        print("Selecione uma turma para filtrar alunos:")
        for t in turmas:
            print(f"  {t['id']} - {t['nome']}")
        print("  0 - Ver todos os alunos")
        
        turma_id = input_inteiro("\nID da turma (0 para todos):", min_valor=0)
        if turma_id is None:
            return
        
        if turma_id == 0:
            alunos, _ = listar_alunos()
            if not alunos:
                print("Não há alunos cadastrados.")
                input("\nPressione Enter para continuar...")
                return
            print("\nAlunos disponíveis:")
        else:
            alunos, nome_turma = listar_alunos(turma_id)
            if not alunos:
                print(f"Não há alunos cadastrados na turma '{nome_turma}'.")
                input("\nPressione Enter para continuar...")
                return
            print(f"\nAlunos da turma '{nome_turma}':")
        
        for a in alunos:
            print(f"  {a['id']} - {a['nome']}")
        
        aluno_id = input_inteiro("\nID do aluno:", min_valor=1)
        if aluno_id is None:
            return
        
        registros, nome_aluno = relatorio_por_aluno(aluno_id)
        
        if not registros:
            print(f"Não há registros de presença para o aluno '{nome_aluno}'.")
            input("\nPressione Enter para continuar...")
            return
        
        print(f"\nRelatório de Presença - Aluno: {nome_aluno}\n")
        print("Data        Status")
        print("─" * 25)
        
        presencas = 0
        for r in sorted(registros, key=lambda x: x['data']):
            status = "Presente" if r['presente'] else "Faltou"
            if r['presente']:
                presencas += 1
            print(f"{r['data']}  {status}")
        
        total = len(registros)
        percentual = int((presencas / total) * 100) if total > 0 else 0
        
        print("─" * 25)
        print(f"Total: {presencas} presenças em {total} aulas ({percentual}%)")
    except Exception as e:
        print(f"\nErro ao gerar relatório: {str(e)}")
    
    input("\nPressione Enter para continuar...")

def menu_listar_turmas():
    mostra_titulo("LISTAR TURMAS")
    
    try:
        turmas = listar_turmas()
        
        if not turmas:
            print("Não há turmas cadastradas.")
            input("\nPressione Enter para continuar...")
            return
        
        print("Turmas cadastradas:\n")
        print("ID    Nome")
        print("─" * 30)
        
        for turma in turmas:
            print(f"{turma['id']:<5} {turma['nome']}")
    except Exception as e:
        print(f"\nErro ao listar turmas: {str(e)}")
    
    input("\nPressione Enter para continuar...")

def menu_listar_alunos():
    mostra_titulo("LISTAR ALUNOS POR TURMA")
    
    try:
        # Listar turmas disponíveis
        turmas = listar_turmas()
        if not turmas:
            print("Não há turmas cadastradas.")
            input("\nPressione Enter para continuar...")
            return
        
        print("Turmas disponíveis:")
        for t in turmas:
            print(f"  {t['id']} - {t['nome']}")
        print("  0 - Ver todos os alunos")
        
        turma_id = input_inteiro("\nID da turma (0 para todos):", min_valor=0)
        if turma_id is None:
            return
        
        if turma_id == 0:
            alunos, _ = listar_alunos()
            if not alunos:
                print("Não há alunos cadastrados.")
                input("\nPressione Enter para continuar...")
                return
            
            print("\nTodos os alunos cadastrados:\n")
            print("ID    Nome                  Turma")
            print("─" * 40)
            
            for a in alunos:
                try:
                    nome_turma = obter_nome_turma(a['turma_id'])
                    print(f"{a['id']:<5} {a['nome'][:20]:<20} {nome_turma}")
                except:
                    print(f"{a['id']:<5} {a['nome'][:20]:<20} <Turma não encontrada>")
        else:
            alunos, nome_turma = listar_alunos(turma_id)
            if not alunos:
                print(f"Não há alunos cadastrados na turma '{nome_turma}'.")
                input("\nPressione Enter para continuar...")
                return
            
            print(f"\nAlunos da turma '{nome_turma}':\n")
            print("ID    Nome")
            print("─" * 30)
            
            for a in alunos:
                print(f"{a['id']:<5} {a['nome']}")
    except Exception as e:
        print(f"\nErro ao listar alunos: {str(e)}")
    
    input("\nPressione Enter para continuar...")

def main():
    try:
        clear()
        print_glitch(ascii_art)
        loading_bar()
        
        while True:
            try:
                show_menu()
                op = input().lower()
                
                if op == 'h':
                    exibir_ajuda()
                    continue
                
                clear()
                
                if op == '1':
                    menu_cadastrar_turma()
                elif op == '2':
                    menu_cadastrar_aluno()
                elif op == '3':
                    menu_marcar_presenca()
                elif op == '4':
                    menu_consultar_frequencia()
                elif op == '5':
                    menu_relatorio_aluno()
                elif op == '6':
                    menu_listar_turmas()
                elif op == '7':
                    menu_listar_alunos()
                elif op == '8':
                    exibir_ajuda()
                elif op == '0':
                    if confirmacao("Deseja realmente sair do sistema?"):
                        break
                else:
                    print("Opção inválida!")
                    input("\nPressione Enter para continuar...")
            except KeyboardInterrupt:
                clear()
                if confirmacao("Deseja realmente sair do sistema?"):
                    break
                continue
            except Exception as e:
                print(f"Erro inesperado: {str(e)}")
                input("\nPressione Enter para continuar...")
    except KeyboardInterrupt:
        clear()
        print("Sistema encerrado pelo usuário.")
    except Exception as e:
        clear()
        print(f"Erro crítico: {str(e)}")
        input("\nPressione Enter para encerrar...")
    finally:
        clear()
        print_glitch("Sistema encerrado. Até logo!")
        time.sleep(1)

if __name__ == "__main__":
    main()