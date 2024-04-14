# Функция для расчёта времени запаздывания в первом задании
import numpy as np


def func_timedelta1(data):
    # Переданные данные из JSON
    t_lab = data['dates_lab'][:250]
    t_kip = data['dates_kip'][:733082]
    v_lab = data['data_lab'][:250]
    v_kip = data['data_kip'][:733082]
    # В этот список заносятся данные с интерполяции
    v_lab_1 = []

    # Линейная интреполяция точек лабораторного анализа
    for i in range(len(t_lab) - 1):
        k = (v_lab[i + 1] - v_lab[i]) / (t_lab[i + 1] - t_lab[i])
        b = v_lab[i] - k * t_lab[i]
        for elem in t_kip:
            if elem > t_lab[i + 1]:
                break
            if elem < t_lab[i]:
                continue
            v_lab_1.append(k * elem + b)

    # Вычисляем одномерную кросс-корреляцию
    correlation = np.correlate(v_lab_1, v_kip, mode='same')

    # Находим индекс максимального значения корреляции
    timedelta1 = np.argmax(correlation)
    return str(timedelta1)
