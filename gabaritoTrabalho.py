import pandas as pd
import matplotlib.pyplot as plt

df_sbrj: pd.DataFrame = pd.read_excel("dataset_SBRJ.xlsx")

print(df_sbrj)

print("\n-----------------------------------------------------")
print("1) Limpeza de dados")
print("""
1.a) Para valores ausentes de vento substitua pelo valor médio a 
velocidade e a direção por zero. (satisfaz req 2)""")
df_sbrj["wind_direction"].fillna(0, inplace=True)
df_sbrj["wind_speed"].fillna(df_sbrj["wind_speed"].mean(), inplace=True)
print(df_sbrj)


print("""
1.b) A velocidade do vento está expressa em nós (milhas nauticas por hora) converta
para km/h (satisfaz req 3)""")
def kts_to_km_h(kts):
    return kts * 1.852
df_sbrj.wind_speed = df_sbrj["wind_speed"].apply(kts_to_km_h)

print("\n-----------------------------------------------------")
print("2) Conhecendo o dataset")
print("2.a) Em todo período mostre qual foi a temperatura máxima")
print(df_sbrj["temperature"].max())

print("2.b) Em qual(quais) momento(s) a temperatura chegou no máximo?")
filtro_max_temp = df_sbrj["temperature"] == df_sbrj["temperature"].max()
print(df_sbrj.loc[filtro_max_temp]["timestamp"])

print("2.c) Qual foi a maior diferenca entre a temperatura e o ponto de orvalho")
print("Quanto maior a diferença menos chance de chuva.")
dif_temperatura_orvalho = abs(df_sbrj["temperature"] - df_sbrj["dew_point"])
print(dif_temperatura_orvalho.max())

print("""2.d) Crie a coluna dif_temp_orvalho com esta diferença e exiba uma categorização
'pode chover' com True se a diferença for dois graus ou menos e False caso a
diferença seja maior que dois graus""")
df_sbrj["dif_temp_orvalho"] = dif_temperatura_orvalho
cat_pode_chover = pd.cut(df_sbrj["dif_temp_orvalho"], 
       bins=[0, 2, df_sbrj["dif_temp_orvalho"].max()],
       labels=["True", "False"])
df_sbrj["pode_chover"] = cat_pode_chover
print(df_sbrj)

print("""2.d) Crie a coluna nivel_visibilidade usando as categorias muito baixo, baixo, 
médio, alto. Use a função pd.cut com intervalos igualmente espaçados""")
cat_nivel_visibilidade = pd.cut(df_sbrj["visibility"], 
       bins=4,
       labels=["Muito baixo", "Baixo", "Médio", "Alto"])
df_sbrj["nivel_visibilidade"] = cat_nivel_visibilidade
print(df_sbrj)

print("""2.f) Para temperatura, vento e visibilidade, mostre o mínimo, max, média,
       variância. Coloque nas linhas dos dados e nas colunas as métricas (satisfaz req 8a)""")
print(df_sbrj.agg(
    {"temperature": ["min", "max", "mean", "var"], 
     "wind_speed": ["min", "max", "mean", "var"],
     "visibility": ["min", "max", "mean", "var"],
     }).transpose())

print("""2.g) Agrupe os timestamps por dia e exiba as mesmas estatísticas
      do exercício anterior. (satisfaz req 8b)""")

df_sbrj["dia"] = pd.to_datetime(df_sbrj["timestamp"]).dt.date
df_diario = df_sbrj.groupby("dia").agg(
    {"temperature": ["min", "max", "mean", "var"], 
     "wind_speed": ["min", "max", "mean", "var"],
     "visibility": ["min", "max", "mean", "var"]}
)
print(df_diario)

print("""2.h) Qual foi o dia mais quente e o mais frio? Considere a temperatura média do dia.""")
print(df_diario["temperature"]["mean"].idxmax(), "com temperatura de", df_diario["temperature"]["mean"].max())
print(df_diario["temperature"]["mean"].idxmin(), "com temperatura de", df_diario["temperature"]["mean"].min())

print("\n-----------------------------------------------------")
print("3) Plotagem de gráficos")
print("""3.a) Plote em um gráfico de linha a temperatura média diária e a
      velocidade média do vento diária. Parece existir relação entre o vento e a temperatura?""")

# Resp: Sim

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(df_diario["temperature"]["mean"], label="Temperatura Média (°C)")
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(df_diario["wind_speed"]["mean"], label="Velocidade Média do Vento (km/h)", color="g")
ax2.set_ylabel("Velocidade Média do Vento (km/h)", color='g')
ax2.tick_params(axis='y', labelcolor='g')

fig.tight_layout()
plt.show()


