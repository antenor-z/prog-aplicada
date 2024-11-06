import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

df_sbrj: pd.DataFrame = pd.read_excel("dataset_SBRJ.xlsx")


print("\n----------------------------------------------------------------------")
print("""
1. Quanto os valores de vento não aparecem, significa que não há vento. Complete 
os valores ausentes de velocidade do vento com zero e os valores ausentes de 
direção com zero. Mostre os 20 primeiros valores ordenados por velocidade de vento.
""")

df_sbrj.timestamp = pd.to_datetime(df_sbrj.timestamp, utc=True)
df_sbrj.set_index("timestamp", inplace=True)
df_sbrj.fillna({"wind_direction": 0, "wind_speed": 0}, inplace=True)
print(df_sbrj.sort_values("wind_speed", ascending=False).head(20))

print("\n----------------------------------------------------------------------")
print("""
2. Os valores de nuvens few (poucas), scatered (espalhadas), broken (muitas) e 
overcast (encoberto) são listas de números separados por vírgula com a altitude 
de cada nuvem. Por exemplo, few com valor "10000,12000" indicam poucas nuvens em 
10 mil pés e 12 mil pés.

Crie uma coluna pior_tipo_nuvem com o valor do tipo de nuvem mais encoberto 
seguindo a ordem few < scatered < broken < overcast. Para garantir que as nuvens 
realmente afetam o aeroporto, considere APENAS nuvens abaixo de 10 mil pés.

Qual o mais nebuloso (mais fechado) tipo de formação para cada valor de temperatura?
Parece haver relação entre a nebulosidade e a temperatura?
""")



def altitude_menor_10000(value):
    if isinstance(value, str):
        return any(int(num) < 10000 for num in value.split(','))
    elif isinstance(value, int) or isinstance(value, float):
        return value < 10000
    return False


df_sbrj['filtro_few'] = df_sbrj['clouds_few'].apply(altitude_menor_10000)
df_sbrj['filtro_scattered'] = df_sbrj['clouds_scattered'].apply(altitude_menor_10000)
df_sbrj['filtro_broken'] = df_sbrj['clouds_broken'].apply(altitude_menor_10000)
df_sbrj['filtro_overcast'] = df_sbrj['clouds_overcast'].apply(altitude_menor_10000)

def nivel_nuvem(row):
    if row['filtro_overcast']:
        return 4
    elif row['filtro_broken']:
        return 3
    elif row['filtro_scattered']:
        return 2
    elif row['filtro_few']:
        return 1
    return np.nan

df_sbrj['nivel_nuvem'] = df_sbrj.apply(nivel_nuvem, axis=1)

df_sbrj = df_sbrj.drop(columns=['filtro_few', 'filtro_scattered', 'filtro_broken', 'filtro_overcast'])
df_sbrj.groupby(["temperature"]).agg({"nivel_nuvem": "max"}).replace(
    {4: "overcast",
     3: "broken",
     2: "scattered",
     1: "few"}, inplace=True)

print(df_sbrj)


print("""
3. A velocidade de vento está expressa em nós (milhas náuticas por hora), converta 
para km/h. Crie as seguintes categorias para a velocidade do vento:

    * **Calmo:** Menor ou igual à 2km/h
    * **Bafagem:** 2 à 5 km/h
    * **Brisa leve:** 6 a 11km/h
    * **Brisa fraca:** 12 a 19km/h
    * **Brisa moderada:** 20 a 28km/h
    * **Brisa forte:** 29 a 38km/h
    * **Vento fresco:** 39 a 49km/h
    * **Vento forte:** 50 a 61km/h
    * **Ventania:** 62 a 74km/h
    * **Ventania forte:** 75 a 88km/h
    * **Tempestade:** 89 a 102km/h
    * **Tempestade violenta**: 103 a 117km/h
    * **Furacao:** Maior que 118km/h

Está é a chamada de Escala de Beaufort.

3.1. Faça uma tabela de frequências destas categorias e mostre em um gráfico pizza.
Qual é o tipo de vento mais presente?

3.2. Mostre uma tabela de frequência com o cruzamento das categorias de vento com os
valores de temperatura. Em qual facha de temperatura ocorrem mais ventos?

3.3. Para cada faixa de vento mostre temperatura mínima, média, máxima e desvio 
padrão. Parece haver relação entre velocidade do vento e temperatura?
""")

def to_kmh(wind):
    return wind * 1.852

df_sbrj["wind_speed"].apply(to_kmh)
df_sbrj["cat_vento"] = pd.cut(
    df_sbrj.wind_speed, 
    bins=[0, 2, 5, 11, 19, 28, 38, 49, 61, 74, 88, 102, 117, 9999],
    labels=["Calmo", "Bafagem", "Brisa leve", "Brisa fraca", "Brisa Moderada",
            "Brisa forte", "Vento fresco", "Vento forte", "Ventania", "Ventania fote",
            "Tempestade", "Tempestade violenta", "Furacao"],
    include_lowest=True
)

df_sbrj["cat_vento"].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
plt.title("Distribuição das Categorias de Vento")
plt.savefig("pie_chart.png")

print(pd.crosstab(df_sbrj["cat_vento"], df_sbrj["temperature"]).transpose())

print(df_sbrj.groupby("cat_vento", observed=True)
      .agg({"temperature": ["min", "max", "mean", "std"]}).
      dropna())

print(
"""
4. Junte os dataframes de dados de voo de um mesmo aeroporto. Faça os dataframes 
chegadas_SBRJ e partidas_SBRJ. Crie um dataframe atraso_chegadas_SBRJ com os 
timestamps agrupados por hora e a média de tempo de atraso. Ou seja, para cada 
hora, teremos o tempo médio de atraso. Faça o mesmo para as partidas criando o 
dataframe atraso-partidas-SBRJ.

```                 
                         _
2024-10-29-SBGL-arrivals  |
2024-10-30-SBGL-arrivals  | ----> chegadas_SBRJ -----> atraso_chegadas_SBRJ
...                       |
2024-11-05-SBGL-arrivals _|

```

Faça um Merge da tabela de condições meteorológicas com os atrasos. Crie as 
colunas atraso_chegada e atraso_partida.

Faça o cruzamento de frequência entre o nível do vento e os atrasos e entre
a pior formação de nuvens (coluna "pior_tipo_nuvem") e os atrasos. Faça 
partidas e chegadas separadamente. Parece haver uma correlação maior nas
partidas ou nas chegadas?
"""
)

sbrj_partidas = pd.DataFrame()
sbrj_chegadas = pd.DataFrame()

# Abrindo os datasets do Santos Dumont e concatenando em chegadas
# e partidas
for arquivo in os.listdir("voos"):
    if "SBRJ" in arquivo:
        if "departures" in arquivo:
            partidas_do_dia = pd.read_excel("voos/" + arquivo)
            sbrj_partidas = pd.concat([sbrj_partidas, partidas_do_dia])
        elif "arrivals" in arquivo:
            chegadas_do_dia = pd.read_excel("voos/" + arquivo)
            sbrj_chegadas = pd.concat([sbrj_chegadas, chegadas_do_dia])

sbrj_partidas = sbrj_partidas[["departure_scheduled", "flight_icao", "departure_delay"]]
sbrj_chegadas = sbrj_chegadas[["arrival_scheduled", "flight_icao", "arrival_delay"]]
sbrj_partidas.rename({"departure_delay": "atraso_partida", "departure_scheduled": "timestamp"}, axis=1, inplace=True)
sbrj_chegadas.rename({"arrival_delay": "atraso_chegada", "arrival_scheduled": "timestamp"}, axis=1, inplace=True)

sbrj_chegadas["atraso_chegada"] = (sbrj_chegadas["atraso_chegada"]
.fillna(sbrj_chegadas["atraso_chegada"].mean()))

sbrj_partidas["atraso_partida"] = (sbrj_partidas["atraso_partida"]
.fillna(sbrj_partidas["atraso_partida"].mean()))


sbrj_partidas["timestamp"] = pd.to_datetime(sbrj_partidas.timestamp, utc=True)
sbrj_chegadas["timestamp"] = pd.to_datetime(sbrj_chegadas.timestamp, utc=True)
sbrj_partidas.set_index("timestamp", inplace=True)
sbrj_chegadas.set_index("timestamp", inplace=True)

# Setando o índice para ter apenas a hora cheia
sbrj_partidas.index = sbrj_partidas.index.floor('h')
sbrj_chegadas.index = sbrj_chegadas.index.floor('h')

sbrj_partidas = sbrj_partidas.groupby("timestamp").agg({"atraso_partida": "mean"})
sbrj_partidas.sort_index()

df_sbrj = df_sbrj.merge(sbrj_partidas, how="inner", on="timestamp")
df_sbrj = df_sbrj.merge(sbrj_chegadas, how="inner", on="timestamp")

cat_atraso_partida = pd.cut(df_sbrj["atraso_partida"], bins=[0, 10, 30, 60, 9999], labels=["baixo atraso", "médio atraso", "alto atraso", "altíssimo atraso"], include_lowest=True)
cat_atraso_chegada = pd.cut(df_sbrj["atraso_chegada"], bins=[0, 10, 30, 60, 9999], labels=["baixo atraso", "médio atraso", "alto atraso", "altíssimo atraso"], include_lowest=True)

print("----- Crosstab nível de nuvem x atraso partida -----")
print(pd.crosstab(df_sbrj["nivel_nuvem"], cat_atraso_partida).transpose())
print("----- Crosstab nível de nuvem x atraso chegada -----")
print(pd.crosstab(df_sbrj["nivel_nuvem"], cat_atraso_chegada).transpose())

print("----- Crosstab categoria do vento x atraso partida -----")
print(pd.crosstab(df_sbrj["cat_vento"], cat_atraso_partida).transpose())
print("----- Crosstab categoria do vento x atraso chegada -----")
print(pd.crosstab(df_sbrj["cat_vento"], cat_atraso_chegada).transpose())

print("""
5. Calculando a diferença entre a temperatura e o ponto de orvalho temos um valor
que quanto mais baixo, maior chance de chuva. Quando a diferença é zero, temos
100% de chance de chuva. Verifique se esta diferença tem influência nos atrasos.
""")

diff_temp = df_sbrj["temperature"] - df_sbrj["dew_point"]

print(pd.crosstab(diff_temp, [df_sbrj["nivel_nuvem"], df_sbrj["atraso_chegada"]]))
