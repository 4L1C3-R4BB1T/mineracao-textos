"""
2) O arquivo exercicio-2.json contém notícias extraídas do site https://feeds folha.uol.com.br/esporte/rss091.xml, apresentado em sala de aula na atividade sobre web scraping.**

Faça o pré-processamento deste arquivo. É necessário que, após o pré-processamento, cada notícia seja copiada num arquivo próprio no formato .txt. Os nomes destes arquivos deve obedecer uma ordem numérica sequencial: feed-001.txt, feed-002.txt, e assim por diante.
"""

import json

# importar o arquivo antes
# lendo o arquivo
with open('exercicio-2.json', 'r', encoding='utf-8') as file:
    news_json = json.load(file)

# salvando cada noticia em um arquivo
for i, news in enumerate(news_json, start=1):
  with open(f'feed-{i:03d}.txt', 'w', encoding='utf-8') as news_file:
    news_file.write(f"TITULO\n{news['title']}\n\n")
    news_file.write(f"RESUMO\n{news['summary']}\n\n")
    news_file.write(f"LINK\n{news['link']}\n")