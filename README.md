# Presença Fácil - Sistema de Controle de Frequência de Alunos

## Descrição do Projeto
O **Presença Fácil** é um sistema simples desenvolvido em Python para gerenciar a frequência de alunos em sala de aula. O sistema permite cadastrar turmas, associar alunos a essas turmas, registrar presenças e consultar relatórios de frequência de forma organizada. O armazenamento dos dados é feito em arquivos **.json**, garantindo uma estrutura leve e de fácil manipulação.

## Funcionalidades Implementadas
- Cadastro de turmas
- Cadastro de alunos vinculados a uma turma
- Registro de presença por data
- Consulta da frequência por turma e data
- Geração de relatórios de presença por aluno

## Arquitetura do Sistema
O sistema segue uma arquitetura **Camada MVC (Model-View-Controller)** simplificada, separando as responsabilidades conforme descrito abaixo:
- **Model (Modelo)**: Gerencia os dados e interage com os arquivos JSON.
- **View (Visão)**: Interface baseada no terminal para interação do usuário.
- **Controller (Controlador)**: Gerencia a lógica da aplicação, recebendo comandos do usuário e manipulando os dados conforme necessário.

### Tecnologias Utilizadas
- **Linguagem**: Python 3.x
- **Armazenamento**: Arquivos JSON para persistência dos dados
- **Bibliotecas**:
  - `json`: Manipulação dos arquivos JSON
  - `os`: Gerenciamento de arquivos e diretórios
  - `datetime`: Registro de datas de presença

## Requisitos Mínimos de Hardware
- Processador: Dual-core 1.6 GHz ou superior
- Memória RAM: 2 GB
- Espaço em disco: 100 MB

## Como Executar o Projeto
1. Instale o Python 3.x no seu sistema (caso ainda não tenha instalado).
2. Clone este repositório ou baixe os arquivos.
3. No terminal, navegue até o diretório do projeto.
4. Execute o comando:
   ```bash
   python main.py
   ```
5. Siga as instruções no terminal para interagir com o sistema.

## Contribuição
Se quiser contribuir com melhorias, sinta-se à vontade para fazer um fork do repositório e enviar um pull request.

---
**Desenvolvido por [Seu Nome]**

