# importar o arquivo a ser lido
# !pip install num2words
# !pip install pyspellchecker
from enum import Enum
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
# from num2words import num2words
from spellchecker import SpellChecker

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# pega as stopwords em portugues
stopwords = set(stopwords.words('portuguese'))

# le o conteudo do arquivo
with open('no14011801.txt', 'r', encoding='utf-8') as texto:
    tribuna = texto.read()

# retorna o array com as palavras do texto
palavras = word_tokenize(tribuna)

"""# **Remover stopwords**"""

# compara cada palavra do texto pra ver se e uma stopword
texto_sem_stopwords = [palavra for palavra in palavras if not palavra.lower() in stopwords]

print(' '.join(texto_sem_stopwords))

"""# **Remover sinais de pontuação**"""

# compara cada palavra do texto pra ver se e um sinal de pontuacao
texto_sem_pontuacao = [palavra for palavra in palavras if not palavra in string.punctuation]

print(' '.join(texto_sem_pontuacao))

# utilizando o regex do nltk
# tokenizer = RegexpTokenizer(r'\w+')
# texto_sem_pontuacao = tokenizer.tokenize(tribuna)

"""# **Remover caracteres especiais (exceto emoji)**"""

# compara cada palavra do texto pra ver se e um caractere especial
texto_sem_caracteres_especiais = [re.sub(r'[^\w\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F]', '', palavra) for palavra in palavras]

print(' '.join(texto_sem_caracteres_especiais))

"""# **Aplicar stemização**"""

stemmer = PorterStemmer()
texto_com_stemizacao = [stemmer.stem(palavra) for palavra in palavras]

print(' '.join(texto_com_stemizacao))

"""# **Aplicar lematização**"""

lemmatizer = WordNetLemmatizer()
texto_com_lematizacao = [lemmatizer.lemmatize(palavra) for palavra in palavras]

print(' '.join(texto_com_lematizacao))

class ClearStrategy(Enum):
    HTML = 0
    URL = 1
    EMOJI = 2
    SPACES = 3

def clear_string(strategy: ClearStrategy):
    def decorator(fnc: callable):
        def wrapper(*args, **kwargs):
            if len(args) != 1:
                raise Exception('The function decorated must accept exactly one argument.')

            target_value: str = args[0]

            if not isinstance(target_value, str):
                raise ValueError('The argument must be a string.')

            if ClearStrategy.HTML == strategy:
                soup = BeautifulSoup(target_value, "html.parser")
                target_value = soup.get_text()

            if ClearStrategy.URL == strategy:
                target_value = re.sub(r'https?://(?:www\.)?\S+|www\.\S+', '', target_value)

            if ClearStrategy.EMOJI == strategy:
                emoji_pattern = (
                      r'['
                      r'\U0001F600-\U0001F64F'
                      r'\U0001F300-\U0001F5FF'
                      r'\U0001F680-\U0001F6FF'
                      r'\U0001F1E0-\U0001F1FF'
                      r'\U00002600-\U000026FF'
                      r'\U00002700-\U000027BF'
                      r'\U0001F900-\U0001F9FF'
                      r'\U0001FA70-\U0001FAFF'
                      r']'
                  )
                target_value = re.sub(emoji_pattern, '', target_value, re.UNICODE)

            if ClearStrategy.SPACES == strategy:
                target_value = re.sub(r'\s{2,}', ' ', target_value)

            return fnc(target_value)
        return wrapper
    return decorator

@clear_string(ClearStrategy.HTML)
def print_html(html: str) -> None:
  print(html, end='\n\n')

@clear_string(ClearStrategy.EMOJI)
def print_emoji(emoji: str) -> None:
  print(emoji, end='\n\n')

@clear_string(ClearStrategy.URL)
def print_url(url: str) -> None:
  print(url, end='\n\n')

@clear_string(ClearStrategy.SPACES)
def print_space(space: str) -> None:
  print(space, end='\n\n')

"""# **Remover tags HTML**"""

print('## Limpando HTML')
print_html(tribuna)

"""# **Remover as URLs**"""

print('## Limpando URLs')
print_url(tribuna)

"""# **Remover emojis**"""

print('## Limpando Emojis')
print_emoji(tribuna)

"""# **Remover espaços em branco excedentes**"""

print('## Limpando espaços em branco')
print_space(tribuna)

"""# **Substituir palavras usadas em chat em palavras normais**"""

def get_matching_word(word: str) -> str:
    dataset = {
        'pqp': 'puta que paril',
        'tchau': 'adeus',
        'bjs': 'beijos',
        'wtf': 'what the fuck',
        'gg': 'good game',
        'tmj': 'estamos juntos',
        'glr': 'galera',
        'pfv': 'por favor',
        'vcs': 'vocês',
        'obg': 'obrigado',
        'vc': 'você',
        'tbm': 'também',
        'vdd': 'verdade',
    }

    normal_word = dataset.get(word.strip())
    return normal_word if normal_word is not None else word

bad_words  = ['pqp', 'ontem', 'eu', 'disse', 'bjs', 'pra', 'ela', 'e', 'ela', 'disse', 'gg', 'tmj']
print(list(map(get_matching_word, bad_words)))

# substituir = word_tokenize('Olá galera! Por favor vocês estão em casa?')
# texto_substituido = [get_matching_word(palavra) for palavra in substituir]
# print(' '.join(texto_substituido))

"""# **Fazer a correção ortográfica**"""

spell = SpellChecker(language='pt')

texto = word_tokenize('Eu nao arcredito que issu esta aconteçendo. Espero que você nao perca esta oprtunidade')
texto_corrigido = [spell.correction(palavra) for palavra in texto]

print(' '.join(texto_corrigido))

"""# **Converter números em palavras**"""

# converter = word_tokenize('3 da manhã o alarme tocou e vi 2 assaltantes fugindo')
# texto_convertido = [num2words(palavra, lang='pt_BR') if palavra.isdigit() else palavra for palavra in converter]
# print(' '.join(texto_convertido))

# Converter números em palavras
numeros = {
    1: "um", 2: "dois", 3: "três", 4: "quatro", 5: "cinco",
    6: "seis", 7: "sete", 8: "oito", 9: "nove", 10: "dez",
    11: "onze", 12: "doze", 13: "treze", 14: "quatorze", 15: "quinze",
    16: "dezesseis", 17: "dezessete", 18: "dezoito", 19: "dezenove", 20: "vinte",
    21: "vinte e um", 22: "vinte e dois", 23: "vinte e três", 24: "vinte e quatro", 25: "vinte e cinco",
    26: "vinte e seis", 27: "vinte e sete", 28: "vinte e oito", 29: "vinte e nove", 30: "trinta",
    31: "trinta e um", 32: "trinta e dois", 33: "trinta e três", 34: "trinta e quatro", 35: "trinta e cinco",
    36: "trinta e seis", 37: "trinta e sete", 38: "trinta e oito", 39: "trinta e nove", 40: "quarenta",
    41: "quarenta e um", 42: "quarenta e dois", 43: "quarenta e três", 44: "quarenta e quatro", 45: "quarenta e cinco",
    46: "quarenta e seis", 47: "quarenta e sete", 48: "quarenta e oito", 49: "quarenta e nove", 50: "cinquenta",
    51: "cinquenta e um", 52: "cinquenta e dois", 53: "cinquenta e três", 54: "cinquenta e quatro", 55: "cinquenta e cinco",
    56: "cinquenta e seis", 57: "cinquenta e sete", 58: "cinquenta e oito", 59: "cinquenta e nove", 60: "sessenta",
    61: "sessenta e um", 62: "sessenta e dois", 63: "sessenta e três", 64: "sessenta e quatro", 65: "sessenta e cinco",
    66: "sessenta e seis", 67: "sessenta e sete", 68: "sessenta e oito", 69: "sessenta e nove", 70: "setenta",
    71: "setenta e um", 72: "setenta e dois", 73: "setenta e três", 74: "setenta e quatro", 75: "setenta e cinco",
    76: "setenta e seis", 77: "setenta e sete", 78: "setenta e oito", 79: "setenta e nove", 80: "oitenta",
    81: "oitenta e um", 82: "oitenta e dois", 83: "oitenta e três", 84: "oitenta e quatro", 85: "oitenta e cinco",
    86: "oitenta e seis", 87: "oitenta e sete", 88: "oitenta e oito", 89: "oitenta e nove", 90: "noventa",
    91: "noventa e um", 92: "noventa e dois", 93: "noventa e três", 94: "noventa e quatro", 95: "noventa e cinco",
    96: "noventa e seis", 97: "noventa e sete", 98: "noventa e oito", 99: "noventa e nove", 100: "cem"
}

def map_word_to_number(word: str) -> str:
    if word.isdigit():
        return numeros.get(int(word), word)
    else:
      return word

print(' '.join(map(map_word_to_number, "3 da manhã o alarme tocou e vi 2 assaltantes fugindo.".split(' '))))

"""# **Converter o texto para letras minúsculas**"""

# texto_minusculo = [palavra.lower() for palavra in palavras]
# print(' '.join(texto_minusculo))

# Converter pra minúsculo
def to_lowercase(target: str):
    for char in target:
      if 'A' <= char <= 'Z':
        yield chr(ord(char) + 32)
      else:
        yield char

for word in to_lowercase(tribuna):
  print(word, end='')