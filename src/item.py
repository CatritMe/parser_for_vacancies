import json
import requests

url_hh = 'https://api.hh.ru/vacancies'
hh_vacancies = requests.get(url_hh).json()
print(hh_vacancies)