import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime
pd.set_option('display.max_rows', None)

ICAO = "SBGL"
df_aeroporto: pd.DataFrame = pd.read_excel(f"aeroportos/dataset_{ICAO}.xlsx")


print("\n----------------------------------------------------------------------")
print("""
1. Quando os valores de vento não aparecem, significa que não há vento. Complete 
os valores ausentes de velocidade do vento com zero e os valores ausentes de 
direção com com a mediana das direções. Completar com a mediana é usada para que
ouliers não afetem algum cálculo de média feito com a direção do vento.
Mostre os 10 maiores e os 10 menores valores ordenados por velocidade de vento.
""")

df_aeroporto.timestamp = pd.to_datetime(df_aeroporto.timestamp, utc=True)
df_aeroporto.set_index("timestamp", inplace=True)
df_aeroporto.fillna(
    {"wind_direction": df_aeroporto["wind_direction"].median(), "wind_speed": 0}, 
    inplace=True)

vento_sorted = df_aeroporto.sort_values("wind_speed", ascending=False)
print(pd.concat([vento_sorted.head(10), vento_sorted.tail(10)]))

print("\n----------------------------------------------------------------------")
print("""
2. Os valores de nuvens few (poucas), scatered (espalhadas), broken (muitas) e 
overcast (encoberto) são listas de números separados por vírgula com a altitude 
de cada nuvem. Por exemplo, few com valor "10000,12000" indicam poucas nuvens em 
10 mil pés e 12 mil pés.

Crie uma coluna 'nivel_nuvem' com o valor do tipo de nuvem mais encoberto 
seguindo a ordem few < scatered < broken < overcast. Para garantir que as nuvens 
realmente afetam o aeroporto, considere APENAS nuvens abaixo de 10 mil pés.

Qual o mais nebuloso (mais fechado) tipo de formação para cada valor de temperatura?
Parece haver relação entre a nebulosidade e a temperatura?
""")


# Isto serve para filtrar valores menores que 10000 em vários formatos
# A regra é retornar true se pelo menos um dos valores for menor que 10000
# Por exemplo: 8000,15000 = true
#              2000       = true
#              12000,20000= false
#              15000      = false
def altitude_menor_10000(value):
    if isinstance(value, str):
        return any(int(num) < 10000 for num in value.split(','))
    elif isinstance(value, int) or isinstance(value, float):
        return value < 10000
    return False


df_aeroporto['filtro_few'] = df_aeroporto['clouds_few'].apply(altitude_menor_10000)
df_aeroporto['filtro_scattered'] = df_aeroporto['clouds_scattered'].apply(altitude_menor_10000)
df_aeroporto['filtro_broken'] = df_aeroporto['clouds_broken'].apply(altitude_menor_10000)
df_aeroporto['filtro_overcast'] = df_aeroporto['clouds_overcast'].apply(altitude_menor_10000)

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

df_aeroporto['nivel_nuvem'] = df_aeroporto.apply(nivel_nuvem, axis=1)

df_aeroporto = df_aeroporto.drop(columns=['filtro_few', 'filtro_scattered', 'filtro_broken', 'filtro_overcast'])
print("----- Pior nível de nuvem abaixo de 10 mil por temperatura -----")
print(df_aeroporto.groupby(["temperature"]).agg({"nivel_nuvem": "max"}).replace(
    {4: "overcast",
     3: "broken",
     2: "scattered",
     1: "few"}))

# Eu só consigo fazer o replace permanente aqui porque no comando de agg eu tenho
# que pegar o valor máximo. Só consigo fazer isto com números
df_aeroporto["nivel_nuvem"] = df_aeroporto["nivel_nuvem"].replace(
    {4: "overcast",
     3: "broken",
     2: "scattered",
     1: "few"})

print("----- Tabela de frequencia percentual de tipos de nuvem -----")
print(df_aeroporto["nivel_nuvem"].value_counts(normalize=True) * 100)
plt.close()
df_aeroporto["nivel_nuvem"].value_counts(normalize=True).plot.bar()
plt.xticks(rotation=0) # Fazer a legendas ficarem visiveis
plt.title(f"{ICAO} - Distribuição das Categorias de Nuvem")
plt.savefig(f"{ICAO}-cat-nuvem.png")
#print(df_aeroporto)

print("\n----------------------------------------------------------------------")
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

Esta é chamada de Escala de Beaufort.

3.1. Faça uma tabela de frequências destas categorias e mostre em um gráfico pizza.
Qual é o tipo de vento mais presente?

3.2. Mostre uma tabela de frequência com o cruzamento das categorias de vento com os
valores de temperatura. Em qual faixa de temperatura ocorrem mais ventos?

3.3. Para cada faixa de vento mostre temperatura mínima, média e máxima. 
Parece haver relação entre velocidade do vento e temperatura?
""")

print("item 3.1")
def to_kmh(wind):
    return wind * 1.852

df_aeroporto["wind_speed"] = df_aeroporto["wind_speed"].apply(to_kmh)
df_aeroporto["cat_vento"] = pd.cut(
    df_aeroporto.wind_speed, 
    bins=[0, 2, 5, 11, 19, 28, 38, 49, 61, 74, 88, 102, 117, 9999],
    labels=["Calmo", "Bafagem", "Brisa leve", "Brisa fraca", "Brisa Moderada",
            "Brisa forte", "Vento fresco", "Vento forte", "Ventania", "Ventania fote",
            "Tempestade", "Tempestade violenta", "Furacao"],
    include_lowest=True
)

print("----- tabela de frequencia numérica de tipos de vento -----")
print(df_aeroporto["cat_vento"].value_counts())


plt.close()
df_aeroporto["cat_vento"].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
plt.title("Distribuição das Categorias de Vento")
plt.savefig("dist-cat-vento.png")

print("Item 3.2")
tabela_freq = pd.crosstab(df_aeroporto["cat_vento"], df_aeroporto["temperature"]).transpose()
tabela_freq["total"] = tabela_freq.sum(axis=1)
print(tabela_freq.sort_values("total", ascending=False))

print("Item 3.3")
tabela_freq_2 = (df_aeroporto.groupby("cat_vento", observed=True)
      .agg({"temperature": ["min", "max", "mean"]}).
      dropna())

tabela_freq_2["amplitude"] = tabela_freq_2["temperature"]["max"]- tabela_freq_2["temperature"]["min"]
print(tabela_freq_2)

print("\n----------------------------------------------------------------------")
print(
"""
4. Junte os dataframes de dados de voo de um mesmo aeroporto.
Faça um Merge da tabela de condições meteorológicas com os atrasos. Crie as 
colunas atraso_chegada e atraso_partida.

Faça o cruzamento de frequência entre o nível do vento e os atrasos e entre
a pior formação de nuvens e os atrasos. Parece haver uma correlação?
"""
)

galeao_partidas = pd.DataFrame()
galeao_chegadas = pd.DataFrame()

todos_aeroportos_partidas = pd.DataFrame()
todos_aeroportos_chegadas = pd.DataFrame()

# Como é possível ver na pasta "voos" são 124 arquivos de excel.
# Pegando todos os arquivos com os voos do aeroportos e organizando
# em dois dataframes todos_aeroportos_partidas e todos_aeroportos_chegadas
# Cada um tem as colunas: ICAO, timestamp, flight_icao, atraso_chegada (ou partida)

# Nesta questão só o Galeão (SBGL) é usado. Mas carreguei todos logo porque mais
# na frente será feita comparação entre aeroportos
for ICAO in ["SBRJ", "SBGR", "SBGL", "SBSP"]:
    for arquivo in os.listdir("voos"):
        if ICAO in arquivo:
            if "departures" in arquivo:
                partidas_do_dia = pd.read_excel("voos/" + arquivo)
                partidas_do_dia["ICAO"] = ICAO
                todos_aeroportos_partidas = pd.concat([todos_aeroportos_partidas, partidas_do_dia])
            elif "arrivals" in arquivo:
                chegadas_do_dia = pd.read_excel("voos/" + arquivo)
                chegadas_do_dia["ICAO"] = ICAO
                todos_aeroportos_chegadas = pd.concat([todos_aeroportos_chegadas, chegadas_do_dia])

todos_aeroportos_partidas = todos_aeroportos_partidas[["ICAO", "departure_scheduled", "flight_icao", "departure_delay"]]
todos_aeroportos_chegadas = todos_aeroportos_chegadas[["ICAO", "arrival_scheduled", "flight_icao", "arrival_delay"]]
todos_aeroportos_partidas.rename({"departure_delay": "atraso_partida", "departure_scheduled": "timestamp"}, axis=1, inplace=True)
todos_aeroportos_chegadas.rename({"arrival_delay": "atraso_chegada", "arrival_scheduled": "timestamp"}, axis=1, inplace=True)
todos_aeroportos_partidas["timestamp"] = pd.to_datetime(todos_aeroportos_partidas.timestamp, utc=True)
todos_aeroportos_chegadas["timestamp"] = pd.to_datetime(todos_aeroportos_chegadas.timestamp, utc=True)
todos_aeroportos_partidas.set_index("timestamp", inplace=True)
todos_aeroportos_chegadas.set_index("timestamp", inplace=True)

filtro_chegada_galeao = todos_aeroportos_chegadas["ICAO"] == "SBGL"
galeao_chegadas = todos_aeroportos_chegadas[filtro_chegada_galeao]
filtro_partida_galeao = todos_aeroportos_partidas["ICAO"] == "SBGL"
galeao_partidas = todos_aeroportos_partidas[filtro_partida_galeao]

# Usando a mediana para mascarar valores ausentes, porque é menos sensível à outliers
galeao_chegadas.fillna({"atraso_chegada": galeao_chegadas["atraso_chegada"].median()}, inplace=True)
galeao_partidas.fillna({"atraso_partida": galeao_partidas["atraso_partida"].median()}, inplace=True)

galeao_partidas.index = galeao_partidas.index.floor('h')
galeao_chegadas.index = galeao_chegadas.index.floor('h')

galeao_partidas = galeao_partidas.groupby("timestamp").agg({"atraso_partida": "mean"})
galeao_partidas.sort_index(inplace=True)
galeao_chegadas = galeao_chegadas.groupby("timestamp").agg({"atraso_chegada": "mean"})
galeao_chegadas.sort_index(inplace=True)

df_aeroporto = df_aeroporto.merge(galeao_partidas, how="inner", on="timestamp")
df_aeroporto = df_aeroporto.merge(galeao_chegadas, how="inner", on="timestamp")

cat_atraso_partida = pd.cut(df_aeroporto["atraso_partida"], bins=[0, 10, 30, 60, 9999], labels=["baixo atraso", "médio atraso", "alto atraso", "altíssimo atraso"], include_lowest=True)
cat_atraso_chegada = pd.cut(df_aeroporto["atraso_chegada"], bins=[0, 10, 30, 60, 9999], labels=["baixo atraso", "médio atraso", "alto atraso", "altíssimo atraso"], include_lowest=True)

print("----- Crosstab nível de nuvem x atraso partida -----")
print(pd.crosstab(df_aeroporto["nivel_nuvem"], cat_atraso_partida).transpose())
print("----- Crosstab nível de nuvem x atraso chegada -----")
print(pd.crosstab(df_aeroporto["nivel_nuvem"], cat_atraso_chegada).transpose())
print("----- Crosstab categoria do vento x atraso partida -----")
print(pd.crosstab(df_aeroporto["cat_vento"], cat_atraso_partida).transpose())
print("----- Crosstab categoria do vento x atraso chegada -----")
print(pd.crosstab(df_aeroporto["cat_vento"], cat_atraso_chegada).transpose())

print("\n----------------------------------------------------------------------")
print("""
5. Calculando a diferença entre a temperatura e o ponto de orvalho temos um valor
que quanto mais baixo, maior chance de chuva. Quando a diferença é zero, temos
100% de chance de chuva. Retire valores maiores de 10 graus, porque são outliers
e filtre por tempo muito nebuloso ou visibiliade menor que 5km.
""")

df_aeroporto["diff_temp"] = df_aeroporto["temperature"] - df_aeroporto["dew_point"]
df_aeroporto["diff_temp"] = df_aeroporto["temperature"] - df_aeroporto["dew_point"]

filtro_maior_10 = df_aeroporto["diff_temp"] <= 10
df_aeroporto = df_aeroporto[filtro_maior_10]

filtro_muito_adverso = (df_aeroporto["nivel_nuvem"] == "overcast") | (df_aeroporto["visibility"] < 5000)
df_aeroporto_adverso = df_aeroporto[filtro_muito_adverso]
df_aeroporto_adverso["atraso"] = round(df_aeroporto_adverso["atraso_chegada"] + df_aeroporto_adverso["atraso_partida"] / 2)
cross = pd.crosstab(df_aeroporto_adverso["diff_temp"] , [df_aeroporto_adverso["nivel_nuvem"], df_aeroporto_adverso["atraso"]])
cross["total_atrasos"] = cross.sum(axis=1)
print(cross)

print(
"""
6. Crie uma tabela no seguinte formato em que cada coluna é um aeroporto e
cada linha é uma hora. Como valores, temos a média de atraso naquele aeroporto
naquela hora. Mostre apenas as linhas que possuem atrasos maiores que 1h.
Destes qual aeroporto tem o maior atraso acumulado?
""")
print("----- Atraso médio por hora das partidas ----- ")
todos_aeroportos_partidas.index = todos_aeroportos_partidas.index.floor('h')
todos_aeroportos_partidas.groupby("timestamp").agg({"atraso_partida": "mean"})
atraso_partidas = pd.crosstab(todos_aeroportos_partidas.index, 
                              todos_aeroportos_partidas.ICAO, 
                              todos_aeroportos_partidas.atraso_partida, 
                              aggfunc="mean").fillna(0)

filtro_acima_30_min = atraso_partidas.max(axis=1) > 60
atraso_partidas_mais_30_min = atraso_partidas[filtro_acima_30_min]
print(atraso_partidas_mais_30_min)


print("----- Atraso médio por hora das chegadas ----- ")
todos_aeroportos_chegadas.index = todos_aeroportos_chegadas.index.floor('h')
todos_aeroportos_chegadas.groupby("timestamp").agg({"atraso_chegada": "mean"})
atraso_chegadas = pd.crosstab(todos_aeroportos_chegadas.index, 
                              todos_aeroportos_chegadas.ICAO, 
                              todos_aeroportos_chegadas.atraso_chegada, 
                              aggfunc="mean").fillna(0)

filtro_acima_30_min = atraso_chegadas.max(axis=1) > 60
atraso_chegadas_mais_30_min = atraso_chegadas[filtro_acima_30_min]
print(atraso_chegadas_mais_30_min)

somas_atrasos_partidas = todos_aeroportos_partidas.groupby('ICAO')['atraso_partida'].sum()
somas_atrasos_chegadas = todos_aeroportos_chegadas.groupby('ICAO')['atraso_chegada'].sum()

pior_atraso_partida = todos_aeroportos_partidas.groupby("ICAO")['atraso_partida'].max()
pior_atraso_chegada = todos_aeroportos_chegadas.groupby("ICAO")['atraso_chegada'].max()

soma_atrasos_df = pd.DataFrame({
    'atraso_partida_total': somas_atrasos_partidas,
    'pior_atraso_partida': pior_atraso_partida,
    'atraso_chegada_total': somas_atrasos_chegadas,
    'pior_atraso_chegada': pior_atraso_chegada,
}).fillna(0) 

print(soma_atrasos_df)

print("""
Qual foi o pior atraso no aeroporto de congonhas no último dia de outubro?   
""")
filtro_sbsp = todos_aeroportos_partidas["ICAO"] == "SBSP"
filtro_dia = todos_aeroportos_partidas.index.date == pd.to_datetime('2024-10-31').date()

print(todos_aeroportos_partidas[filtro_sbsp & filtro_dia].max())
