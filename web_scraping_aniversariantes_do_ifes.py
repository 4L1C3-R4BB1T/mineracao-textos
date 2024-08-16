import re
import unicodedata
from bs4 import BeautifulSoup, Tag
from typing import List
from datetime import datetime
import json
import feedparser

class Scraping(object):

    def __init__(self: 'Scraping', uri: str):
       self._person_birthday: dict = {}
       self.run()

    @property
    def person_birthday(self: 'Scraping'):
        return self._person_birthday

    def run(self: 'Scraping'):
        self._person_birthday = {}
        soup = BeautifulSoup(html, "html.parser")
        elements: List[Tag] = soup.find_all('p')

        for e in elements:
            content = e.get_text(separator='\n')
            args = re.split('\n', content)

            if not len(args):
                continue

            extracted_date_info = self.get_month_and_day(args[0])

            if extracted_date_info is None:
                continue

            (day, month) = extracted_date_info

            # Verifica se existe o mês
            if not self._person_birthday.get(month.strip()):
                self._person_birthday[month] = {}

            if not self._person_birthday[month].get(int(day.strip())):
                self._person_birthday[month][day] = []

            newArgs = list(map(lambda name: name.strip(), args[1:]))
            self._person_birthday[month][day].extend(newArgs)

    def get_month_and_day(self: 'Scraping', src: str):
        assert(src != None and type(src) == str)
        pattern = r'\b(\d{1,2}).*de.*(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\b'
        match = re.search(pattern, src.strip().replace('\n', ''), re.IGNORECASE)
        return match.groups() if match else None

    def search_by_person_name(self, target_name: str):
        assert(target_name != None and type(target_name) == str)

        data = []

        for month in self.person_birthday.keys():
            person_day = self.person_birthday[month]
            for day in person_day.keys(): # Percorrendo os dias
                names = person_day[day] # Pegando os nomes

                def normalize(string: str) -> str:
                     normalized = unicodedata.normalize('NFD', string)
                     normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
                     return normalized.lower()

                def compare_name(name: str) -> bool:
                     return normalize(target_name) in normalize(name)

                name_filtered = list(filter(lambda name: compare_name(name), names)) # Filtrando pra comparar o nome

                if len(name_filtered):

                    def map_to_person(name: str):
                        return {
                            "name": name,
                            "day": day,
                            "month": month
                        }

                    data.extend([map_to_person(name) for name in name_filtered])

        return data[0] if len(data) == 1 else data

    def find_all_person_birthday(self):
        data = []

        for month in self.person_birthday.keys():
            person_day = self.person_birthday[month]
            for day in person_day.keys():

                def map_to_person(name: str):
                    return {
                        "name": name,
                        "day": day,
                        "month": month
                    }

                data.extend(list(map(map_to_person, person_day[day])))

        with open('3.4.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return data

    def get_future_person_birthday(self, person: dict, person_year: int, end_date: datetime):
        assert(person != None and end_date != None)

        datetime_from_person = datetime(
            year=person_year,
            month=self.get_month(person['month']),
            day=int(person['day']))

        next_birthday = datetime_from_person
        birthdays = []

        while next_birthday <= end_date:
            birthdays.append(next_birthday.strftime('%d/%m/%Y'))
            next_birthday = datetime(
                year=next_birthday.year + 1,
                month=next_birthday.month,
                day= next_birthday.day
            )

        return birthdays

    def has_birthday(self, day: str, month: str):
        return month in self._person_birthday and day in self._person_birthday[month]

    def get_month(self, month: str):
         match month.lower():
            case 'janeiro':
                return 1
            case 'fevereiro':
                return 2
            case 'março':
                return 3
            case 'abril':
                return 4
            case 'maio':
                return 5
            case 'junho':
                return 6
            case 'julho':
                return 7
            case 'agosto':
                return 8
            case 'setembro':
                return 9
            case 'outubro':
                return 10
            case 'novembro':
                return 11
            case 'dezembro':
                return 12
            case _:
                raise ValueError(f"Invalid Month: {month}")

URL = 'https://www.ifes.edu.br/aniversariantes?showall=1'

fp = feedparser.parse(URL)

html = fp.feed['summary']
scriping = Scraping(html)

# 3.1) Quais os nomes e as datas de aniversários?
print(scriping.find_all_person_birthday())

# 3.2) Quais as datas de aniversários dos professores da Coordenadoria de Sistemas de Informação?
names = [
    "Alexandre Romanelli",
    "Bruno Missi Xavier",
    "Claudia Fernandes Benevenute",
    "Cristiano da Silveira Colombo",
    "Cristiano Hehr Garcia",
    "Daniel José Ventorim Nunes",
    "Diego Barcelos Rodrigues",
    "Edmundo Rodrigues Junior",
    "Eliane Vasconcelos Stefaneli",
    "Eros Estevao de Moura",
    "Everson Scherrer Borges",
    "Fabielle Castelan Marques",
    "Flavio Izo",
    "Glaice Kelly da Silva Quirino Monfardini",
    "João Paulo de Brito Gonçalves",
    "Messias Yazegy Perim",
    "Rafael Silva Guimarães",
    "Rafael Vargas Mesquita dos Santos",
    "Raul de Souza Brandão",
    "Ricardo Maroquio Bernardo"
]

# Lista os professores da Coordenadoria de Sistemas de Informação
for name in names:
    print()
    print(f'Pesquisando por professor com nome {name}')
    person = scriping.search_by_person_name(name)
    if not person:
        print('Não há nenhum professor com esse nome.')
        print()
        continue
    print(person)

# 3.3) Quais são as próximas datas de aniversário de professores da Coordenadoria de Sistemas de Informação até 01/05/2025?
end_date = datetime(year=2025, month=5, day=1)

for name in names:
    print()
    print(f'Pesquisando por professor com nome {name}')
    person = scriping.search_by_person_name(name)
    if not person:
        print('Não há nenhum professor com esse nome.')
        print()
        continue
    person_birthdays = scriping.get_future_person_birthday(person, 2024, end_date)

    print(person_birthdays)

# 3.4) Em quais datas os servidores a seguir fazem aniversário?
names = [
    "Filipe",
    "Aldemon",
    "Asdrubal"
]

for name in names:
    print(scriping.search_by_person_name(name))

# 3.5) Foram encontradas ocorrências de aniversário em todos os dias do ano? Se não, em qual(is) data(s) não têm aniversariantes?
days_per_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

months = {
    1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
    5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto', 9: 'setembro',
    10: 'outubro', 11: 'novembro', 12: 'dezembro'
}

# Percorrer mês
print('Há dias sem aniversário?')
for month in range(1, 13):
    # Percorrer os dias do mês
    for day in range(1, days_per_months[month - 1] + 1):
        if not scriping.has_birthday(str(day), months.get(month)):
          print(f"{day:02d}/{month:02d}")