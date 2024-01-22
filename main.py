from classes import JSONSaver, Vacancy
from funcs import user_interaction, choise_command

vac = user_interaction()
json_saver = JSONSaver()
json_saver.to_json(vac)
print('Найденные вакансии сохранены в файл')
com = 0
while com != 5:
    com = choise_command()
    if com == 1:
        vac2 = user_interaction()
        second_search = input('Дозаписать найденные вакансии в файл? Да - 1')
        if int(second_search) == 1:
            json_saver.add_vacancy(vac2)
            print('Файл обновлен')
        else:
            continue
    elif com == 2:
        a = json_saver.read_vacancy()
        for i in a:
            print(i)
            print('-' * 50)
    elif com == 3:
        a = json_saver.read_vacancy()
        for i in sorted(a, reverse=True):
            print(i)
            print('-' * 50)
    elif com == 4:
        name = input('Введите название вакансии для удаления:')
        town = input('Введите город, в котором открыта вакансия:')
        del_vac = Vacancy(name, 0, 0, town)
        json_saver.delete_vacancy(del_vac)
        print('Вакансия удалена')
    elif com not in [1, 2, 3, 4, 5]:
        print('Такая команда не найдена')
else:
    print('Всего доброго!')
