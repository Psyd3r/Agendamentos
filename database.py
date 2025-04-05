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
        
             return {"turmas": [], "alunos": [], "presencas": []}

def save_data(data):
    try:
        
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