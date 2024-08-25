"""
1) O arquivo exercicio-1.txt contém o texto da 1a Carta de Paulo aos Gálatas.**

Faça o pré-processamento deste arquivo de modo que cada sentença do texto fique em linhas distintas. É importante que se tenha uma linha em branco separando cada uma das sentenças. Ao final do pré-processamento é preciso que se tenha 2 arquivos: exercicio-1.txt (original) e exercicio-1-sentencas.txt (criado por você).
"""

import re

# importar o arquivo antes
# lendo o arquivo
with open('exercicio-1.txt', 'r', encoding='latin-1') as file:
        text = file.read()

# cada sentenca comeca com um numero e termina com uma quebra de linha
sentences = re.findall(r'\d+.*?(?=\n|$)', text.strip(), re.DOTALL)

# escrevendo o arquivo com as sentencas
with open('exercicio-1-sentencas.txt', 'w', encoding='utf-8') as sentences_file:
    for sentence in sentences:
        sentences_file.write(sentence.strip() + '\n\n')