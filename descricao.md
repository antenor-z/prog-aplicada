# Resumo
Este trabalho tem como objetivo mostrar quais condições climáticas mudam os
horários de voo.

Para responder esta pergunta usamos três dataframes: um com as condições 
climáticas em um aeroporto, o outro com as partidas deste aeroportos e o último
com as chegadas de um aeroporto.

O aeroporto escolhido será o Santos Dumont. Este aeroporto possui código ICAO
SBRJ que será usado ao longo do trabalho para se referir a este aeroporto.

# Bases de dados

## Base: Tempo

Possui as informações históricas metereológicas. É obtido acessando no endereço:
http://a4barros.com/public/prog-aplicada/tempo.zip

### Descrição de colunas

- wind_direction: Direção **de onde** o ventos sopra em graus;
- wind_speed: Velocidade do vento em nós (milhas nauticas por hora);
- temperature: Temperatura em graus Célsius;
- dew_point: Ponto de orvalho em graus Célsius;
- clouds_few: Alturas em pés separadas por virgulas das altitudes que existem
nuvens few (1/8 a 2/8 do céu) presentes;
- clouds_scattered: O mesmo, mas para nuvens scattered (3/8 a 4/8 do céu);
- clouds_broken: O mesmo, mas para nuvens broken (5/8 a 7/8 do céu);
- clouds_overcast: O mesmo, mas para nuvens overcast (encoberto).

## Base: Voos

Contém dados de pousos e decolagens em vários aeroportos do sudeste.
Pode ser obtida em http://a4barros.com/public/prog-aplicada/voos.zip

### Descrição de colunas

- flight_date: Data no formato YYYY-MM-DD.
- flight_status: status do voo pode ser: active, landed, diverted, scheduled,
cancelled, unknown;
- departure_airport: Nome popular do aeroporto.
- departure_timezone: Fuso horário do aeroporto (ex.: America/Sao_Paulo);
- departure_iata: Código IATA do aeroporto de partida. (ex.: SDU);
- departure_icao: Código ICAO do aeoporto de partida (ex.: SBRJ);
- departure_terminal: Terminal de partida do voo;
- departure_gate: Portão de embarque de onde o voo parte (ex.: C02);
- departure_scheduled: Horário programado para a partida do voo no formato de hora
UTC (YYYY-MM-DDTHH:MM:SS+00:00);
- departure_estimated: Horário estimado para a partida do voo no formato de hora UTC;
- arrival_airport: Nome popular do aeroporto de chegada;
- arrival_timezone: Fuso horário do aeroporto de chegada, no formato de região. Ex.: America/Sao_Paulo;
- arrival_iata: Código IATA do aeroporto de chegada (ex.: GRU);
- arrival_icao: Código ICAO do aeroporto de chegada (ex.: SBGR);
- arrival_terminal: Terminal de chegada do voo;
- arrival_gate: Portão de desembarque onde o voo chega (ex.: A02);
- arrival_baggage: Número da esteira onde as bagagens do voo serão disponibilizadas (ex.: Esteira 04);
- arrival_delay: Atraso na chegada do voo em minutos, considerando o horário programado.
- arrival_scheduled: Horário programado para a chegada do voo no formato de hora 
UTC;
- arrival_estimated: Horário estimado para a chegada do voo no formato de hora UTC;
- airline_name: Nome da companhia aérea operadora do voo (ex.: LATAM Airlines);
- airline_iata: Código IATA da companhia aérea (ex.: LA para LATAM);
- airline_icao: Código ICAO da companhia aérea (ex.: TAM para LATAM);
- flight_number: Número único do voo designado pela companhia aérea (ex.: 1111);
- flight_iata: Código IATA completo do voo, formado pelo código da companhia e o número do voo (ex.: LA1234);
- flight_icao: Código ICAO completo do voo, formado pelo código ICAO da companhia e o número do voo (ex.: TAM1234).

# Perguntas respondidas

1. Quanto os valores de vento não aparecem, significa que não há vento. Complete 
os valores ausentes de velocidade do vento com zero e os valores ausentes de 
direção com zero. Mostre os 20 primeiros valores ordenados por velocidade de vento.

2. Os valores de nuvens few (poucas), scatered (espalhadas), broken (muitas) e 
overcast (encoberto) são listas de números separados por vírgula com a altitude 
de cada nuvem. Por exemplo, few com valor "10000,12000" indicam poucas nuvens em 
10 mil pés e 12 mil pés.

Crie uma coluna pior_tipo_nuvem com o valor do tipo de nuvem mais encoberto 
seguindo a ordem few < scatered < broken < overcast. Para garantir que as nuvens 
realmente afetam o aeroporto, considere APENAS nuvens abaixo de 10 mil pés.

Qual o mais nebuloso (mais fechado) tipo de formação para cada valor de temperatura?
Parece haver relação entre a nebulosidade e a temperatura?

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
    * **Tempestade** violenta: 103 a 117km/h
    * **Furacao:** Maior que 118km/h

Está é a chamada de Escala de Beaufort.

3.1. Faça uma tabela de frequências destas categorias e mostre em um gráfico pizza.
Qual é o tipo de vento mais presente?

3.2. Mostre uma tabela de frequência com o cruzamento das categorias de vento com os
valores de temperatura. Em qual facha de temperatura ocorrem mais ventos?

3.3. Para cada faixa de vento mostre temperatura mínima, média, máxima e desvio 
padrão. Parece haver relação entre velocidade do vento e temperatura?

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
a pior formação de nuvens (coluna "pior_tipo_nuvem") e os atrasos. Parece haver
uma correlação?

5. Para um aeroporto é interessante com o vento fique o mais paralelo possível 
com a direção da pista. Isto facilita os pousos e decolagens. 


