import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import solve_ivp

# Чтение данных из файла Excel, пропуская первую строку
data = pd.read_excel('Смешение.xlsx', skiprows=0)
# Преобразование данных в массив NumPy и транспонирование для удобства
data = np.array(data).T

# Вычисление начальных скоростей потока
V_1 = 4*data[1]/(3600*10**(-6)*np.pi*(159-2*6)**2)
V_2 = 4*data[2]/(3600*10**(-6)*np.pi*(159-2*6)**2)
V_3 = 4*data[3]/(3600*10**(-6)*np.pi*(219-2*8)**2)

# Объединение скоростей в двумерный массив
V = np.vstack((V_1, V_2, V_3))

# Задание константы гамма
gamma = 0.76*10**(6)

# Задание длин и диаметров нефтепроводов
d1 = [147, 147, 203]
L = [1979, 303, 440]

# Вычисление интеграла времени транспортного
# запаздывания 
integ = np.zeros((3, len(V_1)))  # Создание массива для интегралов
for k in range(3):
    for i in range(len(V_1)):
        y0 = [V[k][i], 0]  # Начальные значения для решения дифференциальных уравнений
        d = d1[k]
        
        # Определение системы дифференциальных уравнений
        def Navie_Stocks(t, u_a):
            u = u_a[0]
            a = u_a[1]
            return [a, (1/(gamma))*(2*a*u + ((0.0032+0.221/(u*d*10**(15)/gamma)**0.237)*u**2/(2*d*10**(-3))))]

        # Вычисление времени
        t = np.linspace(0, L[k], 10000)
        # Решение системы дифференциальных уравнений
        sol = solve_ivp(Navie_Stocks, t_span=[0, max(t)], y0=y0, t_eval=t)
        
        # Вычисление интеграла
        for j in range(10000-1):
            integ[k][i] += (sol.t[j+1] - sol.t[j])/(sol.y[0][j])
    
# Загрузка данных из файла Excel без пропуска строк
data = pd.read_excel('Смешение.xlsx')

# Преобразование времени в минуты
timestamps = pd.to_datetime(data.iloc[:, 0])
time_in_minutes = [((timestamp.day-1)*24*60 + timestamp.hour * 60 + timestamp.minute) for timestamp in timestamps]

# Построение графика зависимости времени транспортного
# запаздывания от момента измерения качества бензина
plt.figure(figsize=(8, 6))
plt.grid()
plt.plot(time_in_minutes, integ[0]/60, label=f'Length of the oil pipeline №1 = {L[0]}m')
plt.plot(time_in_minutes, integ[1]/60, label=f'Length of the oil pipeline №2 = {L[1]}m')
plt.plot(time_in_minutes, integ[2]/60, label=f'Length of the oil pipeline №3 = {L[2]}m')
plt.ylabel('Transport delay time, minutes')
plt.xlabel('The time of measuring the quality of gasoline\nin the input sensor relative to the initial time, minutes')
plt.title('The dependence of the transport delay time\non the time when the quality of the oil product was measured')
plt.legend()

# Сохранение графика в файл 'График.png'
plt.savefig('График.png')

# Вычисление среднего времени транспортного
#  запаздывания для каждого нефтепровода
time1 = np.sum(integ[0]/60)/len(integ[0])
print(f'Length of the oil pipeline №1 = {L[0]}m ----> {time1}')
time2 = np.sum(integ[1]/60)/len(integ[1])
print(f'Length of the oil pipeline №1 = {L[1]}m ----> {time2}')
time3 = np.sum(integ[2]/60)/len(integ[2])
print(f'Length of the oil pipeline №1 = {L[2]}m ----> {time3}')
