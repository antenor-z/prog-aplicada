# Resumo
Este trabalho tem como objetivo mostrar quais condições climáticas mudam os
horários de voo.

Para responder esta pergunta usamos três dataframes: um com as condições 
climáticas em um aeroporto, o outro com as partidas deste aeroportos e o último
com as chegadas de um aeroporto.

O aeroporto escolhido será o Santos Dumont. Este aeroporto possui código ICAO
SBRJ que será usado ao longo do trabalho para se referir a este aeroporto.

# Bases de dados

## Base: dataset_SBRJ.xlsx

Possui as informações históricas metereológicas. É obtido acessando o endereço:
"https://aero.a4barros.com/history/SBRJ/" e clicando na opção "Baixar como 
planilha".

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

## Base: 2024-10-29-SBRJ-arrivals.xlsx e 2024-10-29-SBRJ-departures.xlsx

Contém dados de pousos e decolagens do SBRJ. 

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
