#!/usr/bin/env python
# coding: utf-8

# # Исследование надежности заемщиков

# ## Откройте таблицу и изучите общую информацию о данных

import pandas as pd

data=pd.read_csv('C:/Users/Админ/Desktop/Учёба/Python Mysql/проект/project/data (1).csv')

# **Задание 2. Выведите первые 20 строчек датафрейма `data` на экран.**
# print(data.head(20))

# **Задание 3. Выведите основную информацию о датафрейме с помощью метода `info()`.**
# data.info()

# ## Предобработка данных
# ##Удаление пропусков

# # **Задание 4. Выведите количество пропущенных значений для каждого столбца. Используйте комбинацию двух методов.**
# print(data.isna().sum())

# # **Задание 5. В двух столбцах есть пропущенные значения. Один из них — `days_employed`. Пропуски в этом столбце вы обработаете на следующем этапе. Другой столбец с пропущенными значениями — `total_income` — хранит данные о доходах. На сумму дохода сильнее всего влияет тип занятости, поэтому заполнить пропуски в этом столбце нужно медианным значением по каждому типу из столбца `income_type`. Например, у человека с типом занятости `сотрудник` пропуск в столбце `total_income` должен быть заполнен медианным доходом среди всех записей с тем же типом.**
# # Находим пустые значения методом перебора и меняем их на медианные. Далее перепроверяем.
for el in data['income_type'].unique():
    data.loc[(data['income_type'] == el) & (data['total_income'].isna()), 'total_income'] =     data.loc[(data['income_type'] == el), 'total_income'].median()

# print(data.isna().sum())

# # ### Обработка аномальных значений

# # **Задание 6. В данных могут встречаться артефакты (аномалии) — значения, которые не отражают действительность и появились по какой-то ошибке. Таким артефактом будет отрицательное количество дней трудового стажа в столбце `days_employed`. Для реальных данных это нормально. Обработайте значения в этом столбце: замените все отрицательные значения положительными с помощью метода `abs()`.**

data.loc[data['days_employed']<0,'days_employed']=abs(data.loc[data['days_employed']<0,'days_employed'])

# # **Задание 7. Для каждого типа занятости выведите медианное значение трудового стажа `days_employed` в днях.**

# print(data.groupby('income_type')['days_employed'].median())

# # У двух типов (безработные и пенсионеры) получатся аномально большие значения. Исправить такие значения сложно, поэтому оставьте их как есть.

# # **Задание 8. Выведите перечень уникальных значений столбца `children`.**

# print(data['children'].unique())

# # **Задание 9. В столбце `children` есть два аномальных значения. Удалите строки, в которых встречаются такие аномальные значения из датафрейма `data`.**

data=data[(data.children>=0) & (data.children !=20)]

# # **Задание 10. Ещё раз выведите перечень уникальных значений столбца `children`, чтобы убедиться, что артефакты удалены.**

# print(data['children'].unique())

# # ### Удаление пропусков (продолжение)

# # **Задание 11. Заполните пропуски в столбце `days_employed` медианными значениями по каждому типу занятости `income_type`.**

for el in data['income_type'].unique():
    data.loc[(data['income_type'] == el) & (data['days_employed'].isna()), 'days_employed'] =     data.loc[(data['income_type'] == el), 'days_employed'].median()

# # **Задание 12. Убедитесь, что все пропуски заполнены. Проверьте себя и ещё раз выведите количество пропущенных значений для каждого столбца с помощью двух методов.**

# print(data.isna().sum())
# print(data.isnull().sum())

# # ### Изменение типов данных

# # **Задание 13. Замените вещественный тип данных в столбце `total_income` на целочисленный с помощью метода `astype()`.**

data['total_income'] = data['total_income'].astype('int')

# # ### Обработка дубликатов

# # **Задание 14. Обработайте неявные дубликаты в столбце `education`. В этом столбце есть одни и те же значения, но записанные по-разному: с использованием заглавных и строчных букв. Приведите их к нижнему регистру.**

data['education']=data['education'].str.lower()

# # **Задание 15. Выведите на экран количество строк-дубликатов в данных. Если такие строки присутствуют, удалите их.**

# # посчитайте дубликаты
# print(data[data.duplicated()].count())

# # удалите дубликаты
data=data.drop_duplicates()

# # ### Категоризация данных

# # **Задание 16. На основании диапазонов, указанных ниже, создайте в датафрейме `data` столбец `total_income_category` с категориями:**
# # 
# # - 0–30000 — `'E'`;
# # - 30001–50000 — `'D'`;
# # - 50001–200000 — `'C'`;
# # - 200001–1000000 — `'B'`;
# # - 1000001 и выше — `'A'`.
# # 
# # 
# # **Например, кредитополучателю с доходом 25000 нужно назначить категорию `'E'`, а клиенту, получающему 235000, — `'B'`. Используйте собственную функцию с именем `categorize_income()` и метод `apply()`.**

# # создайте функцию categorize_income()
def categorize_income (total_income):
    if total_income <=30000:
        return ('E')
    if total_income >30000 and total_income<=50000:
        return ('D')
    if total_income >50000 and total_income<=200000:
        return ('C')
    if total_income >200000 and total_income<=1000000:
        return ('B')
    if total_income >1000000:
        return ('A')


# # примените функцию методом apply()
data['total_income_category']=data['total_income'].apply(categorize_income)

# **Задание 17. Выведите на экран перечень уникальных целей взятия кредита из столбца `purpose`.**

# print(data['purpose'].unique())


# **Задание 18. Создайте функцию, которая на основании данных из столбца `purpose` сформирует новый столбец `purpose_category`, в который войдут следующие категории:**
# 
# - `'операции с автомобилем'`,
# - `'операции с недвижимостью'`,
# - `'проведение свадьбы'`,
# - `'получение образования'`.
# 
# **Например, если в столбце `purpose` находится подстрока `'на покупку автомобиля'`, то в столбце `purpose_category` должна появиться строка `'операции с автомобилем'`.**
# 
# **Используйте собственную функцию с именем `categorize_purpose()` и метод `apply()`. Изучите данные в столбце `purpose` и определите, какие подстроки помогут вам правильно определить категорию.**

# создайте функцию categorize_purpose()
def categorize_purpose(purpose):
    if (purpose=='приобретение автомобиля' or 
            purpose=='на покупку подержанного автомобиля' or 
            purpose=='на покупку своего автомобиля' or
            purpose=='сделка с подержанным автомобилем' or
            purpose=='сделка с автомобилем' or
            purpose=='автомобиль' or
            purpose=='свой автомобиль' or
            purpose=='на покупку автомобиля' or
            purpose=='автомобили'):
        return 'операции с автомобилем' 
    
    if (purpose=='покупка жилья' or
            purpose=='покупка недвижимости' or
            purpose=='строительство собственной недвижимости' or
            purpose=='недвижимость' or
            purpose=='операции с коммерческой недвижимостью' or
            purpose=='покупка коммерческой недвижимости' or
            purpose=='покупка жилья для семьи' or
            purpose=='операции с недвижимостью' or
            purpose=='жилье' or
            purpose=='операции с жильем' or
            purpose=='строительство недвижимости' or
            purpose=='покупка жилой недвижимости' or
            purpose=='покупка жилья для сдачи' or
            purpose=='покупка своего жилья' or
            purpose=='строительство жилой недвижимости' or
            purpose=='ремонт жилью' or
            purpose=='операции со своей недвижимостью'):
        return 'операции с недвижимостью'
    
    if purpose=='на проведение свадьбы' or purpose=='свадьба' or purpose=='сыграть свадьбу':
        return 'проведение свадьбы'
    
    if (purpose=='дополнительное образование' or
            purpose=='заняться образованием' or
            purpose=='получение дополнительного образования' or
            purpose=='образование' or
            purpose=='получение высшего образования' or
            purpose=='заняться высшим образованием' or
            purpose=='получение образования' or
            purpose=='профильное образование' or
            purpose=='высшее образование'):
        return 'получение образования'


# примените функцию методом apply()
data['purpose_category']=data['purpose'].apply(categorize_purpose)

print(data.head(10))
