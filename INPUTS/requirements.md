# 1. Redes Bayesianas

Redes bayesianas são modelos gráficos probabilísticos que representam um
conjunto de variáveis aleatórias e suas dependências condicionais por
meio de um grafo acíclico dirigido (DAG). Cada nó corresponde a uma
variável e cada aresta codifica uma relação de dependência direta,
enquanto a ausência de arestas expressa independências condicionais.
Associada a cada nó há uma distribuição de probabilidade condicional
(CPT), e o produto dessas distribuições fatora a distribuição conjunta
de todas as variáveis.

Essa estrutura permite raciocínio sob incerteza de forma compacta e
interpretável: dada evidência sobre algumas variáveis, é possível
inferir a distribuição de probabilidade das demais.

Nossa missão aqui é construir, aprender e interpretar uma
rede bayesiana sobre um conjunto de dados, percorrendo o
ciclo completo de modelagem: da definição do problema à explicação das
decisões do modelo. Com relação a esse tema, devem ser realizadas as
tarefas a seguir.

# 2. Escolha dos Dados

Vamos escolher um conjunto de dados tabular para modelar. O
conjunto deve conter, idealmente, menos de 60 variáveis, para manter o
aprendizado estrutural e a inferência tratáveis. Se necessário, podem
ser aplicados métodos de seleção de características para eliminar
features redundantes e diminuir a dimensionalidade.

Prefira domínios com categorias naturais e alguma estrutura de
dependência plausível (por exemplo, dados de saúde, educação ou perfis
socioeconômicos), evitando conjuntos puramente contínuos e densamente
correlacionados, que tendem a produzir redes densas e de difícil
interpretação.

Variáveis contínuas devem ser discretizadas, e o método de discretização
apresentado e justificado.

- O conjunto de dados escolhidos aqui é de um levantamento norte-americano
de colisão de fauna com aeronaves.
- Os dados brutos estão em: INPUTS/dados/brutos
- Os dados tratados estão em: INPUTS/dados/processados
- O script que coleta os dados está em INPUTS/scripts/coletar_birdstrikes.py

# 3. Tarefas

## Tarefa 1

Descreva o domínio dos dados escolhidos e o pré-processamento realizado
(tratamento de valores faltantes, discretização das variáveis contínuas
em três faixas por quantis, codificação das categorias). Formule ao
menos uma pergunta de interesse que a rede bayesiana deveria ser capaz
de responder no contexto do problema.

- O conjunto de dados escolhidos aqui é de um levantamento norte-americano
de colisão de fauna com aeronaves.
- O dicionário dos dados está detalhado em: INPUTS/dados/processados/relatorio.md
- Os dados brutos estão em: INPUTS/dados/brutos
- Os dados tratados estão em: INPUTS/dados/processados

## Tarefa 2

Antes de qualquer aprendizado automático, desenhe manualmente a
estrutura da rede que você julga fazer sentido para o domínio, com base
no conhecimento sobre as variáveis.

Caso a rede seja grande demais para desenhar, não é necessário montar a
rede inteira, foque apenas em algumas relações que você espera
encontrar.

Essa estrutura elicitada será comparada com a estrutura aprendida na
Tarefa 3.

A rede desenhada está em: INPUTS/rede_etapa2.png

## Tarefa 3

Aprenda a estrutura da rede a partir dos dados utilizando dois
algoritmos: o **Hill-Climbing com o score BIC**, e qualquer outro método
de sua escolha.

- Esse outro método à escolha será um dos métodos citados no arquivo
INPUTS/FUND_IA_Chapter_9_RBs_BNSL (1).pdf
- Priorize um método contemplado pela biblioteca pgmpy

O Hill-Climbing está disponível nas principais bibliotecas, e você pode
usar qualquer outro método pronto, de bibliotecas ou algum repositório.

Compare as estruturas aprendidas com a estrutura elicitada manualmente
na Tarefa 2:

-   Onde o algoritmo concordou com a sua intuição?
-   Onde discordou?
-   Discuta possíveis razões para as diferenças.

## Tarefa 4

A partir da estrutura aprendida, estime os parâmetros da rede (as
tabelas de probabilidade condicional).

Normalmente os métodos disponíveis são: máxima verossimilhança e
estimação bayesiana com priors. Utilize o que achar mais pertinente.

Em seguida, utilize a rede para responder às perguntas formuladas na
Tarefa 1 por meio de inferência, explorando consultas com diferentes
evidências.

## Tarefa 5

Escolha uma predição específica da rede e explique-a usando propriedades
da própria rede.

Você pode, por exemplo:

-   Fazer uma análise de sensibilidade para descobrir quais variáveis
    são mais relevantes para aquela predição;
-   Usar a topologia da rede para identificar caminhos de influência;
-   Produzir contrafactuais (*interventions*);
-   Analisar o *Markov blanket*.

Use sua criatividade e capacidade de pesquisa para gerar as explicações
e interpretar os resultados da rede.

Explicações em linguagem natural também são bem-vindas (geração de um
texto que explica, em linguagem natural, os detalhes da inferência que a
rede fez).

------------------------------------------------------------------------

# 4. Construção do Relatório

Você deverá entregar um relatório detalhado, preferencialmente
escrito em LaTeX, contendo explicações e discussões pertinentes às
resoluções de cada tarefa enumerada na seção anterior.

Dentre as discussões que devem constar no documento, estão:

-   Descrição do domínio, das variáveis e do pré-processamento
    realizado;
-   Justificativa da estrutura elicitada manualmente e sua comparação
    com a estrutura aprendida;
-   Explicação básica do algoritmo de aprendizado estrutural e dos
    métodos de estimação de parâmetros empregados;
-   Discussão das respostas obtidas por inferência e da análise de
    explicabilidade da Tarefa 5.

O relatório será avaliado em termos da clareza da escrita, correção
gramatical e riqueza do conteúdo apresentado.

Não hesite em acrescentar imagens, gráficos e tabelas para reforçar sua
argumentação. Lembre-se: figuras e tabelas devem ser devidamente
referenciadas no texto.

Todas as referências bibliográficas utilizadas devem constar ao final do
documento e estar no mesmo formato (ABNT, APA ou Vancouver, conforme
desejarem).

Recomenda-se o uso da biblioteca **pgmpy (Python)**, que cobre
aprendizado estrutural, estimação de parâmetros e inferência, além de um
notebook reproduzível anexo ao relatório.

------------------------------------------------------------------------

# 5. Resumo

Ao fim, o que devemos entregar é um notebook reproduzível que faça o setup
do ambiente, baixando as bibliotecas necessárias, baixando a base de dados e
rodando o script de tratamento dos dados, e rodando os blocos de código que
fazem todas as etapas contempladas. Esse notebook deve ter uma condução clara
do que está sendo feito e uma breve discussão dos resultados após rodar cada
bloco de código. Junto do notebook, um relatório que descreva todos os pontos
citados no tópico 4. Tudo o que é necessário para executar as tarefas deve
ser instalável e reproduzível no notebook.