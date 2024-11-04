import pandas as pd
import matplotlib.pyplot as plt

df_sbrj: pd.DataFrame = pd.read_excel("dataset_SBRJ.xlsx")


print("\n-----------------------------------------------------")
print("""
1. Quanto os valores de vento não aparecem, significa que não há vento. Complete 
os valores ausentes de velocidade do vento com zero e os valores ausentes de 
direção com zero. Quando ocorreu o vento mais forte, qual foi a velocidade?
""")

df_sbrj.timestamp = pd.to_datetime(df_sbrj.timestamp)
df_sbrj.set_index("timestamp", inplace=True)
df_sbrj.fillna({"wind_direction": 0, "wind_speed": 0}, inplace=True)
ts_vento_max = df_sbrj.wind_speed.idxmax()
print("Quando ocorreu vento máximo", ts_vento_max)
filtro_vento_max = df_sbrj.index == ts_vento_max
print("Valores máximos:", filtro_vento_max)

