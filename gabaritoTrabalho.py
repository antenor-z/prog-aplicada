import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

ICAO = "SBGL"
df_aeroporto: pd.DataFrame = pd.read_excel(f"aeroportos/dataset_{ICAO}.xlsx")


print("\n----------------------------------------------------------------------")
print("""
1. Quando os valores de vento não aparecem, significa que não há vento. Complete 
os valores ausentes de velocidade do vento com zero e os valores ausentes de 
direção com zero. Mostre os 20 primeiros valores ordenados por velocidade de vento.
""")

df_aeroporto.timestamp = pd.to_datetime(df_aeroporto.timestamp, utc=True)
df_aeroporto.set_index("timestamp", inplace=True)
df_aeroporto.fillna({"wind_direction": 0, "wind_speed": 0}, inplace=True)
print(df_aeroporto.sort_values("wind_speed", ascending=False).head(20))

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
print("Nível de nuvem por temperatura")
print(df_aeroporto.groupby(["temperature"]).agg({"nivel_nuvem": "max"}).replace(
    {4: "overcast",
     3: "broken",
     2: "scattered",
     1: "few"}))

# Eu só consigo fazer o replace permanente aqui porque no comando acima eu tenho
# que pegar o valor máximo. Só consigo fazer isto com números
df_aeroporto["nivel_nuvem"] = df_aeroporto["nivel_nuvem"].replace(
    {4: "overcast",
     3: "broken",
     2: "scattered",
     1: "few"})

print("Tabela de frequencia percentual de tipos de nuvem")
print(df_aeroporto["nivel_nuvem"].value_counts(normalize=True) * 100)
df_aeroporto["nivel_nuvem"].value_counts(normalize=True).plot.bar()
plt.title("Distribuição das Categorias de Nuvem")
plt.savefig("Distribuição das Categorias de Nuvem.png")
print(df_aeroporto)


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

3.3. Para cada faixa de vento mostre temperatura mínima, média, máxima e desvio 
padrão. Parece haver relação entre velocidade do vento e temperatura?
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

print("tabela de frequencia numérica de tipos de vento")
print(df_aeroporto["cat_vento"].value_counts())

df_aeroporto["cat_vento"].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
plt.title("Distribuição das Categorias de Vento")
plt.savefig("Distribuição das Categorias de Vento.png")

print("Item 3.2")
print(pd.crosstab(df_aeroporto["cat_vento"], df_aeroporto["temperature"]).transpose())

print("Item 3.3")
print(df_aeroporto.groupby("cat_vento", observed=True)
      .agg({"temperature": ["min", "max", "mean", "std"]}).
      dropna())

print(
"""
4. Junte os dataframes de dados de voo de um mesmo aeroporto. Faça os dataframes 
chegadas_SBRJ e partidas_SBRJ. Crie um dataframe atraso_chegadas_SBRJ com os 
timestamps agrupados por hora e a média de tempo de atraso. Ou seja, para cada 
hora, teremos o tempo médio de atraso. Faça o mesmo para as partidas criando o 
dataframe atraso-partidas-SBRJ.

Faça um Merge da tabela de condições meteorológicas com os atrasos. Crie as 
colunas atraso_chegada e atraso_partida.

Faça o cruzamento de frequência entre o nível do vento e os atrasos e entre
a pior formação de nuvens e os atrasos. Parece haver uma correlação?
"""
)

aeroporto_partidas = pd.DataFrame()
aeroporto_chegadas = pd.DataFrame()

# Abrindo os datasets do Santos Dumont e concatenando em chegadas
# e partidas
for arquivo in os.listdir("voos"):
    if ICAO in arquivo:
        if "departures" in arquivo:
            partidas_do_dia = pd.read_excel("voos/" + arquivo)
            aeroporto_partidas = pd.concat([aeroporto_partidas, partidas_do_dia])
        elif "arrivals" in arquivo:
            chegadas_do_dia = pd.read_excel("voos/" + arquivo)
            aeroporto_chegadas = pd.concat([aeroporto_chegadas, chegadas_do_dia])

aeroporto_partidas = aeroporto_partidas[["departure_scheduled", "flight_icao", "departure_delay"]]
aeroporto_chegadas = aeroporto_chegadas[["arrival_scheduled", "flight_icao", "arrival_delay"]]
aeroporto_partidas.rename({"departure_delay": "atraso_partida", "departure_scheduled": "timestamp"}, axis=1, inplace=True)
aeroporto_chegadas.rename({"arrival_delay": "atraso_chegada", "arrival_scheduled": "timestamp"}, axis=1, inplace=True)

# Usando a mediana para mascarar valores ausentes, porque é menos sensível à outliers
aeroporto_chegadas["atraso_chegada"] = (aeroporto_chegadas["atraso_chegada"]
.fillna(aeroporto_chegadas["atraso_chegada"].median()))

aeroporto_partidas["atraso_partida"] = (aeroporto_partidas["atraso_partida"]
.fillna(aeroporto_partidas["atraso_partida"].median()))


aeroporto_partidas["timestamp"] = pd.to_datetime(aeroporto_partidas.timestamp, utc=True)
aeroporto_chegadas["timestamp"] = pd.to_datetime(aeroporto_chegadas.timestamp, utc=True)
aeroporto_partidas.set_index("timestamp", inplace=True)
aeroporto_chegadas.set_index("timestamp", inplace=True)

# Setando o índice para ter apenas a hora cheia
aeroporto_partidas.index = aeroporto_partidas.index.floor('h')
aeroporto_chegadas.index = aeroporto_chegadas.index.floor('h')

aeroporto_partidas = aeroporto_partidas.groupby("timestamp").agg({"atraso_partida": "mean"})
aeroporto_partidas.sort_index()

df_aeroporto = df_aeroporto.merge(aeroporto_partidas, how="inner", on="timestamp")
df_aeroporto = df_aeroporto.merge(aeroporto_chegadas, how="inner", on="timestamp")

cat_atraso_partida = pd.cut(df_aeroporto["atraso_partida"], bins=[0, 10, 30, 60, 9999], labels=["baixo atraso", "médio atraso", "alto atraso", "altíssimo atraso"], include_lowest=True)
cat_atraso_chegada = pd.cut(df_aeroporto["atraso_chegada"], bins=[0, 10, 30, 60, 9999], labels=["baixo atraso", "médio atraso", "alto atraso", "altíssimo atraso"], include_lowest=True)
cat_atraso_partida = pd.cut(df_aeroporto["atraso_partida"], bins=[0, 10, 30, 60, 9999], labels=["baixo atraso", "médio atraso", "alto atraso", "altíssimo atraso"], include_lowest=True)
cat_atraso_chegada = pd.cut(df_aeroporto["atraso_chegada"], bins=[0, 10, 30, 60, 9999], labels=["baixo atraso", "médio atraso", "alto atraso", "altíssimo atraso"], include_lowest=True)

print("----- Crosstab nível de nuvem x atraso partida -----")
print(pd.crosstab(df_aeroporto["nivel_nuvem"], cat_atraso_partida).transpose())
print(pd.crosstab(df_aeroporto["nivel_nuvem"], cat_atraso_partida).transpose())
print("----- Crosstab nível de nuvem x atraso chegada -----")
print(pd.crosstab(df_aeroporto["nivel_nuvem"], cat_atraso_chegada).transpose())
print(pd.crosstab(df_aeroporto["nivel_nuvem"], cat_atraso_chegada).transpose())

print("----- Crosstab categoria do vento x atraso partida -----")
print(pd.crosstab(df_aeroporto["cat_vento"], cat_atraso_partida).transpose())
print(pd.crosstab(df_aeroporto["cat_vento"], cat_atraso_partida).transpose())
print("----- Crosstab categoria do vento x atraso chegada -----")
print(pd.crosstab(df_aeroporto["cat_vento"], cat_atraso_chegada).transpose())
print(pd.crosstab(df_aeroporto["cat_vento"], cat_atraso_chegada).transpose())

print("""
5. Calculando a diferença entre a temperatura e o ponto de orvalho temos um valor
que quanto mais baixo, maior chance de chuva. Quando a diferença é zero, temos
100% de chance de chuva. Retire valores maiores de 10 graus. Verifique se esta 
diferença tem influência nos atrasos para cada tipo de nuvem.
      
Repita o procedimento, mas considerando apenas condições muito adversas de tempo.
Visibilidade menor que 5000 e nuvens encobertas.
""")

df_aeroporto["diff_temp"] = df_aeroporto["temperature"] - df_aeroporto["dew_point"]
df_aeroporto["diff_temp"] = df_aeroporto["temperature"] - df_aeroporto["dew_point"]

filtro_maior_10 = df_aeroporto["diff_temp"] <= 10
df_aeroporto = df_aeroporto[filtro_maior_10]
filtro_maior_10 = df_aeroporto["diff_temp"] <= 10
df_aeroporto = df_aeroporto[filtro_maior_10]

print(pd.crosstab(df_aeroporto["diff_temp"] , [df_aeroporto["nivel_nuvem"], df_aeroporto["atraso_chegada"]]))

print("Calculando para condições muito adversas")

filtro_muito_adverso = (df_aeroporto["nivel_nuvem"] == "overcast") & (df_aeroporto["visibility"] < 5000)
df_aeroporto_adverso = df_aeroporto[filtro_muito_adverso]
print(pd.crosstab(df_aeroporto_adverso["diff_temp"] , [df_aeroporto_adverso["nivel_nuvem"], df_aeroporto_adverso["atraso_chegada"]]))

print("Atraso médio", ICAO, (df_aeroporto["atraso_chegada"].mean() + df_aeroporto["atraso_partida"].mean()) / 2)
