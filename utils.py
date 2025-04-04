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