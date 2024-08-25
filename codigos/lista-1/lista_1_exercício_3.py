"""
3) O arquivo exercicio-3.txt contém perguntas e respostas de um simulado para vestibulares, publicado no caderno Cidades do jornal A Tribuna em 19/10/2006.**

Faça o pré-processamento deste arquivo. Feito isso, copie cada questão (pergunta e resposta) para um arquivo próprio no formato .txt. Os nomes destes arquivos deve obedecer uma ordem numérica sequencial: questao-001.txt, questao-002.txt, e assim por diante.

Não se esqueça de criar um arquivo para as respostas das questões.
"""

import re

# importar o arquivo antes
# lendo o arquivo
with open('exercicio-3.txt', 'r', encoding='latin-1') as file:
  content = file.readlines()

question_regex = re.compile(r'^\d+\.')
answers_regex = re.compile(r'^RESPOSTAS$')

# lista para armazenar questões
questions = []
current_question = ""

# variavel para identificar se esta dentro de uma questão
is_question = False
is_answers = False

# ler cada linha do arquivo
for line in content:
  # se e uma linha de inicio de questao
  if question_regex.match(line):
    # porcao de texto lida antes de chegar no regex
    if is_question:
      # adicionar questao a lista
      questions.append(current_question.strip())
      current_question = ""

    # porcao de texto atual
    current_question += line
    is_question = True  # marcar que e questao
    is_answers = False

  # se e a linha de inicio das respostas
  elif answers_regex.match(line):
    # porcao de texto lida antes de chegar no regex
    if is_question:
      # adicionar questao atual a lista
      questions.append(current_question.strip())
      current_question = ""

    # porcao de texto atual
    current_question += line
    is_question = False
    is_answers = True  # marcar que e resposta

  # pra nao pegar a porcao de texto antes de iniciar a questao 1
  elif is_question or is_answers:
    current_question += line


# respostas
# ultima porcao de texto lida
if is_answers:
  answers = current_question.strip()


# contador de questoes
count = 1

# salvando cada questao em um arquivo
for i, question in enumerate(questions, start=1):
  # previnir que a questao 16 quebre em duas com o regex usado
  if (i == 17):
    # salvando no arquivo
    with open(f'questao-016.txt', 'a', encoding='utf-8') as question_16:
      question_16.write(question)
    # contador
    count = count - 1
  # demais questoes
  else:
    # salvando no arquivo
    with open(f'questao-{count:03d}.txt', 'w', encoding='utf-8') as question_file:
      question_file.write(question)
  # contador
  count = count + 1


# salvando as respostas no arquivo
with open(f'respostas.txt', 'w', encoding='utf-8') as answer_file:
  # retirar a parte fontes
  clean_answers = re.sub(r'Fonte:.*', '', answers, flags=re.DOTALL).strip()
  answer_file.write(clean_answers)