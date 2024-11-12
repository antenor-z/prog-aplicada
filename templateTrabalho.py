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

3.3. Parece haver relação entre velocidade do vento e temperatura?
""")


print("\n----------------------------------------------------------------------")
print(
"""
4. Junte os dataframes de dados de voo do aeroporto do Galeão.
Faça um Merge da tabela de condições meteorológicas com os atrasos. Crie as 
colunas atraso_chegada e atraso_partida.

Faça o cruzamento de frequência entre o nível do vento e os atrasos e entre
a pior formação de nuvens e os atrasos. Parece haver uma correlação?
"""
)


print("\n----------------------------------------------------------------------")
print("""
5. Calculando a diferença entre a temperatura e o ponto de orvalho temos um valor
que quanto mais baixo, maior chance de chuva. Quando a diferença é zero, temos
100% de chance de chuva. Retire valores maiores de 10 graus, porque são outliers
e filtre por tempo muito nebuloso ou visibiliade menor que 5km.
""")


print("\n----------------------------------------------------------------------")

print(
"""
6. Crie uma tabela no seguinte formato em que cada coluna é um aeroporto e
cada linha é uma hora. Como valores, temos a média de atraso naquele aeroporto
naquela hora. Mostre apenas as linhas que possuem atrasos maiores que 1h.
Destes qual aeroporto tem o maior atraso acumulado?
""")

print("\n----------------------------------------------------------------------")


print("""
7. Qual foi o pior atraso no aeroporto de congonhas no último dia de outubro?   
""")

print("\n----------------------------------------------------------------------")


print("""
8. Qual o tempo médio de atrasos médios diários do SBGL e qual a correlação com Nível de Nuvem ? """)