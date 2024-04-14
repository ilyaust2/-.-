import csv
import datetime
# Считывание данных из таблицы с показаниями датчиков


def read_csv_to_list_kip(file_path, sensor_number):
    # Массивы с датой (в секундах) и со значениями измерений в эту дату
    dates_kip = []
    data_kip = []

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        i = 0
        for row in csv_reader:
            i += 1
            if i == 1:
                continue
            elem = row[0].split(';')
            # Используем обработчик ошибок, т.к. в таблице есть некорретные значения ('Bad')
            try:
                if i == 2:
                    start = datetime.datetime.strptime(elem[0], '%d.%m.%Y %H:%M')
                # Перевод даты в секунды относительно начальной
                a = datetime.datetime.strptime(elem[0], '%d.%m.%Y %H:%M') - start
                a = a.total_seconds()
                data_kip.append(float(elem[sensor_number]))
                dates_kip.append(a)
            except ValueError:
                continue
    # Возвращаем массивы
    return [dates_kip, data_kip]
