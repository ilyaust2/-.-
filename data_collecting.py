# Файл для формирования JSON запроса
# Использует приведённые данные из исходных таблиц

import pandas as pd
import numpy as np
from read_lab import read_csv_to_list_lab
from read_kip import read_csv_to_list_kip

# пути до таблиц и номер датчика
csv_file_path_lab = r'C:\Users\Olymp\Documents\Это папка\Регрессия_ЛА.csv'
csv_file_path_kip = r'C:\Users\Olymp\Documents\Это папка\Регрессия_КИП.csv'
sensor_number = 3

for_lab = read_csv_to_list_lab(csv_file_path_lab)
for_kip = read_csv_to_list_kip(csv_file_path_kip, sensor_number)

# Данные, которые используются в JSON запросе для первого задания
values_dates_lab = for_lab[0]
values_data_lab = for_lab[1]
values_dates_kip = for_kip[0]
values_data_kip = for_kip[1]

# Данные, которые используются в JSON запросе для второго задания
data_q = pd.read_excel(r'C:\Users\Olymp\Documents\Это папка\Смешение.xlsx', skiprows=0)
data_q = np.array(data_q).T[1:]
data_q = [[el for el in elem] for elem in data_q]

