# -*- coding: utf-8 -*-
"""CK.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Bq9FK6eL4z74ob7OI3CzkuOxZgF-mKhs
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import statistics as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import random as rnd

from sklearn import tree

from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split



from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report


# %matplotlib inline
sns.set()


df = pd.read_csv('CK.csv')

"""

---


# **Анализ числовых и категориальных признаков (НУЖНО!)**


---

"""

df

df.describe(include=['O'])

df.describe()

"""

---


# **Анализ дубликатов и пустот (НУЖНО!)**


---

"""

df

df = df.drop_duplicates(keep=False) # 4374 - 4002 = 372

for name in list(df.columns):
    print(f'{name}: {int(df[[name]].isnull().sum()) / len(df) * 100:.2f}%')

"""

---


# **Анализ аномалий (НУЖНО!)**


---

"""

from pandas.api.types import is_string_dtype


num_property_list = ['PRICE', 'BEDS', 'BATH', 'PROPERTYSQFT', 'LATITUDE', 'LONGITUDE']

fig, ax = plt.subplots(2, 3)
fig.set_figwidth(15)
fig.set_figheight(10)
r
for i in range(3):
    for j in range(2):
        ax[j][i].scatter(x=list(df.index), y=sorted(list(df[num_property_list[j * 3 + i]])), c='blue', s=3)
        ax[j][i].set_title(num_property_list[j * 3 + i])
        ax[j][i].legend([f'Среднее значение: {st.mean(list(df[num_property_list[j * 3 + i]])):.2f}'])
        ax[j][i].set_xticks([], [])
        ax[j][i].set_yticks([])

df.drop(list(df[df['PRICE'] > 15000000].index), axis = 0, inplace = True)
df.drop(list(df[df['BEDS'] > 17].index), axis = 0, inplace = True)
df.drop(list(df[(df['BATH'] > 2) & (df['BATH'] < 3)].index), axis = 0, inplace = True)
df.drop(list(df[df['BATH'] > 15].index), axis = 0, inplace = True)
df.drop(list(df[df['PROPERTYSQFT'] > 7000].index), axis = 0, inplace = True)

"""

---


# **Зависимость кол-ва ванных комнат от спален (НЕ ОСОБО НУЖНО!)**


---

"""

fig, ax = plt.subplots(1, 1)
fig.set_figwidth(8)
fig.set_figheight(8)

ax.scatter(x=df['BEDS'], y=df['BATH'], c='blue', s=3)
ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

sns.lmplot(x='BEDS', y='BATH', data=df)

"""

---


# **Анализ категориальных свойств (НУЖНО!)**


---

"""

del df['FORMATTED_ADDRESS']
del df['LONG_NAME']
del df['STREET_NAME']
del df['SUBLOCALITY']
del df['LOCALITY']
del df['ADMINISTRATIVE_AREA_LEVEL_2']
del df['MAIN_ADDRESS']
del df['STATE']
del df['ADDRESS']

series = df['TYPE'].value_counts()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(series)

fig, ax = plt.subplots(1, 1)
fig.set_figwidth(8)
fig.set_figheight(8)

ax.scatter(x=df[df['TYPE'].isin(['Condo for sale'])]['LATITUDE'], y=df[df['TYPE'].isin(['Condo for sale'])]['LONGITUDE'], c='b', s=3)
ax.scatter(x=df[df['TYPE'].isin(['Condop for sale'])]['LATITUDE'], y=df[df['TYPE'].isin(['Condop for sale'])]['LONGITUDE'], c='r', s=15)

df.loc[df['TYPE'] == 'Condop for sale', 'TYPE'] = 'Condo for sale'

df.drop(list(df[df['TYPE'].isin(list(series[series.values < 20].index))].index), axis = 0, inplace = True)

series = df['BROKERTITLE'].value_counts()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(series[series.values > 20])

print(len(list(map(lambda x: x.lower(), list(series.index)))))
print(len(set(list(map(lambda x: x.lower(), list(series.index))))))

df.drop(list(df[df['BROKERTITLE'].isin(['NoBroker'])].index), axis = 0, inplace = True)

unic_broker = {}

for broker in list(df['BROKERTITLE']):
    if broker.lower() not in unic_broker.keys():
        unic_broker[broker.lower()] = broker
    else:
        df.loc[df['BROKERTITLE'] == broker, 'BROKERTITLE'] = unic_broker[broker.lower()]

series = list(df['BROKERTITLE'].value_counts().index)
series.reverse()

y = list(st.mean(df[df['BROKERTITLE'].isin([series[num]])]['PRICE']) for num in range(len(series)))

fig, ax = plt.subplots(1, 1)
fig.set_figwidth(5)
fig.set_figheight(5)

series = df['BROKERTITLE'].value_counts()
ax.scatter(x=[x for x in range(len(y))], y=y, c='b', s=5)

ax.set_yticks([0, 2000000, 4000000, 6000000, 8000000, 10000000, 12000000,
           14000000, 16000000])
ax.set_xticks([])

ax.set_xlabel(f'Мало продаж                         Много продаж')
ax.ticklabel_format(useOffset=False, style='plain', axis='y')
ax.set_title('Средние цены брокеров по мере возрастания продаж')

plt.axvline(x = 490, color = 'g', label = 'Продажа =1')
plt.axvline(x = 770, color = 'r', label = 'Продажа <5')

plt.legend()

"""

---


# **Ценовой диапазон по расположению жилья (НЕ ОСОБО НУЖНО!)**


---

"""

df

stat_df = df[df['TYPE'] == 'Co-op for sale'].copy()
fig = go.Figure(go.Scattermapbox(lat=stat_df['LATITUDE'],
                                 lon=stat_df['LONGITUDE'],
                                 text='Фирма брокера: ' + stat_df['BROKERTITLE'] + '<br>' \
                                 + 'Количество спален: ' + stat_df['BEDS'].astype(str) + '<br>' \
                                 + 'Количество ванных: ' + stat_df['BATH'].astype(int).astype(str) + '<br>' \
                                 + 'Площадь: ' + stat_df['PROPERTYSQFT'].astype(str) + '<br>' \
                                 + 'Цена: ' + stat_df['PRICE'].astype(str) + '$',
                                 marker=dict(colorbar=dict(title='Цена',
                                                           ticktext=['Низкая цена', 'Высокая цена'],
                                                           tickvals=[5, 7]),
                                             color=np.log10(stat_df['PRICE']),
                                             size=np.log10(stat_df['PRICE']))))

map_center = go.layout.mapbox.Center(lat=(stat_df['LATITUDE'].max()+stat_df['LATITUDE'].min())/2,
                                     lon=(stat_df['LONGITUDE'].max()+stat_df['LONGITUDE'].min())/2)

fig.update_layout(legend_orientation='h',
                  mapbox_style='carto-positron',
                  mapbox=dict(center=map_center, zoom=10),
                  margin={"r":0,"t":0,"l":0,"b":0},
                  hoverlabel=dict(bgcolor="white",
                                  font_size=16,
                                  font_family="Inter"))
fig.show()

stat_df = df[df['TYPE'] == 'Condo for sale'].copy()
fig = go.Figure(go.Scattermapbox(lat=stat_df['LATITUDE'],
                                 lon=stat_df['LONGITUDE'],
                                 text='Фирма брокера: ' + stat_df['BROKERTITLE'] + '<br>' \
                                 + 'Количество спален: ' + stat_df['BEDS'].astype(str) + '<br>' \
                                 + 'Количество ванных: ' + stat_df['BATH'].astype(int).astype(str) + '<br>' \
                                 + 'Площадь: ' + stat_df['PROPERTYSQFT'].astype(str) + '<br>' \
                                 + 'Цена: ' + stat_df['PRICE'].astype(str) + '$',
                                 marker=dict(colorbar=dict(title='Цена',
                                                           ticktext=['Низкая цена', 'Высокая цена'],
                                                           tickvals=[5, 7]),
                                             color=np.log10(stat_df['PRICE']),
                                             size=np.log10(stat_df['PRICE']))))

map_center = go.layout.mapbox.Center(lat=(stat_df['LATITUDE'].max()+stat_df['LATITUDE'].min())/2,
                                     lon=(stat_df['LONGITUDE'].max()+stat_df['LONGITUDE'].min())/2)

fig.update_layout(legend_orientation='h',
                  mapbox_style='carto-positron',
                  mapbox=dict(center=map_center, zoom=10),
                  margin={"r":0,"t":0,"l":0,"b":0},
                  hoverlabel=dict(bgcolor="white",
                                  font_size=16,
                                  font_family="Inter"))
fig.show()

stat_df = df[df['TYPE'] == 'Contingent'].copy()
fig = go.Figure(go.Scattermapbox(lat=stat_df['LATITUDE'],
                                 lon=stat_df['LONGITUDE'],
                                 text='Фирма брокера: ' + stat_df['BROKERTITLE'] + '<br>' \
                                 + 'Количество спален: ' + stat_df['BEDS'].astype(str) + '<br>' \
                                 + 'Количество ванных: ' + stat_df['BATH'].astype(int).astype(str) + '<br>' \
                                 + 'Площадь: ' + stat_df['PROPERTYSQFT'].astype(str) + '<br>' \
                                 + 'Цена: ' + stat_df['PRICE'].astype(str) + '$',
                                 marker=dict(colorbar=dict(title='Цена',
                                                           ticktext=['Низкая цена', 'Высокая цена'],
                                                           tickvals=[5.47, 7]),
                                             color=np.log10(stat_df['PRICE']),
                                             size=np.log10(stat_df['PRICE']))))

map_center = go.layout.mapbox.Center(lat=(stat_df['LATITUDE'].max()+stat_df['LATITUDE'].min())/2,
                                     lon=(stat_df['LONGITUDE'].max()+stat_df['LONGITUDE'].min())/2)

fig.update_layout(legend_orientation='h',
                  mapbox_style='carto-positron',
                  mapbox=dict(center=map_center, zoom=10),
                  margin={"r":0,"t":0,"l":0,"b":0},
                  hoverlabel=dict(bgcolor="white",
                                  font_size=16,
                                  font_family="Inter"))
fig.show()

stat_df = df[df['TYPE'] == 'House for sale'].copy()
fig = go.Figure(go.Scattermapbox(lat=stat_df['LATITUDE'],
                                 lon=stat_df['LONGITUDE'],
                                 text='Фирма брокера: ' + stat_df['BROKERTITLE'] + '<br>' \
                                 + 'Количество спален: ' + stat_df['BEDS'].astype(str) + '<br>' \
                                 + 'Количество ванных: ' + stat_df['BATH'].astype(int).astype(str) + '<br>' \
                                 + 'Площадь: ' + stat_df['PROPERTYSQFT'].astype(str) + '<br>' \
                                 + 'Цена: ' + stat_df['PRICE'].astype(str) + '$',
                                 marker=dict(colorbar=dict(title='Цена',
                                                           ticktext=['Низкая цена', 'Высокая цена'],
                                                           tickvals=[5.41, 7]),
                                             color=np.log10(stat_df['PRICE']),
                                             size=np.log10(stat_df['PRICE']))))

map_center = go.layout.mapbox.Center(lat=(stat_df['LATITUDE'].max()+stat_df['LATITUDE'].min())/2,
                                     lon=(stat_df['LONGITUDE'].max()+stat_df['LONGITUDE'].min())/2)

fig.update_layout(legend_orientation='h',
                  mapbox_style='carto-positron',
                  mapbox=dict(center=map_center, zoom=10),
                  margin={"r":0,"t":0,"l":0,"b":0},
                  hoverlabel=dict(bgcolor="white",
                                  font_size=16,
                                  font_family="Inter"))
fig.show()

stat_df = df[df['TYPE'] == 'Multi-family home for sale'].copy()
fig = go.Figure(go.Scattermapbox(lat=stat_df['LATITUDE'],
                                 lon=stat_df['LONGITUDE'],
                                 text='Фирма брокера: ' + stat_df['BROKERTITLE'] + '<br>' \
                                 + 'Количество спален: ' + stat_df['BEDS'].astype(str) + '<br>' \
                                 + 'Количество ванных: ' + stat_df['BATH'].astype(int).astype(str) + '<br>' \
                                 + 'Площадь: ' + stat_df['PROPERTYSQFT'].astype(str) + '<br>' \
                                 + 'Цена: ' + stat_df['PRICE'].astype(str) + '$',
                                 marker=dict(colorbar=dict(title='Цена',
                                                           ticktext=['Низкая цена', 'Высокая цена'],
                                                           tickvals=[5.58, 6.87]),
                                             color=np.log10(stat_df['PRICE']),
                                             size=np.log10(stat_df['PRICE']))))

map_center = go.layout.mapbox.Center(lat=(stat_df['LATITUDE'].max()+stat_df['LATITUDE'].min())/2,
                                     lon=(stat_df['LONGITUDE'].max()+stat_df['LONGITUDE'].min())/2)

fig.update_layout(legend_orientation='h',
                  mapbox_style='carto-positron',
                  mapbox=dict(center=map_center, zoom=10),
                  margin={"r":0,"t":0,"l":0,"b":0},
                  hoverlabel=dict(bgcolor="white",
                                  font_size=16,
                                  font_family="Inter"))
fig.show()

stat_df = df[df['TYPE'] == 'Pending'].copy()
fig = go.Figure(go.Scattermapbox(lat=stat_df['LATITUDE'],
                                 lon=stat_df['LONGITUDE'],
                                 text='Фирма брокера: ' + stat_df['BROKERTITLE'] + '<br>' \
                                 + 'Количество спален: ' + stat_df['BEDS'].astype(str) + '<br>' \
                                 + 'Количество ванных: ' + stat_df['BATH'].astype(int).astype(str) + '<br>' \
                                 + 'Площадь: ' + stat_df['PROPERTYSQFT'].astype(str) + '<br>' \
                                 + 'Цена: ' + stat_df['PRICE'].astype(str) + '$',
                                 marker=dict(colorbar=dict(title='Цена',
                                                           ticktext=['Низкая цена', 'Высокая цена'],
                                                           tickvals=[5.25, 6.95]),
                                             color=np.log10(stat_df['PRICE']),
                                             size=np.log10(stat_df['PRICE']))))

map_center = go.layout.mapbox.Center(lat=(stat_df['LATITUDE'].max()+stat_df['LATITUDE'].min())/2,
                                     lon=(stat_df['LONGITUDE'].max()+stat_df['LONGITUDE'].min())/2)

fig.update_layout(legend_orientation='h',
                  mapbox_style='carto-positron',
                  mapbox=dict(center=map_center, zoom=10),
                  margin={"r":0,"t":0,"l":0,"b":0},
                  hoverlabel=dict(bgcolor="white",
                                  font_size=16,
                                  font_family="Inter"))
fig.show()

stat_df = df[df['TYPE'] == 'Townhouse for sale'].copy()
fig = go.Figure(go.Scattermapbox(lat=stat_df['LATITUDE'],
                                 lon=stat_df['LONGITUDE'],
                                 text='Фирма брокера: ' + stat_df['BROKERTITLE'] + '<br>' \
                                 + 'Количество спален: ' + stat_df['BEDS'].astype(str) + '<br>' \
                                 + 'Количество ванных: ' + stat_df['BATH'].astype(int).astype(str) + '<br>' \
                                 + 'Площадь: ' + stat_df['PROPERTYSQFT'].astype(str) + '<br>' \
                                 + 'Цена: ' + stat_df['PRICE'].astype(str) + '$',
                                 marker=dict(colorbar=dict(title='Цена',
                                                           ticktext=['Низкая цена', 'Высокая цена'],
                                                           tickvals=[5.71, 7]),
                                             color=np.log10(stat_df['PRICE']),
                                             size=np.log10(stat_df['PRICE']))))

map_center = go.layout.mapbox.Center(lat=(stat_df['LATITUDE'].max()+stat_df['LATITUDE'].min())/2,
                                     lon=(stat_df['LONGITUDE'].max()+stat_df['LONGITUDE'].min())/2)

fig.update_layout(legend_orientation='h',
                  mapbox_style='carto-positron',
                  mapbox=dict(center=map_center, zoom=10),
                  margin={"r":0,"t":0,"l":0,"b":0},
                  hoverlabel=dict(bgcolor="white",
                                  font_size=16,
                                  font_family="Inter"))
fig.show()

df

"""

---


# **Кодировка категориальных свойств (НУЖНО!)**


---

"""

df_copy = df.copy(deep=True)

enc = OrdinalEncoder()
df[['BROKERTITLE']] = enc.fit_transform(df[['BROKERTITLE']])

enc = OneHotEncoder()
res = enc.fit_transform(df[['TYPE']])
df[enc.categories_[0]] = res.toarray()
del df['TYPE']

with pd.option_context('display.max_columns', None):
    display(df)

"""

---


# **Тепловая карта (НУЖНО!)**


---

"""

sns.heatmap(df.corr())

"""

---


# **1 Метод**
# **Регрессия (Работает)**
# **Полиномиальная**


---

"""

scaler_mm = MinMaxScaler()
scaler_s = StandardScaler()

x_col = ['BEDS', 'BATH', 'PROPERTYSQFT', 'LATITUDE', 'LONGITUDE', 'Condo for sale']

x = df[x_col].copy(deep=True)
y = df['PRICE'].copy(deep=True)

x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size=0.3,
                                                    random_state=57)

x_train = scaler_mm.fit_transform(x_train, y_train)
x_test = scaler_mm.transform(x_test)

poly_features = PolynomialFeatures(degree=3)
x_poly = poly_features.fit_transform(x_train)
poly_model = LinearRegression()
poly_model.fit(x_poly, y_train)

x_test_poly = poly_features.fit_transform(x_test)

y_pred = poly_model.predict(x_test_poly)

print('R2 score: ', r2_score(y_test, y_pred))
print('Mean squared error: ', mean_squared_error(y_test, y_pred))

fig, ax = plt.subplots()
fig.set_figwidth(250)
fig.set_figheight(7)

ax.plot(range(len(y_test)), y_test, c='blue')
ax.plot(range(len(y_pred)), y_pred, c='red')
ax.legend(['True value', 'Predicate value'], loc='upper left')

fig.show()

"""

---


# **2 Метод**
# **Классификация (Не работает)**
# **Наивный Байес (Гаусс и Многочленный)**


---

"""

df = df_copy.copy(deep=True)

enc = OrdinalEncoder()
df[['BROKERTITLE']] = enc.fit_transform(df[['BROKERTITLE']])

x_col = ['BEDS', 'BATH', 'PROPERTYSQFT']

x = df[x_col].copy(deep=True)
y = df['TYPE'].copy(deep=True)

x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size=0.3,
                                                    random_state=57, stratify=y)

x_train = scaler_mm.fit_transform(x_train, y_train)
x_test = scaler_mm.transform(x_test)

gnb = GaussianNB()
mnb = MultinomialNB()

y_pred_gnb = gnb.fit(x_train, y_train).predict(x_test)
cm = confusion_matrix(y_test, y_pred_gnb)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()

y_pred_mnb = mnb.fit(x_train, y_train).predict(x_test)
cm = confusion_matrix(y_test, y_pred_mnb)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()

print(classification_report(y_test, y_pred_gnb))
print(classification_report(y_test, y_pred_mnb))

"""

---


# **3 Метод**
# **Классификация (Работает)**
# **Деревья решений**


---

"""

df = df_copy.copy(deep=True)

enc = OrdinalEncoder()
df[['BROKERTITLE']] = enc.fit_transform(df[['BROKERTITLE']])

x = df.drop('TYPE', axis=1)
y = df['TYPE']

x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size=0.2,
                                                    random_state=57, stratify=y)

x_train = scaler_mm.fit_transform(x_train)
x_test = scaler_mm.transform(x_test)

clf = DecisionTreeClassifier(random_state=8, max_depth=7)
clf.fit(x_train, y_train)
print('Точность предсказания дерева решений: ', clf.score(x_test, y_test))

y_pred = clf.predict(x_test)
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=clf.classes_, xticks_rotation='vertical')

print(classification_report(y_test, y_pred))

plt.figure(figsize=(200, 25))
tree.plot_tree(clf, feature_names=clf.feature_importances_, class_names=clf.classes_, rounded=True, filled=True)
plt.show()

"""

---


# **4 Метод**
# **Классификация (Работает)**
# **Случайный лес**


---

"""

df = df_copy.copy(deep=True)

enc = OrdinalEncoder(dtype=int)
df[['BROKERTITLE']] = enc.fit_transform(df[['BROKERTITLE']])

x = df.drop('TYPE', axis=1)
y = df['TYPE']

x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size=0.3,
                                                    random_state=57, stratify=y)

x_train = scaler_s.fit_transform(x_train, y_train)
x_test = scaler_s.transform(x_test)

rfc = RandomForestClassifier(random_state=8, max_depth=21)
rfc.fit(x_train, y_train)
print('Точность предсказания случайного леса: ', rfc.score(x_test, y_test))

y_pred = rfc.predict(x_test)
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=rfc.classes_, xticks_rotation='vertical')

print(classification_report(y_test, y_pred))

"""

---


# **5 Метод**
# **Кластеризация (Работает)**
# **PCA и DBSCAN**


---

"""

df = df_copy.copy(deep=True)

x_col = ['BROKERTITLE', 'BEDS', 'BATH', 'PROPERTYSQFT', 'PRICE']
df = df[x_col].copy(deep=True)

enc = OrdinalEncoder()
df[['BROKERTITLE']] = enc.fit_transform(df[['BROKERTITLE']])

enc = OneHotEncoder()
res = enc.fit_transform(df[['TYPE']])
df[enc.categories_[0]] = res.toarray()
del df['TYPE']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

X_normalized = normalize(X_scaled)
X_normalized = pd.DataFrame(X_normalized)

pca = PCA(n_components = 2)
X_principal = pca.fit_transform(X_normalized)
X_principal = pd.DataFrame(X_principal)
X_principal.columns = ['P1', 'P2']
print(X_principal.head())

for j in range(35, 75, 1):
    for i in range(1, 100):
        db_new = DBSCAN(eps = j / 1000, min_samples = i).fit(X_principal)
        labels = db_new.labels_
        myset = set(labels)
        if len(myset) == 4:
            print(f'eps: {j / 1000}  min_samples: {i}')

db_new = DBSCAN(eps = 0.063, min_samples = 3).fit(X_principal)
labels = db_new.labels_

myset = set(labels)
print(myset)

a_part_of_color = ['20', '80', 'E0']
b_part_of_color = ['20','80', 'E0']
c_part_of_color = ['20','80', 'E0']
using_color = []
def get_color():
    color = '#' + rnd.choice(a_part_of_color) + rnd.choice(b_part_of_color) + rnd.choice(c_part_of_color)
    if color not in using_color:
        using_color.append(color)
        return color
    else:
        return get_color()

using_color = []
colours = {}
for i in set(labels):
    colours[i] = get_color()
colours[-1] = '#000000'

cvec = [colours[label] for label in labels]

plt.figure(figsize = (7, 7))
plt.scatter(X_principal['P1'], X_principal['P2'], c = cvec)
plt.show()

stat_df = df_copy.copy(deep=True)
fig = go.Figure(go.Scattermapbox(lat=stat_df['LATITUDE'],
                                 lon=stat_df['LONGITUDE'],
                                 text='Фирма брокера: ' + stat_df['BROKERTITLE'] + '<br>' \
                                 + 'Количество спален: ' + stat_df['BEDS'].astype(str) + '<br>' \
                                 + 'Количество ванных: ' + stat_df['BATH'].astype(int).astype(str) + '<br>' \
                                 + 'Площадь: ' + stat_df['PROPERTYSQFT'].astype(str) + '<br>' \
                                 + 'Цена: ' + stat_df['PRICE'].astype(str) + '$',
                                 marker=dict(color=cvec,
                                             size=7)))

map_center = go.layout.mapbox.Center(lat=(stat_df['LATITUDE'].max()+stat_df['LATITUDE'].min())/2,
                                     lon=(stat_df['LONGITUDE'].max()+stat_df['LONGITUDE'].min())/2)

fig.update_layout(legend_orientation='h',
                  mapbox_style='carto-positron',
                  mapbox=dict(center=map_center, zoom=10),
                  margin={"r":0,"t":0,"l":0,"b":0},
                  hoverlabel=dict(bgcolor="white",
                                  font_size=16,
                                  font_family="Inter"))
fig.show()