import pandas as pd
import matplotlib.pyplot as plt

df_sbrj: pd.DataFrame = pd.read_excel("dataset_SBRJ.xlsx")


print("\n----------------------------------------------------------------------")
print("""
1. Quanto os valores de vento não aparecem, significa que não há vento. Complete 
os valores ausentes de velocidade do vento com zero e os valores ausentes de 
direção com zero. Mostre os 20 primeiros valores ordenados por velocidade de vento.
""")

df_sbrj.timestamp = pd.to_datetime(df_sbrj.timestamp)
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

Qual o pior (mais fechado) tipo de formação para cada valor de temperatura?
""")



def altitude_menor_10000(value):
    if isinstance(value, str):
        return any(int(num) < 10000 for num in value.split(','))
    elif isinstance(value, int) or isinstance(value, float):
        return value < 10000
    return False

filtro_few = df_sbrj['clouds_few'].apply(altitude_menor_10000)
filtro_scattered = df_sbrj['clouds_scattered'].apply(altitude_menor_10000)
fitro_broken = df_sbrj['clouds_broken'].apply(altitude_menor_10000)
fitro_overcast = df_sbrj['clouds_overcast'].apply(altitude_menor_10000)

print(fitro_overcast)

