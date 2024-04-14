import csv
import datetime
# Считывание данных из таблицы с показаниями в лаборатории


def read_csv_to_list_lab(file_path):
    # Массивы с датой(в секундах) и со значениями измерений в эту дату
    dates_lab = []
    data_lab = []

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        i = 0
        for row in csv_reader:
            i += 1
            if i == 1:
                continue
            elem = row[0].split(';')
            if i == 2:
                start = datetime.datetime.strptime(elem[0], '%d.%m.%Y %H:%M')

            # Перевод даты в секунды относительно начальной
            a = datetime.datetime.strptime(elem[0], '%d.%m.%Y %H:%M') - start
            a = a.total_seconds()
            dates_lab.append(a)
            data_lab.append(float(elem[1]))

    # Возвращаем массивы
    return [dates_lab, data_lab]
