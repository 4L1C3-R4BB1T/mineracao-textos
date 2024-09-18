import re
import os
import random
from collections import Counter, defaultdict
from typing import List
import nltk
from nltk import pos_tag, ne_chunk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import ngrams
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob

nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('words')

stopwords = set(stopwords.words('portuguese'))


file_path = os.path.join(os.getcwd(), 'doril.txt');

if not os.path.isfile(file_path):
  raise FileNotFoundError('Arquivo não encontrado.')

with open(file_path, 'r', encoding='utf-8') as file:
  text = file.read()

"""### Imprima as primeiras sentenças (frases)

Nesta tarefa, sua equipe deve imprimir as primeiras 20 sentenças (frases) do texto. Isso permite uma visão inicial do conteúdo e formato dos dados de texto.
"""

sentences = sent_tokenize(text, language='portuguese')

for i, sentence in enumerate(sentences[:20], 1):
  print(f"Sentença {i}: {sentence}\n")

"""### Imprima sentenças (frases) aleatórias
Nesta tarefa, sua equipe deve imprimir sentenças (frases) aleatórias do texto. Esta ação auxilia na leitura mais representativa e pode ajudar a descobrir possíveis variações no texto.



"""

sentences = sent_tokenize(text, language='portuguese')

random_sentences = random.sample(sentences, 10) # dez sentencas aleatorias

for i, sentence in enumerate(random_sentences, start=1):
  print(f"Sentença {i}: {sentence}\n")

"""### Realizar a análise de estrutura do texto
Nesta tarefa, sua equipe deve conhecer a estrutura do texto. Pode ser que existam títulos, subtítulos ou formatação especial (por exemplo, tags HTML) que não foram abordados durante o pré-processamento.
"""

def analyze_text_structure(text: str) -> dict:
  lines = text.split('\n')
  output = {
    'titles': [],
    'subtitles': [],
    'especials': [],
  }

  for index, line in enumerate(lines):
    line = re.sub(r'[\r\n]+', ' ', line).strip()
    ends_characteres = ['?', '!', '.']

    if (index + 1) < len(lines):
      next_line = lines[index + 1]
      if next_line.isupper() and next_line.endswith(tuple(ends_characteres)) and not re.match(r'[IV\d]+', next_line):
        line += ' ' + next_line

    if re.match(r'^(([IV]+)\s[®A-ZÀÁÂÃÇÈÉÊÌÍÎÒÓÔÕÙÚÛÝŸ:.,\s–-]+$)|(^[®A-Z]+$)', line):
      output['titles'].append(line)

    elif re.match(r'^([0-9]+\.)[A-ZÀÁÂÃÇÈÉÊÌÍÎÒÓÔÕÙÚÛÝŸ˃:.,\s–?-]+$', line):
      output['subtitles'].append(line)

    else:
      if re.match(r'<\s*[^>]*>', line):
        output['especials'].append(line)

  return output


output = analyze_text_structure(text)

print('\n' + '-'*5 + ' Títulos ' + '-'*5 + '\n')
for title in output['titles']:
  print(title)

print('\n' + '-'*5 + ' Subtítulos ' + '-'*5 + '\n')
for subtitle in output['subtitles']:
  print(subtitle)

print('\n' + '-'*5 + ' Especiais ' + '-'*5)
for especial in output['especials']:
  print(especial)

"""### Conhecer os tipos de dados presentes no texto
Nesta tarefa, sua equipe deve investigar os tipos de dados presentes no dataset. Pode ser que além do texto, existam metadados ou rótulos associados ao texto que precisam ser considerados.
"""

# # ainda nao conseguimos fazer
# # Vamos pegar padrões que contém ou, e e informações dentro de parênteses, ok?
# chosen_patterns = [
#     'ou',
#     '+',
#     # tem q ajustar ç.ç
#     re.compile(r'\b\([a-zàáâãäçèéêëìíîïòóôõöùúûüýÿ\s,-]+\)', re.IGNORECASE | re.MULTILINE)
# ]


# dataset = text.split('\n')

# for data in dataset:
#     if any((pattern in data if isinstance(pattern, str) else re.search(pattern, data)) for pattern in chosen_patterns):
#         print(data, end='\n\n')

"""### Realizar a contagem de caracteres
Nesta tarefa, sua equipe vai contar o número de caracteres do seu dataset. Tal medida auxilia na avaliação da complexidade do texto.
"""

words = word_tokenize(text, language='portuguese')

total_caracters = 0

for word in words:
  total_caracters += len(word)

print(f'Número de caracteres: {total_caracters}')

"""### Efetuar a contagem de palavras
Nesta tarefa, sua equipe vai calcular o número de palavras do seu dataset. Esta métrica auxilia na compreensão do comprimento geral do dataset.
"""

words = word_tokenize(text, language='portuguese')
words = [word for word in words if word.isalnum()]

qtt_words = len(words)

print(f'Número de palavras: {qtt_words}')

"""### Determinar o comprimento médio das palavras
Nesta tarefa, sua equipe vai investigar comprimento médio das palavras, pois tal informação pode prover insights sobre a complexidade do vocabulário.
"""

words = word_tokenize(text, language='portuguese')
words = [word for word in words if word.isalnum()]

total_caracters = 0

for word in words:
  total_caracters += len(word)

qtt_words = len(words)

print(f'Comprimento médio das palavras: {(total_caracters/qtt_words):.2f}')

"""### Fazer a contagem de sentenças (frases)
Nesta tarefa, sua equipe vai descobrir o número de frases do seu dataset. Esta informação revela insights sobre a estrutura do texto.
"""

sentences = sent_tokenize(text, language='portuguese')

print("Número de frases:", len(sentences))

"""### Tokenizar as palavras
Nesta tarefa, sua equipe deve dividir o texto em palavras "separadas".
"""

words = word_tokenize(text, language='portuguese')
words = [word for word in words if word.isalnum()]

for word in words:
  print(word)

"""### Identificar tokens únicos (exclusivos)
Nesta tarefa, sua equipe deve identificar e contar o número de tokens únicos (exclusivos) do dataset. Tal informação auxilia na avaliação da riqueza do vocabulário.
"""

lines = text.split('\n')
tokenize_words = []

for line in lines:
  words = [word.lower() for word in re.sub(r'[^\w\s]', ' ', line).split() if word.strip() != '']
  tokenize_words.extend(words)

occurrence = Counter(tokenize_words)
unique_tokens = list(map(lambda target: target[0], filter(lambda item: item[1] == 1, occurrence.items())))

print("Número de tokens únicos:", len(unique_tokens))
print(unique_tokens)

"""### Tokenizar as sentenças (frases)
Nesta tarefa, sua equipe deve dividir o texto em sentenças "separadas".
"""

sentences = sent_tokenize(text, language='portuguese')

for i, sentence in enumerate(sentences, start=1):
    print(f"Sentença {i}: {sentence}\n")

"""### Plotar um histograma de frequência de palavras
Nesta tarefa, sua equipe deve plotar um histograma de frequência de palavras para auxiliar na compreensão da distribuição de ocorrências de termos. Este gráfico pode ajudar a identificar termos raros ou comuns.
"""

words = word_tokenize(text, language='portuguese')
words = [word for word in words if word.isalnum()]
no_stopwords_text = [word.lower() for word in words if not word.lower() in stopwords]

freq_dist = FreqDist(no_stopwords_text)
freq_dist.plot(30, title='Histograma de Frequência', cumulative=False) # 30 palavras mais comuns

"""### Gerar nuvem de palavras
Nesta tarefa, sua equipe deve gerar nuvem de palavras para visualizar os termos mais frequentes em seu dataset. As nuvens de palavras são eficazes para identificar rapidamente palavras ou temas importantes.
"""

words = word_tokenize(text, language='portuguese')
words = [word for word in words if word.isalnum()]
no_stopwords_text = [word.lower() for word in words if not word.lower() in stopwords]

clean_text = ' '.join(no_stopwords_text)

cloud = WordCloud(width=800, height=400, background_color='white').generate(clean_text)

plt.figure(figsize=(10, 5))
plt.imshow(cloud, interpolation='bilinear')
plt.axis('off')
plt.show()

"""### Apresentar a distribuição de tags POS
Nesta tarefa, sua equipe vai apresentar a distribuição de tags POS (substantivos, verbos, adjetivos) em seus dados de texto para compreender a sua estrutura gramatical.

A tarefa de Part-of-speech (POS) é importante em NLP pois rotula palavras em uma frase com suas tags POS correspondentes. As tags POS indicam a categoria gramatical de uma palavra, como substantivo, verbo, adjetivo, advérbio, etc. O objetivo da marcação POS é determinar a estrutura sintática de uma frase e identificar a função de cada palavra na frase.
"""

words = word_tokenize(text, language='portuguese')
words = [word for word in words if word.isalnum()]
no_stopwords_text = [word.lower() for word in words if not word.lower() in stopwords]

tags = pos_tag(no_stopwords_text)
tags_pos = [tag for word, tag in tags]
tag_counts = Counter(tags_pos)

plt.figure(figsize=(10, 5))
plt.bar(tag_counts.keys(), tag_counts.values())
plt.title('Distribuição de Tags POS')
plt.xlabel('Tag POS')
plt.ylabel('Frequência')
plt.show()

"""### Investigar sobre n-gramas
Nesta tarefa, sua equipe deve investigar sobre n-gramas e apresentar os n-gramas, bi-gramas e tri-gramas presentes no dataset.

Mas antes, vamos conceituar o que é n-grams.

Em NLP, n-gramas são uma sequência contígua de n itens de uma determinada amostra de texto. Tais itens podem ser caracteres, palavras ou outras unidades de texto e são usados ​​para analisar a frequência e distribuição de padrões linguísticos em uma determinada amostra.

Exemplos típicos de n-gramas são bi-gramas (2-gramas) e tri-gramas (3-gramas), que capturam sequências de palavras. Por exemplo, “processamento de linguagem natural” poderia produzir bi-gramas como [(“processamento”, “de”), (“de”, “linguagem”), (“linguagem”, “natural”)].
"""

words = word_tokenize(text, language='portuguese')
words = [word for word in words if word.isalnum()]
no_stopwords_text = [word.lower() for word in words if not word.lower() in stopwords]

n_gramas = Counter(ngrams(no_stopwords_text, 1))
bi_gramas = Counter(ngrams(no_stopwords_text, 2))
tri_gramas = Counter(ngrams(no_stopwords_text, 3))

print('UNIGRAMAS: ')
for ngrama, contagem in n_gramas.most_common(10):
  print(f"{' '.join(ngrama)}: {contagem}")

print('\nBIGRAMAS: ')
for ngrama, contagem in bi_gramas.most_common(10):
  print(f"{' '.join(ngrama)}: {contagem}")

print('\nTRIGRAMAS: ')
for ngrama, contagem in tri_gramas.most_common(10):
  print(f"{' '.join(ngrama)}: {contagem}")

"""### Plote gráficos de bi-gramas e tri-gramas
Nesta tarefa, sua equipe deve plotar 2 gráficos, um de bi-gramas e outro de tri-gramas presentes no dataset. Os gráficos vão auxiliar na compreensão dos padrões de coocorrência de termos nos dados de texto.

Dica: Os gráficos do tipo mapa de calor (heatmap), podem ser úteis nesta tarefa.
"""

words = word_tokenize(text, language='portuguese')
words = [word for word in words if word.isalnum()]
no_stopwords_text = [word.lower() for word in words if not word.lower() in stopwords]

n_gramas = Counter(ngrams(no_stopwords_text, 1))
bi_gramas = Counter(ngrams(no_stopwords_text, 2))
tri_gramas = Counter(ngrams(no_stopwords_text, 3))

def plot_ngramas(ngramas, title):
  ngramas, contagens = zip(*ngramas.most_common(10))
  ngramas = [' '.join(ngr) for ngr in ngramas]
  plt.figure(figsize=(10, 5))
  plt.barh(ngramas, contagens)
  plt.title(title)
  plt.xlabel('Frequência')
  plt.gca().invert_yaxis()
  plt.show()

plot_ngramas(bi_gramas, "Distribuição de Bigramas")
plot_ngramas(tri_gramas, "Distribuição de Trigramas")

"""### Plote a distribuição de sentimentos do texto
Nesta tarefa, sua equipe deve plotar a distribuição dos sentimentos presentes no dataset. Use um histograma para demonstrar a polaridade de sentimentos do texto (positiva, negativa, neutra).
"""

sentences = sent_tokenize(text, language='portuguese')

polarities = []

for sentence in sentences:
    blob = TextBlob(sentence)
    polarity = blob.sentiment.polarity
    polarities.append(polarity)

positive = [polarity for polarity in polarities if polarity > 0]
neutral = [polarity for polarity in polarities if polarity == 0]
negative = [polarity for polarity in polarities if polarity < 0]

plt.figure(figsize=(10, 6))
plt.hist([negative, neutral, positive], bins=3, color=['red', 'gray', 'green'], label=['Negativo', 'Neutro', 'Positivo'])
plt.title('Distribuição de Sentimentos')
plt.xlabel('Polaridade')
plt.ylabel('Frequência')
plt.legend()
plt.show()

"""### Reconheça as entidades nomeadas
Nesta tarefa, sua equipe deve apresentar os rótulos de entidades nomeadas presentes no dataset (pessoas, organizações, locais). Isto auxilia na identificação de entidades de interesse ou padrões.
"""

entities = defaultdict(list)

words = word_tokenize(text, language='portuguese')

tags = pos_tag(words)
chunks = ne_chunk(tags)

for chunk in chunks:
  if isinstance(chunk, nltk.Tree):
    entity = ' '.join(c[0] for c in chunk.leaves())
    if chunk.label() == 'PERSON':
      entities['PESSOA'].append(entity)
    elif chunk.label() == 'ORGANIZATION':
      entities['ORGANIZAÇÃO'].append(entity)
    elif chunk.label() == 'GPE':
      entities['LOCAL'].append(entity)

entities_count = {k: Counter(v) for k, v in entities.items()}

for entity_type, count in entities_count.items():
  print(f'\n----- {entity_type} -----')
  for entity in count:
    print(entity)