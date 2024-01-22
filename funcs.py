from classes import HeadHunterAPI, SuperJobAPI


def user_interaction():
    """
    Функция для взаимодействия с пользователем
    :return: словарь найденных вакансий по запросу пользователя
    """
    quantity = int(input('Введите количество вакансий для поиска:'))
    keyword = str(input('Введите ключевое слово:'))
    search_query = int(input('Выберите сайт, на котором искать вакансии: "HeadHunter" - 1 или "SuperJob" - 2'))
    if search_query not in [1, 2]:
        print('Введите 1 или 2: "HeadHunter" - 1 или "SuperJob" - 2')
        user_interaction()
    elif search_query == 1:
        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies(keyword, quantity)
        print(f'Найдено {len(vacancies)} вакансий')
        return vacancies
    else:
        sj_api = SuperJobAPI()
        vacancies = sj_api.get_vacancies(keyword, quantity)
        print(f'Найдено {len(vacancies)} вакансий')
        return vacancies


def choise_command():
    """
    Функция для выбора действий пользователя
    :return: команда пользователя
    """
    command = int(input('Выберите действия:\n'
                        '1 - найти другие вакансии\n'
                        '2 - вывести найденные вакансии в терминале\n'
                        '3 - отсортировать по зарплате\n'
                        '4 - удалить вакансию из файла\n'
                        '5 - выйти\n'))
    return command