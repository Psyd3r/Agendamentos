# ======================== database.py ========================
import json
import os

DB_FILE = "db.json"

def load_data():
    try:
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, 'w') as f:
                json.dump({"turmas": [], "alunos": [], "presencas": []}, f)
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Erro: Arquivo de banco de dados corrompido.")
        if os.path.exists(DB_FILE + ".bak"):
            print("Restaurando backup...")
            os.replace(DB_FILE + ".bak", DB_FILE)
            return load_data()
        else:
            print("Criando novo banco de dados...")
            with open(DB_FILE, 'w') as f:
                json.dump({"turmas": [], "alunos": [], "presencas": []}, f)
            return {"turmas": [], "alunos": [], "presencas": []}
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return {"turmas": [], "alunos": [], "presencas": []}

def save_data(data):
    try:
        # Criar backup antes de salvar
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as f_orig:
                with open(DB_FILE + ".bak", 'w') as f_bak:
                    f_bak.write(f_orig.read())
        
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {str(e)}")
        return False

# ======================== models.py ========================
from dataclasses import dataclass
from datetime import datetime

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

# ======================== controllers.py ========================
from database import load_data, save_data
from models import Turma, Aluno, Presenca
from utils import gerar_id
from datetime import datetime

def validar_data(data_str):
    """Valida se a data está no formato correto yyyy-mm-dd"""
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
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

# ======================== utils.py ========================
import time
import sys
import random
import shutil
import os
from datetime import datetime

def gerar_id(lista):
    if not lista:
        return 1
    return max(item['id'] for item in lista) + 1

def get_terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def center_line(line):
    width = get_terminal_width()
    padding = max((width - len(line)) // 2, 0)
    return ' ' * padding + line

def glitch_char(c):
    glitch_set = ['#', '%', '$', '@', '&', '*', '+', '!', '?', '=', '▮']
    return random.choice(glitch_set) if random.random() < 0.1 else c

def print_glitch(text, delay=0.004):
    for line in text.splitlines():
        glitched = ''.join(glitch_char(c) for c in line)
        print(f"\033[92m{center_line(glitched)}\033[0m")
        time.sleep(delay)

def loading_bar(total=30, delay=0.1):
    print("\n" + center_line("\033[92mInicializando módulos do sistema...\033[0m") + "\n")
    for i in range(total + 1):
        percent = int((i / total) * 100)
        bar = '█' * i + '-' * (total - i)
        sys.stdout.write('\r' + center_line(f"\033[92m[{bar}] {percent}%\033[0m"))
        sys.stdout.flush()
        time.sleep(delay)
    print("\n" + center_line("\033[92mCarregamento completo!\033[0m"))
    time.sleep(1)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_com_voltar(prompt):
    """Função para input com opção de voltar ao menu"""
    print(f"{prompt} (Digite 'v' para voltar ao menu)")
    valor = input("> ")
    if valor.lower() == 'v':
        return None
    return valor

def input_inteiro(prompt, min_valor=None, max_valor=None):
    """Função para input de número inteiro com validação"""
    while True:
        valor = input_com_voltar(prompt)
        if valor is None:
            return None
        
        try:
            num = int(valor)
            if (min_valor is not None and num < min_valor) or (max_valor is not None and num > max_valor):
                print(f"Valor deve estar entre {min_valor} e {max_valor}")
                continue
            return num
        except ValueError:
            print("Por favor, digite um número válido")

def input_data(prompt):
    """Função para input de data com validação"""
    while True:
        valor = input_com_voltar(prompt)
        if valor is None:
            return None
        
        try:
            if valor.lower() == 'hoje':
                return datetime.now().strftime("%Y-%m-%d")
            
            if not validar_data(valor):
                print("Formato de data inválido. Use yyyy-mm-dd")
                continue
            
            return valor
        except Exception:
            print("Data inválida. Use o formato yyyy-mm-dd")

def mostra_titulo(titulo):
    """Exibe um título formatado"""
    clear()
    width = min(get_terminal_width() - 4, 76)
    print("\033[92m" + center_line("╔" + "═" * width + "╗"))
    print(center_line("║" + titulo.center(width) + "║"))
    print(center_line("╚" + "═" * width + "╝") + "\033[0m\n")

def confirmacao(mensagem="Tem certeza?"):
    """Solicita confirmação do usuário"""
    print(f"\n{mensagem} (S/N)")
    return input("> ").upper() == 'S'

def exibir_ajuda():
    """Exibe informações de ajuda sobre atalhos do sistema"""
    mostra_titulo("AJUDA DO SISTEMA")
    print("Atalhos disponíveis em todo o sistema:")
    print("  'v' - Voltar ao menu anterior")
    print("  '0' - Sair do sistema")
    print("  'h' - Exibir esta ajuda")
    print("\nAtalhos para entrada de data:")
    print("  'hoje' - Usar a data atual")
    print("\nNavegação:")
    print("  Na maioria das telas, você pode pressionar 'v' para voltar")
    print("  Nas listagens, pressione qualquer tecla para continuar")
    print("\nTratamento de erros:")
    print("  O sistema valida todas as entradas para evitar problemas")
    print("  Backups automáticos são criados antes de salvar dados")
    input("\nPressione Enter para voltar...")

def show_menu():
    clear()
    print("\033[92m" + center_line("╔════════════════════════════════════════════════════╗"))
    print(center_line("║                   SISTEMA FREQUÊNCIA               ║"))
    print(center_line("╠════════════════════════════════════════════════════╣"))
    print(center_line("║  [1]   Cadastrar Turma                             ║"))
    print(center_line("║  [2]   Cadastrar Aluno                             ║"))
    print(center_line("║  [3]   Marcar Presença                             ║"))
    print(center_line("║  [4]   Consultar Frequência por Turma              ║"))
    print(center_line("║  [5]   Relatório por Aluno                         ║"))
    print(center_line("║  [6]   Listar Turmas                               ║"))
    print(center_line("║  [7]   Listar Alunos por Turma                     ║"))
    print(center_line("║  [8]   Ajuda (Atalhos e Comandos)                  ║"))
    print(center_line("║  [0]   Sair                                        ║"))
    print(center_line("╚════════════════════════════════════════════════════╝") + "\033[0m")
    print("\n" + center_line("\033[92mDigite a opção desejada:\033[0m"), end=' ')

ascii_art = """
 ██▓███    ██████▓██   ██▓▓█████▄ ▓█████  ██▀███  
▓██░  ██▒▒██    ▒ ▒██  ██▒▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒░ ▓██▄    ▒██ ██░░██   █▌▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒  ▒   ██▒ ░ ▐██▓░░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ░  ░▒██████▒▒ ░ ██▒▓░░▒████▓ ░▒████▒░██▓ ▒██▒
▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░  ██▒▒▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
░▒ ░     ░ ░▒  ░ ░▓██ ░▒░  ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
░░       ░  ░  ░  ▒ ▒ ░░   ░ ░  ░    ░     ░░   ░ 
               ░  ░ ░        ░       ░  ░   ░     
                  ░ ░      ░                      
"""

# ======================== main.py ========================
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