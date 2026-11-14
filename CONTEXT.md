# CONTEXT — tp3-redes-bayesianas

> Snapshot destilado do enunciado, do domínio e dos dados, construído a partir de `INPUTS/` (auditado em 2026-11-14, sem prompt injection). **Reescreva as seções no lugar quando os fatos mudarem; não é um diário.** As fontes brutas ficam em `INPUTS/`; este arquivo é a interpretação delas.

_Last updated: 2026-11-14_

## 1. One-paragraph summary

Trabalho prático 3 da disciplina **Fundamentos de Inteligência Artificial** (Departamento de Engenharia Elétrica — DEE, Engenharia de Sistemas, Belo Horizonte; profs. João Pedro Campos e Cristiano Leite de Castro, segundo os slides). A tarefa é percorrer o ciclo completo de uma **rede bayesiana discreta**: escolher e tratar um conjunto tabular, desenhar à mão uma estrutura plausível, aprender a estrutura com **Hill-Climbing + BIC** e um segundo método dos slides, estimar as CPTs, responder perguntas por inferência e explicar uma predição. O conjunto escolhido é a **FAA National Wildlife Strike Database** (colisões de fauna com aeronaves nos EUA), recortada para 2017–2025 e reduzida a **72.877 colisões × 14 variáveis categóricas** (+ `nivel_dano` como variável extra). A entrega é um **notebook reproduzível** (instala as bibliotecas, baixa a base, roda o tratamento e todas as tarefas, com discussão após cada bloco) e um **relatório detalhado, de preferência em LaTeX**. O sucesso é medido pela clareza, correção gramatical e riqueza do relatório (critério declarado no enunciado).

## 2. Stakeholders

| Name | Role / org | What they decide or own | Contact channel |
|---|---|---|---|
| Bruno (BrunoL28) | Aluno, dono do repositório | Escolhas de modelagem, aprovação do plano, submissão | — |
| João Pedro Campos (MSc) | Professor (autor dos slides do cap. 9) | Enunciado, avaliação | TODO: canal da disciplina (Moodle/e-mail) |
| Cristiano Leite de Castro (PhD) | Professor (autor dos slides do cap. 9) | Enunciado, avaliação | TODO: canal da disciplina |
| Colegas de grupo | TODO: confirmar se o TP é em grupo e quem participa | Divisão de tarefas | — |

## 3. The business today (as-is)

O ponto de partida já existe em `INPUTS/`:

- **Script de coleta/limpeza** — `INPUTS/scripts/coletar_birdstrikes.py`: baixa `https://wildlife.faa.gov/assets/database_excel.zip` (~133 MB, contém `Public.xlsx`), lê a planilha (360.384 linhas × 102 colunas) com `python-calamine` (fallback `openpyxl`, ~10 min), guarda um cache `dados/brutos/strikes_bruto.parquet`, limpa e grava `dados/processados/strikes_rede.csv` + `relatorio.md`. Caminhos são relativos ao diretório corrente (`RAIZ = Path("dados")`), não a `INPUTS/`. Argumentos: `--sem-download`, `--ano-min 2017`, `--ano-max 2025` (2017 = critério de dano estável; 2026 incompleto).
- **Funil de linhas** (de `relatorio.md`): 360.384 na planilha → 159.245 em 2017–2025 → −65.745 sem nível de dano → −20.623 sem fase do voo (carcaças achadas sem relato) → **72.877**.
- **Rede elicitada da Tarefa 2** — `INPUTS/rede_etapa2.png` (ver §4.2).
- **Base tratada** — `INPUTS/dados/processados/strikes_rede.csv`. ⚠ O arquivo commitado está **alinhado com espaços** (nomes de colunas e valores, ex. `' estacao  '`, `' primavera'`): não é a saída crua de `to_csv`. Ler com `skipinitialspace=True` + `strip()`, ou regenerar pelo script. Sem NaN depois do strip.

Nada de modelagem (estrutura, CPTs, inferência), notebook ou relatório existe ainda.

## 4. Target (to-be)

### 4.1 Entregáveis (de `INPUTS/requirements.md` §4–5)

1. **Notebook reproduzível** que: instala as bibliotecas; baixa a base da FAA; roda o script de tratamento; executa as Tarefas 1–5 em blocos, cada um seguido de uma breve discussão dos resultados. "Tudo o que é necessário para executar as tarefas deve ser instalável e reproduzível no notebook."
2. **Relatório** (preferencialmente LaTeX) cobrindo, no mínimo: domínio, variáveis e pré-processamento; justificativa da estrutura elicitada e comparação com a aprendida; explicação básica do algoritmo de aprendizado estrutural e dos métodos de estimação de parâmetros; discussão das inferências e da explicabilidade (Tarefa 5). Figuras/tabelas referenciadas no texto; referências no fim, num só formato (ABNT, APA ou Vancouver). Avaliado por clareza, correção gramatical e riqueza.

### 4.2 Tarefas

| Tarefa | O que pede | Estado dos insumos |
|---|---|---|
| 1 | Descrever domínio e pré-processamento (faltantes, **discretização das contínuas em três faixas por quantis**, codificação das categorias); formular **≥ 1 pergunta de interesse** | Pré-processamento feito pelo script; perguntas ainda não formuladas |
| 2 | Desenhar manualmente a estrutura antes de qualquer aprendizado (pode ser parcial) | **Feita**: `INPUTS/rede_etapa2.png` |
| 3 | Aprender a estrutura com **Hill-Climbing + BIC** e **outro método citado nos slides** (`FUND_IA_Chapter_9_RBs_BNSL (1).pdf`), de preferência disponível no pgmpy; comparar com a elicitada (onde concordou, onde discordou, por quê) | A fazer |
| 4 | Estimar CPTs (MLE ou bayesiano com priors) e responder às perguntas da Tarefa 1 por inferência com evidências variadas | A fazer |
| 5 | Escolher uma predição e explicá-la com propriedades da rede (sensibilidade, caminhos de influência, intervenções/contrafactuais, Markov blanket, explicação em linguagem natural) | A fazer |

**Rede elicitada (Tarefa 2)** — 14 nós, 17 arestas, alvos destacados em rosa (`Houve dano`, `Efeito no voo`):

```
Estação → Céu → Aviso
Estação → Animal          Período → Animal          Fase do voo → Altura → Animal
Animal → Tamanho do animal → Houve dano
Animal → Quantidade atingida → Houve dano
Quantidade atingida → Ingestão motor
Massa da aeronave → Motor → Ingestão motor
Massa da aeronave → Houve dano
Ingestão motor → Houve dano          Ingestão motor → Efeito no voo
Houve dano → Efeito no voo
```

Mapeamento nó → coluna: Estação=`estacao`, Período=`periodo`, Fase do voo=`fase_voo`, Altura=`altura`, Céu=`ceu`, Aviso=`avisado`, Massa da aeronave=`massa_aeronave`, Motor=`motor`, Animal=`animal`, Tamanho do animal=`tamanho_animal`, Quantidade atingida=`qtd_atingida`, Ingestão motor=`ingestao_motor`, Houve dano=`houve_dano`, Efeito no voo=`efeito_voo`.

### 4.3 Métodos de aprendizado estrutural citados nos slides

Restrição: **PC**. Score: **Hill-Climbing com BIC**, Tabu Search, Simulated Annealing, **Genético (Larrañaga, 1996)**, **MAGABN** (genético multiagente). Híbrido: **MMHC**. Árvore: **Chow-Liu** (seção inteira, com teoria da informação). No pgmpy 1.1.2 existem: `HillClimbSearch` (com `tabu_length`), `PC`, `MmhcEstimator`, `TreeSearch(estimator_type="chow-liu")`, `GES`, `ExhaustiveSearch`. GA/MAGABN não existem no pgmpy. Parâmetros: os slides cobrem só MLE por contagem relativa (θijk = Nijk/Nij); a referência bibliográfica é Poole & Mackworth (2023).

## 5. Domain glossary

| Term | Meaning in this project | Source |
|---|---|---|
| `estacao` | Estação do ano pelo mês (dez–fev inverno, mar–mai primavera, jun–ago verão, set–nov outono; hemisfério norte) | script, `INCIDENT_MONTH` |
| `periodo` | `TIME_OF_DAY` → amanhecer/dia/anoitecer/noite/desconhecido | script |
| `fase_voo` | `PHASE_OF_FLIGHT` agrupada: corrida_decolagem, subida (climb, departure), rota (en route, local), aproximacao (approach, descent, arrival), corrida_pouso, solo_taxi (taxi, parked) | script |
| `altura` | `HEIGHT` (pés AGL): 0 → `solo`; >0 em **tercis** → baixa/media/alta; vazio → desconhecido | script (`tercis_com_zero`) |
| `ceu` | `SKY` → sem_nuvens/algumas_nuvens/encoberto/desconhecido | script |
| `massa_aeronave` | `AC_MASS` (códigos FAA 1–5): ≤2 leve, 3 media, ≥4 pesada | script |
| `motor` | `TYPE_ENG`: A pistao, B/D jato, C turboelice, F helicoptero, E/Y desconhecido | script |
| `animal` | `SPECIES` por regex: ave (padrão), morcego, terrestre (mamíferos/répteis) | script |
| `tamanho_animal` | `SIZE` → pequeno/medio/grande/desconhecido | script |
| `qtd_atingida` | `NUM_STRUCK` → um / 2_a_10 / mais_de_10 / desconhecido | script |
| `avisado` | `WARNED` (piloto avisado da fauna) → sim/nao/desconhecido (51% desconhecido) | script |
| `ingestao_motor` | Algum `ING_ENG1..4` verdadeiro → sim/nao | script |
| `houve_dano` | `DAMAGE_LEVEL` N → nao; M, M?, S, D → sim (**alvo principal**; 7,7% sim) | script |
| `nivel_dano` | N nenhum; M e M? leve; S e D grave (420 casos graves). Função determinística de/para `houve_dano` — **não usar junto** no aprendizado | script |
| `efeito_voo` | `EFFECT` → desligamento_motor/decolagem_abortada/pouso_precaucao/outro/nenhum; vazio → nenhum | script |
| `M?` | Dano indeterminado (houve dano, nível desconhecido) — codificado como leve | FAA fieldlist |
| Elicitada | Estrutura desenhada à mão na Tarefa 2 | enunciado |
| BIC | `log P(D|θ̂) − (k/2)·log n` — penaliza parâmetros livres; consistente | slides p.10 |

## 6. Systems & data

| System | What we use it for | Access (who/what account) | Key objects / fields |
|---|---|---|---|
| FAA Wildlife Strike Database | Fonte dos dados | Público, sem login: `https://wildlife.faa.gov/assets/database_excel.zip` | `Public.xlsx`, 1 planilha `Sheet1`, 102 colunas (`INDEX_NR`, `INCIDENT_YEAR`, `INCIDENT_MONTH`, `TIME_OF_DAY`, `PHASE_OF_FLIGHT`, `HEIGHT`, `SPEED`, `SKY`, `PRECIPITATION`, `AC_MASS`, `TYPE_ENG`, `SPECIES`, `SIZE`, `NUM_STRUCK`, `WARNED`, `DAMAGE_LEVEL`, `EFFECT`, `ING_ENG1..4`, …). Contém nomes/cargos de quem reportou (`REPORTED_NAME`, `PERSON`) — não usar |
| pgmpy 1.1.2 | Estrutura, CPTs, inferência, intervenções | PyPI | `causal_discovery.HillClimbSearch`, `estimators.TreeSearch`, `causal_discovery.PC`, `estimators.MmhcEstimator`, `models.DiscreteBayesianNetwork`, `parameter_estimator.DiscreteMLE/DiscreteBayesianEstimator`, `inference.VariableElimination`, `inference.CausalInference`, `metrics.SHD` |
| GitHub `BrunoL28/tp3-redes-bayesianas` | Estado do projeto | Privado | — |

**Distribuições na base final (n = 72.877):** estacao outono 25.385 / verao 23.855 / primavera 16.681 / inverno 6.956 · fase_voo aproximacao 36.043 / corrida_pouso 13.722 / subida 10.671 / corrida_decolagem 8.663 / rota 3.463 / solo_taxi 315 · altura solo 22.731 / desconhecido 16.294 / media 11.430 / baixa 11.340 / alta 11.082 · massa pesada 53.546 / leve 11.090 / media 7.780 / desconhecido 461 · motor jato 61.124 / pistao 5.965 / helicoptero 2.616 / turboelice 2.613 / desconhecido 559 · animal ave 70.780 / morcego 1.194 / terrestre 903 · houve_dano sim 5.634 (7,7%) · ingestao_motor sim 2.240 · efeito_voo nenhum 68.011 / pouso_precaucao 3.470 / decolagem_abortada 818 / outro 467 / desligamento_motor 111 (pelo script atual; o CSV commitado em `INPUTS/` veio de uma versão anterior do script e tem 828/101 — 10 colisões "Aborted Take-off, Engine Shutdown" mudaram de grupo).

**Sinais fortes já visíveis nas tabelas cruzadas** (`relatorio.md`, % com dano leve+grave): tamanho grande 44% vs. pequeno 2,9%; animal terrestre 30,8% vs. morcego 1,4%; motor pistão 23,2% vs. jato 5,6%; massa leve 19,9% vs. pesada 5,0%; ingestão no motor 25,1% vs. 7,1%; fase rota 18,8% vs. corrida_pouso 3,8%; efeito desligamento_motor 64,9% com dano. Estação, período e céu quase não mexem no dano (5–14%).

## 7. Constraints & non-negotiables

- Hill-Climbing **com BIC** é obrigatório; o segundo método tem de estar nos slides (de preferência no pgmpy).
- Contínuas discretizadas em **três faixas por quantis** (o script faz tercis só para `HEIGHT`, com zero e faltante como estados próprios — justificar no relatório). `SPEED` é lido mas **não** vira nó.
- Idealmente < 60 variáveis (temos 14).
- Notebook 100% reproduzível em ambiente limpo; repositório é **privado** → o notebook não pode buscar arquivos no GitHub sem autenticação.
- Relatório em português, gramaticalmente correto, figuras/tabelas referenciadas, bibliografia num formato único.
- Prazo de entrega: **TODO — desconhecido** (ver §9).

## 8. Decisions made

| Date | Decision | Why | Decided by |
|---|---|---|---|
| ≤2026-11-13 | Base: FAA Wildlife Strikes, 2017–2025 | Domínio com categorias naturais e dependências plausíveis; critério de dano estável desde 2017 | Bruno |
| ≤2026-11-13 | Remover linhas sem `DAMAGE_LEVEL` e sem `PHASE_OF_FLIGHT`; demais faltantes viram estado `desconhecido` | Alvo e fase são essenciais; perder outras linhas enviesaria a base | Bruno (script) |
| ≤2026-11-14 | Rede elicitada com 14 nós (`INPUTS/rede_etapa2.png`) | Tarefa 2 | Bruno |
| 2026-11-14 | Repo self-managed privado `BrunoL28/tp3-redes-bayesianas`; `INPUTS/dados/brutos/` fora do git | Zip de 133 MB excede o limite de 100 MB do GitHub; regenerável | Bruno + agente |
| 2026-11-14 | pgmpy fixado em 1.1.2 | API mudou entre versões; reprodutibilidade | Agente |
| 2026-11-14 | Segundo método da Tarefa 3: **Chow-Liu** | Seção inteira nos slides, `TreeSearch` no pgmpy, contraste claro com o HC | Bruno |
| 2026-11-14 | Notebook roda no **Colab e em Jupyter local** | Reprodutibilidade nos dois ambientes | Bruno |
| 2026-11-14 | Perguntas de interesse **Q1–Q4** do plano (§9 C4) aprovadas | — | Bruno |
| 2026-11-14 | Escopo: Build Order completa, **sem extras não pedidos** (sem PC/MMHC, `ExpertKnowledge`, EM, `SPEED`, alvo `nivel_dano`, variantes de HC) | "Se não foi pedido, não precisa fazer" | Bruno |
| 2026-11-14 | Hill-Climbing puro (`tabu_length=0`); com tabu 100 o grafo é idêntico | Fiel ao algoritmo pedido | Agente |
| 2026-11-14 | Parâmetros: BDeu α = 50 (melhor log-verossimilhança em holdout 80/20; MLE dá P = 0 em 16 registros de teste) | Tarefa 4 pede o "mais pertinente" | Agente |
| 2026-11-14 | Bibliografia em **Vancouver** (natbib + `unsrtnat`), compila local e no Overleaf | TeX local não tem `biblatex`/`abntex2`; trocável | Agente (padrão, revisar) |

## 9. Open questions

| # | Question | Who can answer | Blocking? |
|---|---|---|---|
| 1 | Qual o prazo de entrega e onde se submete (Moodle? PDF + .ipynb?) | Bruno / professores | Não (Bruno: seguir a Build Order completa independentemente do prazo) |
| 2 | O TP é individual ou em grupo? Quem são os integrantes (capa do relatório)? | Bruno | Não |
| 3 | ~~Segundo método~~ — **resolvido: Chow-Liu** (§8) | Bruno | — |
| 4 | ~~Ambiente-alvo~~ — **resolvido: os dois** (§8) | Bruno | — |
| 5 | Relatório no Overleaf (sincronizado) ou LaTeX local? Formato de citação (ABNT/APA/Vancouver)? | Bruno | Não |
| 6 | ~~`SPEED`~~ — **resolvido: fica fora** (não pedido; a regra dos tercis vale para as contínuas usadas, só `HEIGHT`) | Bruno | — |
| 7 | `estacao` está pela convenção do hemisfério norte (dez–fev = inverno), correta para os EUA — confirmar que é a intenção | Bruno | Não |

## 10. Sources

Auditados com `prompt-injection-audit` (modo ingestão) em 2026-11-14 — todos **NÃO**; relatório: `archive/input-audits/2026-11-14-injection-audit.md`.

| File in INPUTS/ | What it is | Date |
|---|---|---|
| `INPUTS/requirements.md` | Enunciado do TP (adaptado com caminhos do projeto) | 2026-11-14 |
| `INPUTS/FUND_IA_Chapter_9_RBs_BNSL (1).pdf` | Slides "Aprendizado Estrutural de Redes Bayesianas" (63 p., Beamer) | 2025-05-23 |
| `INPUTS/rede_etapa2.png` | Rede elicitada manualmente (Tarefa 2) | 2026-11-14 |
| `INPUTS/scripts/coletar_birdstrikes.py` | Script de download + limpeza + discretização | 2026-11-14 |
| `INPUTS/dados/processados/relatorio.md` | Saída do script: funil, valores originais, tabelas de dano | 2026-11-13 |
| `INPUTS/dados/processados/strikes_rede.csv` | Base final (72.877 × 17), alinhada com espaços | 2026-11-13 |
| `INPUTS/dados/brutos/database_excel.zip`, `strikes_bruto.parquet` | Download original e cache (gitignored) | 2026-11-13 |
