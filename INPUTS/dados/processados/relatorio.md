# Relatório — FAA Wildlife Strikes

- linhas na planilha: 360,384; colunas: 102
- de 2017 a 2025: 159,245
- sem nível de dano informado (removidas): 65,745
- sem fase do voo (carcaças sem relato; removidas): 20,623

## Valores originais (top 15) — conferir se os agrupamentos cobrem tudo

### TIME_OF_DAY
```
TIME_OF_DAY
Day        38850
Night      23363
<vazio>     5405
Dusk        3022
Dawn        2237
```

### PHASE_OF_FLIGHT
```
PHASE_OF_FLIGHT
Approach        34211
Landing Roll    13722
Climb            8865
Take-off Run     8663
En Route         2816
Departure        1806
Descent          1266
Local             647
Arrival           566
Taxi              284
Parked             31
```

### SKY
```
SKY
No Cloud      28936
Some Cloud    19003
<vazio>       16916
Overcast       8022
```

### PRECIPITATION
```
PRECIPITATION
<vazio>            69283
Rain                2599
Fog                  591
Snow                 266
Fog, Rain             93
None, Snow            13
None, Rain            12
Rain, Snow             9
Fog, Snow              6
Fog, None              4
Fog, Rain, Snow        1
```

### AC_MASS
```
AC_MASS
4          52730
3           7780
1           5898
2           5192
5            816
<vazio>      461
```

### TYPE_ENG
```
TYPE_ENG
D          61075
A           5965
F           2616
C           2613
<vazio>      556
B             49
Y              2
E              1
```

### SIZE
```
SIZE
Small      42321
<vazio>    17641
Medium      8614
Large       4301
```

### NUM_STRUCK
```
NUM_STRUCK
1                64928
2-10              7537
11-100             337
<vazio>             65
More than 100       10
```

### WARNED
```
WARNED
Unknown    36942
Yes        19190
No         16745
```

### DAMAGE_LEVEL
```
DAMAGE_LEVEL
N     67243
M?     4472
M       742
S       403
D        17
```

### EFFECT
```
EFFECT
<vazio>                                          68011
Precautionary Landing                             3221
Aborted Take-off                                   809
Other                                              467
Other, Precautionary Landing                       249
Engine Shutdown                                     65
Engine Shutdown, Precautionary Landing              20
Engine Shutdown, Other, Precautionary Landing       12
Aborted Take-off, Engine Shutdown                   10
Aborted Take-off, Other                              9
Engine Shutdown, Other                               4
```

### ING_ENG1
```
ING_ENG1
0    71700
1     1177
```

### Espécies em 'morcego' (top 15)
```
SPECIES
Brazilian free-tailed bat    490
Eastern red bat              200
Vesper bats                  122
Hoary bat                     83
Free-tailed bats              69
Big brown bat                 55
Evening bat                   52
Silver-haired bat             38
Seminole bat                  21
Little brown bat              21
Northern yellow bat           11
Pallas's mastiff bat           7
Egyptian free-tailed bat       4
Tri-colored bat                3
Big free-tailed bat            2
```

### Espécies em 'terrestre' (top 15)
```
SPECIES
White-tailed deer          264
Coyote                     206
Black-tailed jackrabbit     56
Striped skunk               48
Red fox                     43
Virginia opossum            40
White-tailed jackrabbit     28
Woodchuck                   27
Raccoon                     21
Turtles                     18
Green iguana                14
Gopher tortoise             11
Rabbits                     10
Foxes                        8
Mule deer                    8
```

## Base final: 72,877 colisões, 14 nós (+ nivel_dano extra)

## Nível de dano por ano (%)
```
nivel_dano  grave  leve  nenhum
ano                            
2017          0.7   8.3    91.0
2018          0.7   7.8    91.6
2019          0.7   7.8    91.5
2020          0.8   8.2    91.0
2021          0.5   8.0    91.5
2022          0.6   7.1    92.3
2023          0.7   6.1    93.2
2024          0.4   6.5    93.1
2025          0.4   6.2    93.4
```

### estacao
```
nivel_dano  total  %grave  %leve  %nenhum
estacao                                  
inverno      6956     0.9   12.9     86.1
outono      25385     0.6    7.2     92.2
primavera   16681     0.7    7.8     91.5
verao       23855     0.3    5.0     94.7
total       72877     0.6    7.2     92.3
```

### periodo
```
nivel_dano    total  %grave  %leve  %nenhum
periodo                                    
amanhecer      2237     0.4    7.3     92.2
anoitecer      3022     0.6    8.7     90.7
desconhecido   5405     0.4    7.3     92.2
dia           38850     0.6    7.3     92.2
noite         23363     0.7    6.7     92.6
total         72877     0.6    7.2     92.3
```

### fase_voo
```
nivel_dano         total  %grave  %leve  %nenhum
fase_voo                                        
aproximacao        36043     0.3    6.9     92.8
corrida_decolagem   8663     0.3    6.3     93.4
corrida_pouso      13722     0.2    3.6     96.1
rota                3463     4.8   14.0     81.3
solo_taxi            315     0.3    1.9     97.8
subida             10671     0.8   11.1     88.1
total              72877     0.6    7.2     92.3
```

### altura
```
nivel_dano    total  %grave  %leve  %nenhum
altura                                     
alta          11082     0.8   11.1     88.1
baixa         11340     0.2    6.8     92.9
desconhecido  16294     0.5    5.7     93.8
media         11430     1.5   10.8     87.7
solo          22731     0.3    4.6     95.1
total         72877     0.6    7.2     92.3
```

### ceu
```
nivel_dano      total  %grave  %leve  %nenhum
ceu                                          
algumas_nuvens  19003     0.4    7.4     92.2
desconhecido    16916     0.7    6.1     93.1
encoberto        8022     0.4    6.9     92.7
sem_nuvens      28936     0.6    7.6     91.7
total           72877     0.6    7.2     92.3
```

### massa_aeronave
```
nivel_dano      total  %grave  %leve  %nenhum
massa_aeronave                               
desconhecido      461     1.5   10.4     88.1
leve            11090     2.7   17.2     80.1
media            7780     0.3    9.0     90.6
pesada          53546     0.2    4.8     95.1
total           72877     0.6    7.2     92.3
```

### motor
```
nivel_dano    total  %grave  %leve  %nenhum
motor                                      
desconhecido    559     4.1   14.3     81.6
helicoptero    2616     4.9    8.2     86.9
jato          61124     0.2    5.4     94.4
pistao         5965     2.2   21.0     76.8
turboelice     2613     1.1   13.8     85.1
total         72877     0.6    7.2     92.3
```

### animal
```
nivel_dano  total  %grave  %leve  %nenhum
animal                                   
ave         70780     0.5    7.0     92.5
morcego      1194     0.1    1.3     98.6
terrestre     903     5.6   25.2     69.1
total       72877     0.6    7.2     92.3
```

### tamanho_animal
```
nivel_dano      total  %grave  %leve  %nenhum
tamanho_animal                               
desconhecido    17641     0.3    4.5     95.2
grande           4301     4.6   39.4     56.0
medio            8614     1.3   17.8     80.9
pequeno         42321     0.1    2.8     97.1
total           72877     0.6    7.2     92.3
```

### qtd_atingida
```
nivel_dano    total  %grave  %leve  %nenhum
qtd_atingida                               
2_a_10         7537     1.0   10.9     88.1
desconhecido     65    23.1   16.9     60.0
mais_de_10      347     0.3   15.0     84.7
um            64928     0.5    6.7     92.8
total         72877     0.6    7.2     92.3
```

### avisado
```
nivel_dano    total  %grave  %leve  %nenhum
avisado                                    
desconhecido  36942     0.5    6.1     93.4
nao           16745     0.9    9.5     89.6
sim           19190     0.4    7.2     92.4
total         72877     0.6    7.2     92.3
```

### ingestao_motor
```
nivel_dano      total  %grave  %leve  %nenhum
ingestao_motor                               
nao             70637     0.5    6.6     92.8
sim              2240     1.6   23.5     74.9
total           72877     0.6    7.2     92.3
```

### houve_dano
```
nivel_dano  total  %grave  %leve  %nenhum
houve_dano                               
nao         67243     0.0    0.0    100.0
sim          5634     7.5   92.5      0.0
total       72877     0.6    7.2     92.3
```

### efeito_voo
```
nivel_dano          total  %grave  %leve  %nenhum
efeito_voo                                       
decolagem_abortada    828     1.6   15.0     83.5
desligamento_motor    101    14.9   50.5     34.7
nenhum              68011     0.2    5.6     94.2
outro                 467     8.8   31.9     59.3
pouso_precaucao      3470     5.9   30.7     63.3
total               72877     0.6    7.2     92.3
```