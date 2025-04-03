# Presença Fácil - Sistema de Controle de Frequência de Alunos

## Descrição do Projeto
O **Presença Fácil** é um sistema completo desenvolvido em Python para gerenciar a frequência de alunos em sala de aula. O sistema permite cadastrar turmas, associar alunos a essas turmas, registrar presenças e consultar relatórios de frequência de forma organizada. O armazenamento dos dados é feito em arquivos **.json**, garantindo uma estrutura leve e de fácil manipulação.

## Funcionalidades Implementadas
- Cadastro e listagem de turmas
- Cadastro e listagem de alunos vinculados a uma turma
- Registro de presença dos alunos por data
- Consulta da frequência por turma e data
- Geração de relatórios detalhados por aluno com percentual de presença

## Arquitetura do Sistema
O sistema segue uma arquitetura **em três camadas**, separando as responsabilidades conforme descrito abaixo:

### Camada de Modelo (Dados)
- Gerencia o armazenamento e recuperação dos dados em JSON.
- Implementa funções para manipular turmas, alunos e registros de frequência.

### Camada de Serviço (Lógica)
- Implementa as regras de negócio do sistema.
- Valida os dados antes de enviá-los para a camada de modelo.
- Fornece mensagens de feedback para a interface.

### Camada de Interface (Terminal)
- Apresenta o menu e opções ao usuário.
- Utiliza arte ASCII como banner.
- Coleta os inputs do usuário e os envia para processamento.

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

Os dados são salvos automaticamente em um arquivo JSON chamado **"dados_frequencia.json"** no mesmo diretório do programa.

## Contribuição
Se quiser contribuir com melhorias, sinta-se à vontade para fazer um fork do repositório e enviar um pull request.

---
**Desenvolvido por [João Guilherme]**

