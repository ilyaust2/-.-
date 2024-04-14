# Файл с отправкой JSON запроса на сервер и принятием ответа - времени запаздывания
import requests
from data_collecting import values_dates_kip, values_dates_lab, values_data_lab, values_data_kip, data_q

# Ручной ввод данных для JSON запроса
'''
values_dates_kip = []
values_data_kip = []
values_dates_lab = []
values_data_lab = []
'''

# URL адрес сервера

url = 'http://localhost:5000/api/timedelta1'

# JSON запрос и его отправка на сервер в первом задании

data = {
    'dates_kip': values_dates_kip,
    'data_kip': values_data_kip,
    'dates_lab': values_dates_lab,
    'data_lab': values_data_lab
}

# JSON запрос и его отправка на сервер во втором задании
'''
data = {
    'data_q': data_q
}
'''
response = requests.get(url, json=data)

# Вывод времени транспортного запаздывания
print(response.json())
