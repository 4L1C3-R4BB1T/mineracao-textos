import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

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

# juntas todas as palavras do array
' '.join(texto_sem_stopwords)

"""# **Remover sinais de pontuação**"""

# compara cada palavra do texto pra ver se e um sinal de pontuacao
texto_sem_pontuacao = [palavra for palavra in palavras if not palavra in string.punctuation]

# utilizando o regex do nltk (exclui os emojis)
# tokenizer = RegexpTokenizer(r'\w+')
# texto_sem_pontuacao = tokenizer.tokenize(tribuna)

' '.join(texto_sem_pontuacao)

"""# **Remover caracteres especiais (exceto emoji)**"""

# compara cada palavra do texto pra ver se e um caractere especial
texto_sem_caracteres_especiais = [re.sub(r'[^\w\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F]', '', palavra) for palavra in palavras]

' '.join(texto_sem_caracteres_especiais)

"""# **Aplicar stemização**"""

stemmer = PorterStemmer()

texto_com_stemizacao = [stemmer.stem(palavra) for palavra in palavras]

' '.join(texto_com_stemizacao)

"""# **Aplicar lematização**"""

lemmatizer = WordNetLemmatizer()

texto_com_lematizacao = [lemmatizer.lemmatize(palavra) for palavra in palavras]

' '.join(texto_com_lematizacao)