import json
from abc import ABC, abstractmethod
import requests
import os


class API(ABC):

    @abstractmethod
    def get_vacancies(self, keyword, quantity):
        pass


class HeadHunterAPI(API):

    def get_vacancies(self, keyword, quantity):
        url_hh = 'https://api.hh.ru/vacancies'
        vacancies_hh = requests.get(url_hh, params={'text': keyword, 'currency': 'RUR', 'host': 'hh.ru'}).json()
        vacancy = {}
        for i in range(0, quantity):
            try:
                vac = {
                    'name': vacancies_hh['items'][i]['name'],
                    'payment_to': vacancies_hh['items'][i]['salary']['to'],
                    'payment_from': vacancies_hh['items'][i]['salary']['from'],
                    'town': vacancies_hh['items'][i]['area']['name'],
                    'requirement': vacancies_hh['items'][i]['snippet']['requirement']
                }
            except TypeError:
                vac = {
                    'name': vacancies_hh['items'][i]['name'],
                    'payment_to': 0,
                    'payment_from': 0,
                    'town': vacancies_hh['items'][i]['area']['name'],
                    'requirement': vacancies_hh['items'][i]['snippet']['requirement']
                }
            except IndexError:
                print('По ключевому слову не найдено вакансий')
            vacancy[vacancies_hh['items'][i]['id']] = vac
        return vacancy


class SuperJobAPI(API):

    def get_vacancies(self, keyword, quantity):
        secret_key = {'X-Api-App-Id': os.getenv('SJ-API-KEY')}
        url_sj = 'https://api.superjob.ru/2.0/vacancies/'
        vacancies_sj = requests.get(url_sj, headers=secret_key, params={'keyword': str(keyword)}).json()
        vacancy = {}
        for i in range(0, quantity):
            try:
                vac = {
                    'name': vacancies_sj['objects'][i]['profession'],
                    'payment_to': vacancies_sj['objects'][i]['payment_to'],
                    'payment_from': vacancies_sj['objects'][i]['payment_from'],
                    'town': vacancies_sj['objects'][i]['town']['title'],
                    'requirement': vacancies_sj['objects'][i]['candidat']
                }
            except TypeError:
                vac = {
                    'name': vacancies_sj['objects'][i]['profession'],
                    'payment_to': 0,
                    'payment_from': 0,
                    'town': vacancies_sj['objects'][i]['town']['title'],
                    'requirement': vacancies_sj['objects'][i]['candidat']
                }
            except IndexError:
                print('По ключевому слову не найдено вакансий')
            vacancy[vacancies_sj['objects'][i]['id']] = vac
        return vacancy


class Vacancy:

    def __init__(self, name=None, payment_from=0, payment_to=0, town=None, requirement=None):
        self.name = name
        try:
            self.payment_to: int = int(payment_to)
            self.payment_from: int = int(payment_from)
        except TypeError:
            print('Введите зарплату цифрами')
        self.town = town
        self.requirement = requirement
        if self.payment_to is None and self.payment_from is None:
            self.salary = 0
        elif self.payment_from is None:
            self.salary = self.payment_to
        elif self.payment_to is None:
            self.salary = self.payment_from
        else:
            self.salary = (self.payment_from + self.payment_to) / 2

    def __lt__(self, other):
        return self.salary < other.salary

    def __str__(self):
        return f'''Название вакансии: {self.name}
Средняя зарплата: {int(self.salary)}
Город: {self.town}
Описание: {self.requirement[0:100]}'''


class JSONSave(ABC):

    @abstractmethod
    def to_json(self, getted_vac):
        pass

    @abstractmethod
    def add_vacancy(self, getted_vac):
        pass

    @abstractmethod
    def delete_vacancy(self, getted_vac):
        pass


class JSONSaver(JSONSave):

    def __init__(self, file='saved_vacancies.json'):
        self.file = file


    def to_json(self, getted_vac):
        with open(os.path.abspath(self.file), 'w', encoding='utf=8') as f:
            json.dump(getted_vac, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, getted_vac):
        getted_vac = json.dumps(getted_vac)
        getted_vac = json.loads(str(getted_vac))
        b = json.load(open(os.path.abspath(self.file), 'r', encoding='utf=8'))
        for key, items in getted_vac.items():
            b[key] = items
        json.dump(b, open(os.path.abspath(self.file), 'w', encoding='utf=8'), ensure_ascii=False, indent=2)

    def read_vacancy(self):
        b = json.load(open(os.path.abspath(self.file), 'r', encoding='utf=8'))
        vacancies_list = []
        for key,item in b.items():
            vacancies_list.append(Vacancy(item['name'], int(item['payment_to']), int(item['payment_from']), item['town'], item['requirement']))
        return vacancies_list

    def delete_vacancy(self, del_vac):
        try:
            del_vac = json.dumps(del_vac.__dict__)
            del_vac = json.loads(str(del_vac))
            name = del_vac['name']
            payment_from = del_vac['town']
        except AttributeError:
            name = del_vac['name']
            payment_from = del_vac['town']
        b = json.load(open(os.path.abspath(self.file), 'r', encoding='utf=8'))
        for key, items in list(b.items()):
            if items['name'] == name and items['town'] == payment_from:
                b.pop(key, items)
        json.dump(b, open(os.path.abspath(self.file), 'w', encoding='utf=8'), ensure_ascii=False, indent=2)