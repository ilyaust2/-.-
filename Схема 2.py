#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import solve_ivp

# Загрузка данных из файла Excel
data = pd.read_excel('Смешение.xlsx', skiprows=0)
data = np.array(data).T
#print(data)

# Рассчитываем скорости потока через трубопроводы
V_1 = 4*data[1]/(3600*10**(-6)*np.pi*(159-2*6)**2)
#print(V_1)
V_2 = 4*data[2]/(3600*10**(-6)*np.pi*(159-2*6)**2)
#print(V_2)
V_3 = 4*data[3]/(3600*10**(-6)*np.pi*(219-2*8)**2)
#print(V_3)

gamma = 0.76*10**(6)

d1 = [147, 147, 203]
L = [1979, 303, 440]

integ = np.zeros((3, len(V_1)))
for k in range(3):
    for i in range(len(V_1)):
        y0 = [V_1[i], 0]
        d = d1[k]
        # Определение дифференциального уравнения
        def Navie_Stocks(t, u_a):
            u = u_a[0]
            a = u_a[1]
            return[a, (1/(gamma))*(2*a*u + ((0.0032+0.221/(u*d*10**(15)/gamma)**0.237)*u**2/(2*d*10**(-3))))]
        t = np.linspace(0, L[k], 10000)
        # Решение дифференциального уравнения
        sol = solve_ivp(Navie_Stocks, t_span=[0, max(t)], y0 = y0, t_eval=t)
        # Интегрирование решения для нахождения времени запаздывания
        for j in range(10000-1):
            integ[k][i] += (sol.t[j+1]-sol.t[j])/sol.y[0][j]
        print(integ[k][i]/60)

# Загрузка данных из файла Excel
data = pd.read_excel('Смешение.xlsx')

# Выбор только первого столбца с датами и преобразование их во временные метки
timestamps = pd.to_datetime(data.iloc[:, 0])

# Преобразование времени в минуты
time_in_minutes = [((timestamp.day-1)*24*60 + timestamp.hour * 60 + timestamp.minute) for timestamp in timestamps]

# Построение графика
plt.figure(figsize=(8, 6))
plt.grid()
plt.plot(time_in_minutes, integ[0]/60, label = f'Length of the oil pipeline №1 = {L[0]}m')
plt.plot(time_in_minutes, integ[1]/60, label = f'Length of the oil pipeline №2 = {L[1]}m')
plt.plot(time_in_minutes, integ[2]/60, label = f'Length of the oil pipeline №3 = {L[2]}m')
plt.ylabel('Transport delay time, minutes')
plt.xlabel('The time of measuring the quality of gasoline\nin the input sensor relative to the initial time, minutes')
plt.title('The dependence of the transport delay time\non the time when the quality of the oil product was measured')
plt.legend()

# Сохранение графика
plt.savefig('График.png')
print(V_1*3.6)

# Вычисление среднего времени запаздывания для каждого трубопровода
time1 = np.sum(integ[0]/60)/len(integ[0])
print(f'Length of the oil pipeline №1 = {L[0]}m ----> {time1}')
time2 = np.sum(integ[1]/60)/len(integ[1])
print(f'Length of the oil pipeline №2 = {L[1]}m ----> {time2}')
time3 = np.sum(integ[2]/60)/len(integ[2])
print(f'Length of the oil pipeline №3 = {L[2]}m ----> {time3}')
