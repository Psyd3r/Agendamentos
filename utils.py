import time
import sys
import random
import shutil
import os

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
