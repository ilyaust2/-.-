# Функция для расчёта времени запаздывания в первом задании
import numpy as np
from scipy.integrate import solve_ivp


def func_timedelta2(data):
    # кинематический коэффициент вязкости
    gamma = 0.76 * 10 ** 6

    # Рассчитываем скорости потока через трубопроводы
    V_1 = 4 * np.array(data['data_q'][0]) / (3600 * 10 ** (-6) * np.pi * (159 - 2 * 6) ** 2)
    V_2 = 4 * np.array(data['data_q'][1]) / (3600 * 10 ** (-6) * np.pi * (159 - 2 * 6) ** 2)
    V_3 = 4 * np.array(data['data_q'][2]) / (3600 * 10 ** (-6) * np.pi * (219 - 2 * 8) ** 2)
    V = np.vstack((V_1, V_2, V_3))

    # Данные для труб
    d1 = [147, 147, 203]
    L = [1979, 303, 440]

    integ = np.zeros((3, len(V_1)))
    for k in range(3):
        for i in range(len(V_1)):
            y0 = [V[k][i], 0]
            d = d1[k]

            # Определение дифференциального уравнения
            def Navie_Stocks(t, u_a):
                u = u_a[0]
                a = u_a[1]
                return [a, (1 / (gamma)) * (2 * a * u + (
                            (0.0032 + 0.221 / (u * d * 10 ** (15) / gamma) ** 0.237) * u ** 2 / (2 * d * 10 ** (-3))))]

            t = np.linspace(0, L[k], 10000)
            # Решение дифференциального уравнения
            sol = solve_ivp(Navie_Stocks, t_span=[0, max(t)], y0=y0, t_eval=t)
            # Интегрирование решения для нахождения времени запаздывания
            for j in range(10000 - 1):
                integ[k][i] += (sol.t[j + 1] - sol.t[j]) / sol.y[0][j]
            print(integ[k][i] / 60)

    # Вычисление среднего времени запаздывания для каждого трубопровода
    time1 = np.sum(integ[0]) / len(integ[0])
    time2 = np.sum(integ[1]) / len(integ[1])
    time3 = np.sum(integ[2]) / len(integ[2])
    return str(min(time1, time2, time3))
