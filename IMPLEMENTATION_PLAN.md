# IMPLEMENTATION PLAN — tp3-redes-bayesianas

**Revision:** 1 · **Date:** 2026-11-14 · **Previous revisions:** `archive/` (none yet)

> Pequenas mudanças (componente concluído, bug corrigido) → editar no lugar. Mudanças grandes (troca do segundo método, nova base, reestruturação) → mover para `archive/IMPLEMENTATION_PLAN_rev1_AAAA-MM-DD.md` e escrever a rev 2.
>
> Todo o código abaixo foi conferido contra o código-fonte do **pgmpy 1.1.2** (wheel do PyPI, 2026-11-14), mas ainda **não foi executado**. O primeiro passo da Build Order é um smoke test que confirma cada chamada.

---

## 1. Current Implementation Status

**Phase:** Phase 0 — bootstrap concluído; aguardando revisão do plano e respostas às perguntas abertas (CONTEXT §9).

| # | Component | Status | Tested? | Notes |
|---|---|---|---|---|
| C0 | Ambiente local (`.venv` + pgmpy 1.1.2) | ⬜ Not started | — | `tmp/venv` existe só para a auditoria; o venv do projeto é `.venv/` |
| C1 | Notebook — setup do ambiente | ⬜ Not started | — | Depende da resposta "Colab ou local" (CONTEXT §9 #4) |
| C2 | Notebook — coleta e tratamento (script da FAA) | 🟡 Script pronto em `INPUTS/scripts/` | Gerou `INPUTS/dados/processados/*` em 2026-11-13 (72.877 linhas) | Falta embutir no notebook |
| C3 | Carga e validação da base | ⬜ Not started | — | CSV commitado é alinhado com espaços |
| C4 | Tarefa 1 — domínio, pré-processamento, perguntas | 🟡 Pré-processamento feito | `relatorio.md` | Perguntas de interesse ainda não fixadas (proposta em §9-C4) |
| C5 | Tarefa 2 — rede elicitada | ✅ Desenho feito | — | `INPUTS/rede_etapa2.png`; falta codificar como DAG (17 arestas) |
| C6 | Tarefa 3a — Hill-Climbing + BIC | ⬜ Not started | — | |
| C7 | Tarefa 3b — segundo método (Chow-Liu, proposto) | ⬜ Not started | — | Decisão pendente (CONTEXT §9 #3) |
| C8 | Tarefa 3c — comparação das estruturas | ⬜ Not started | — | |
| C9 | Tarefa 4 — CPTs + inferência | ⬜ Not started | — | |
| C10 | Tarefa 5 — explicação de uma predição | ⬜ Not started | — | |
| C11 | Figuras e tabelas exportadas | ⬜ Not started | — | `relatorio/figuras/` |
| C12 | Relatório LaTeX | ⬜ Not started | — | `relatorio/` |
| C13 | Entrega (snapshot + execução limpa) | ⬜ Not started | — | `entregas/` |

### Bug log

| Date | Bug | Root cause | Fix | Status |
|---|---|---|---|---|
| 2026-11-14 | `pd.read_csv("strikes_rede.csv")` devolve colunas `' estacao  '` e valores `' primavera'` | CSV commitado foi alinhado com espaços (não é a saída crua de `to_csv`) | Ler com `skipinitialspace=True` + `strip()` (C3) ou regenerar pelo script (C2) | Open (contornado no plano) |

---

## 2. Introduction

Colisões entre aeronaves e fauna (aves, morcegos, mamíferos terrestres) são um risco operacional conhecido na aviação. A FAA mantém a *National Wildlife Strike Database* com cerca de 360 mil relatos desde 1990. No recorte 2017–2025, depois de remover relatos sem nível de dano e sem fase do voo, restam **72.877 colisões**, das quais **5.634 (7,7%) causaram dano** à aeronave e 420 (0,6%) dano grave. As tabelas cruzadas já mostram efeitos fortes e interpretáveis: animal grande gera dano em 44% dos casos (pequeno: 2,9%), aeronave leve em 19,9% (pesada: 5,0%), motor a pistão em 23,2% (jato: 5,6%), ingestão pelo motor em 25,1% (sem ingestão: 7,1%).

O TP3 pede o ciclo completo de uma rede bayesiana sobre um conjunto como esse: modelar o domínio à mão, deixar dois algoritmos aprenderem a estrutura, comparar as três, estimar as CPTs, consultar a rede e explicar uma predição. Este projeto transforma os insumos já prontos (script de coleta, base tratada, rede elicitada) em um notebook reproduzível e num relatório LaTeX que respondam a cada item do enunciado (`INPUTS/requirements.md`).

---

## 3. Scope note

**In scope (v1):**
- 14 nós: `estacao, periodo, fase_voo, altura, ceu, massa_aeronave, motor, animal, tamanho_animal, qtd_atingida, avisado, ingestao_motor, houve_dano, efeito_voo`. Alvo principal: `houve_dano`; alvo secundário: `efeito_voo`.
- Estrutura: elicitada (Tarefa 2), **Hill-Climbing + BIC** (`bic-d`), **Chow-Liu** (segundo método proposto, decisão pendente).
- Comparação: tabela de arestas (concorda / invertida / só na aprendida / só na elicitada), SHD entre CPDAGs, BIC de cada estrutura sobre os mesmos dados, figuras lado a lado.
- Parâmetros: BDeu (estimação bayesiana) como principal, MLE como comparação; escolha do tamanho amostral equivalente por log-verossimilhança em holdout.
- Inferência: 3–4 perguntas fixas (§9-C4) com evidências variadas, cada uma conferida contra a frequência empírica.
- Explicabilidade: uma predição concreta explicada por Markov blanket, sensibilidade (leave-one-out + variação de estados), caminhos ativos, intervenção `do()` e texto em linguagem natural gerado por template.
- Notebook único executável do início ao fim + relatório LaTeX.

**Explicitly deferred (Phase 2+):**
- Terceiro método (PC ou MMHC) como comparação extra — só se sobrar tempo; enriquece a discussão de score vs. restrição vs. híbrido.
- HC + BIC com conhecimento a priori (`ExpertKnowledge`, ex. proibir arestas que entram em `estacao`/`periodo`) — variante interessante, não pedida.
- `nivel_dano` (3 estados) como alvo alternativo — só 420 casos graves; fica para discussão.
- `velocidade` (`SPEED` em tercis) como 15º nó — ver Known Holes #6.

**Acceptable v1 fallbacks:**
- Se o download da FAA falhar no momento da execução, o notebook aceita um `Public.xlsx`/zip local enviado manualmente (célula alternativa documentada), mantendo o mesmo tratamento.
- Se `CausalInference.query(do=...)` falhar ou ficar lento, a intervenção é feita por "cirurgia" manual do grafo (remover arestas que entram no nó intervencionado e fixar a CPT) e inferência com `VariableElimination`.
- Se o Overleaf não for usado, LaTeX local com `latexmk`.

**Out of scope:**
- Algoritmos genéticos (Larrañaga, MAGABN) — não existem no pgmpy; implementar do zero não compensa para o TP.
- Variáveis contínuas não discretizadas, redes híbridas/gaussianas.
- Texto livre (`REMARKS`, `COMMENTS`) e dados de quem reportou.

---

## 4. Design Philosophy

- **O enunciado é o contrato.** Cada seção do notebook e do relatório aponta para o item do enunciado que cumpre; nada obrigatório fica implícito.
- **Um notebook, do zero ao fim.** Ele roda em ambiente limpo sem nada além de internet: instala, baixa, trata, aprende, consulta, explica.
- **Todo número da rede é conferido contra os dados.** Uma probabilidade da rede sem comparação com a frequência empírica não entra no relatório.
- **Compare equivalências, não desenhos.** O BIC não distingue DAGs Markov-equivalentes; a comparação de orientação usa CPDAGs, e a discussão diz isso.
- **"Desconhecido" é um estado, e isso tem custo.** Faltantes viraram categoria; isso pode criar arestas entre variáveis que só compartilham a fonte do relato. É resultado a discutir, não ruído a esconder.
- **Determinismo.** Semente fixa, versões fixas, ordem de estados fixa. Duas execuções dão as mesmas figuras.
- **Explicar com a própria rede.** A Tarefa 5 usa d-separação, Markov blanket, sensibilidade e `do()` do modelo aprendido, sem modelos externos.

---

## 5. Functional Requirements

### FR-1 — Setup reproduzível (requirements §5)

- **Trigger:** primeira célula do notebook.
- **Input:** nenhum além de internet.
- **Output:** pacotes instalados com versão fixa; impressão das versões (`python`, `pgmpy`, `pandas`, `numpy`, `networkx`); `SEED = 42`.
- **Errors:** se `pgmpy.__version__ != "1.1.2"`, a célula falha com mensagem clara (evita rodar com API diferente).
- **Scope:** não instala LaTeX nem graphviz de sistema.

### FR-2 — Coleta e tratamento (requirements §2, §5; Tarefa 1)

- **Trigger:** segunda seção do notebook.
- **Input:** `https://wildlife.faa.gov/assets/database_excel.zip`.
- **Output:** `dados/processados/strikes_rede.csv` (1 linha por colisão, 17 colunas: `id, ano` + 14 nós + `nivel_dano`) e `dados/processados/relatorio.md`.
- **State:** `dados/brutos/database_excel.zip`, `dados/brutos/strikes_bruto.parquet` (cache).
- **Errors:** download com timeout de 120 s por requisição (do script); se a FAA estiver fora, célula alternativa para upload manual.
- **Scope:** usa exatamente a lógica de `INPUTS/scripts/coletar_birdstrikes.py` (copiada para o notebook, ver C2).

### FR-3 — Descrição e perguntas (Tarefa 1)

- **Output:** tabela de variáveis (nome, origem FAA, estados, contagens, % desconhecido), funil de linhas, justificativa da discretização (tercis de `HEIGHT` com `solo` e `desconhecido` à parte), tabela "taxa de dano por estado" e as perguntas de interesse Q1–Q4 (§9-C4).

### FR-4 — Rede elicitada (Tarefa 2)

- **Output:** `DAG_ELICITADA` em código (17 arestas), figura no mesmo layout das aprendidas, parágrafo de justificativa por aresta (tabela "aresta → razão de domínio").

### FR-5 — Aprendizado de estrutura (Tarefa 3)

- **Output:** `dag_hc` (Hill-Climbing + BIC) e `dag_cl` (Chow-Liu); para cada uma: nº de arestas, nº de parâmetros livres, BIC sobre os dados, figura.
- **Comparação:** tabela de arestas por categoria, SHD entre CPDAGs (elicitada vs HC, elicitada vs CL, HC vs CL), discussão "onde concordou / onde discordou / por quê".

### FR-6 — Parâmetros e inferência (Tarefa 4)

- **Output:** modelo `DiscreteBayesianNetwork` sobre `dag_hc` ajustado com BDeu (tamanho amostral equivalente escolhido em holdout), comparação com MLE, CPTs relevantes impressas (`houve_dano`, `efeito_voo`), respostas Q1–Q4 com ≥ 2 conjuntos de evidência cada, conferência contra frequências empíricas.

### FR-7 — Explicação de uma predição (Tarefa 5)

- **Output:** um caso concreto (registro real da base, `id` citado) com P(`houve_dano`=sim | evidência); Markov blanket do alvo; gráfico tornado de sensibilidade; caminhos ativos evidência → alvo; comparação condicionamento vs. `do()`; parágrafo em linguagem natural gerado do resultado.

### FR-8 — Relatório (requirements §4)

- **Output:** `relatorio/main.tex` → PDF, com as seções de §9-C12, todas as figuras/tabelas referenciadas, bibliografia num formato único.

---

## 6. High-Level Architecture

```
                         ┌──────────────────────── notebook/tp3_redes_bayesianas.ipynb ─────────────────────────┐
FAA zip (133 MB) ──► C2 coleta/limpeza ──► strikes_rede.csv ──► C3 carga+validação ──► df[NOS] (72.877 × 14)
                    (script embutido)                                                     │
                                                    ┌───────────────────────────────────┼───────────────────────────┐
                                                    ▼                                   ▼                           ▼
                                           C5 DAG elicitada                    C6 Hill-Climbing + BIC        C7 Chow-Liu (TreeSearch)
                                           (17 arestas, à mão)                 (causal_discovery)            (estimators)
                                                    └──────────────┬────────────────────┴───────────────────────────┘
                                                                   ▼
                                                   C8 comparação (arestas, CPDAG, SHD, BIC)
                                                                   │
                                                                   ▼
                                     C9 CPTs (BDeu vs MLE, holdout) ──► VariableElimination ──► Q1–Q4 (+ checagem empírica)
                                                                   │
                                                                   ▼
                                     C10 explicação: Markov blanket · sensibilidade · caminhos ativos · do() · texto
                                                                   │
                                                                   ▼
                                     C11 figuras/tabelas (PDF/PNG + .tex) ──► C12 relatório LaTeX ──► C13 entregas/
                         └──────────────────────────────────────────────────────────────────────────────────────┘
```

**C2 (coleta) dentro do notebook.** O repositório é privado; um notebook rodando no Colab não consegue baixar o script do GitHub sem token. Por isso o script vai **embutido** numa célula `%%writefile coletar_birdstrikes.py` (cópia literal de `INPUTS/scripts/coletar_birdstrikes.py`), executado logo em seguida com `!python coletar_birdstrikes.py`. Rejeitado: reescrever o tratamento em funções do notebook (duplica lógica e afasta do script que gerou o `relatorio.md`); baixar do GitHub (exige token).

**C3 (carga).** Ponto único de leitura. Fixa a lista `NOS`, a ordem dos estados de cada variável (`STATE_NAMES`) e valida contagens. Todos os componentes seguintes recebem `df[NOS]` com dtype `category` ordenado, para que as CPTs e figuras saiam sempre na mesma ordem.

**C5/C6/C7 (estruturas).** As três estruturas são objetos `pgmpy.base.DAG` sobre os mesmos 14 nós; nós isolados são adicionados explicitamente para não sumirem (`add_nodes_from(NOS)`).

**C8 (comparação).** Usa CPDAG (`DAG.to_pdag()`) porque o BIC é score-equivalente: DAGs na mesma classe de Markov empatam, então a orientação de uma aresta "reversível" não é evidência contra a intuição. Também calcula o BIC das três estruturas sobre os mesmos dados — mostra quanto a elicitada perde em ajuste e quanto ganha em parcimônia.

**C9 (parâmetros).** BDeu em vez de MLE puro porque há estados raros (`solo_taxi` 315, `desligamento_motor` 101, `qtd_atingida=desconhecido` 65) e combinações de pais sem dados geram probabilidade zero ou indefinida no MLE.

**C10 (explicação).** Tudo vem da rede: d-separação e Markov blanket da topologia, sensibilidade de consultas repetidas, intervenção pelo `CausalInference`. O texto em linguagem natural é montado por template a partir desses números (determinístico, sem LLM).

---

## 7. Integration Feasibility Report

### 7.1 FAA Wildlife Strike Database (download)

| Item | Detail |
|---|---|
| Nodes / SDK / API used | HTTP GET estático via `requests` (no script): `https://wildlife.faa.gov/assets/database_excel.zip` |
| Credential type | Nenhuma (público) |
| Existing or to-create | Existe. HEAD em 2026-11-14: `200 OK`, `Content-Length: 133451569`, `Last-Modified: Tue, 10 Nov 2026 05:31:34 GMT` (idêntico ao zip em `INPUTS/dados/brutos/`) |
| Setup steps | 1. Nenhum. 2. Dicionário de campos: `https://wildlife.faa.gov/assets/fieldlist.pdf` (citar no relatório) |

**Operations:**

| Operation | Endpoint / node op | Input | Output | Limits |
|---|---|---|---|---|
| Download | GET `database_excel.zip` (stream, blocos de 1 MB) | — | zip 133 MB com `Public.xlsx` (159 MB) | Timeout 120 s por requisição; ~1–3 min no Colab |
| Leitura | `pd.read_excel(engine="calamine", dtype=str)` | `Public.xlsx` | DataFrame 360.384 × 102 | ~1–2 min com calamine; ~10 min com openpyxl; vários GB de RAM (ok no Colab gratuito, ~12 GB) |

**Potential issues:** (a) a FAA **atualiza o arquivo periodicamente** (o atual é de 2026-11-10) — relatos atrasados de 2025 podem entrar e mudar as contagens em algumas linhas; o notebook imprime as contagens e o relatório cita a data do download (Known Holes #4). (b) O site pode estar fora; há fallback de upload manual. (c) Nomes de colunas mudaram no passado; o script já trata sinônimos (`PHASE_OF_FLT`, `PRECIP`, `BIRDS_STRUCK`, `DAMAGE`, `INDEX NR`).

**Overall feasibility:** ✅ — URL ativa, sem autenticação, script já testado contra ela.

### 7.2 pgmpy 1.1.2 (PyPI)

| Item | Detail |
|---|---|
| Nodes / SDK / API used | `pgmpy==1.1.2` (Python ≥3.10, <3.15; deps: numpy≥2, pandas≥1.5, networkx≥3, scipy, scikit-learn, statsmodels, torch **não** é necessário) |
| Credential type | Nenhuma |
| Existing or to-create | Instalar no `.venv` local e na 1ª célula do notebook |
| Setup steps | 1. `pip install "pgmpy==1.1.2"`. 2. Smoke test (Build Order passo 1). |

**Operations:**

| Operation | API (1.1.2) | Input | Output | Notes |
|---|---|---|---|---|
| Hill-Climbing | `pgmpy.causal_discovery.HillClimbSearch(scoring_method="bic-d", return_type="dag", tabu_length=..., max_indegree=None, show_progress=False).fit(df)` → `.causal_graph_` | DataFrame categórico | `DAG` | **Default `return_type="pdag"`** — tem de passar `"dag"`. A classe antiga `pgmpy.estimators.HillClimbSearch(df).estimate(...)` ainda existe mas emite `FutureWarning` |
| Chow-Liu | `pgmpy.estimators.TreeSearch(df, root_node=R).estimate(estimator_type="chow-liu", show_progress=False)` | DataFrame + raiz | `DAG` (árvore) | Peso padrão `edge_weights_fn="mutual_info"` |
| PC (opcional) | `pgmpy.causal_discovery.PC(ci_test="chi_square", significance_level=0.01, return_type="pdag")` | DataFrame | PDAG | Com n = 72.877 quase todo teste rejeita independência → grafo denso |
| MMHC (opcional) | `pgmpy.estimators.MmhcEstimator(df).estimate(scoring_method=..., tabu_length=10, significance_level=0.01)` | DataFrame | DAG | API antiga (estimators) |
| Score de um DAG | `pgmpy.metrics.StructureScore(scoring_method="bic-d")(X=df, causal_graph=dag)` | DataFrame + DAG | float | Mesmo score que o HC otimiza |
| SHD | `pgmpy.metrics.SHD()(true_causal_graph=g1, est_causal_graph=g2)` | 2 grafos | int | `edge_reverse_penalty=1` por padrão |
| Modelo | `pgmpy.models.DiscreteBayesianNetwork(edges)`; `.add_nodes_from(NOS)`; `.fit(df, estimator=...)`; `.check_model()`; `.get_markov_blanket(no)` | | | |
| Estimadores | `pgmpy.parameter_estimator.DiscreteBayesianEstimator(prior_type="BDeu", equivalent_sample_size=ESS)`, `DiscreteMLE()` | | | `pgmpy.estimators.BayesianEstimator` está deprecado (remoção na 1.3.0) |
| Inferência | `pgmpy.inference.VariableElimination(model).query(variables=[...], evidence={...}, show_progress=False)`; `.map_query(...)` | | `DiscreteFactor` | |
| Intervenção | `pgmpy.inference.CausalInference(model).query(variables=[...], do={...}, evidence={...}, inference_algo="ve")` | | `DiscreteFactor` | |
| d-separação | `model.is_dconnected(a, b, observed=...)`, `model.active_trail_nodes(...)`, `model.minimal_dseparator(a, b)` | | | Conferir nomes no smoke test |

**Potential issues:** a API está em transição (docs do branch `dev` já mostram `fit()` estilo scikit-learn; releases antigos usavam `.estimate()`). Snippets da internet para 0.1.x (`BayesianNetwork`, `BicScore`, `BayesianEstimator(model, data)`) **não** funcionam como estão. Fixar a versão resolve.

**Overall feasibility:** ✅ — todos os métodos necessários existem na 1.1.2; risco só de nome/assinatura, coberto pelo smoke test.

### 7.3 Google Colab (se escolhido como ambiente-alvo)

| Item | Detail |
|---|---|
| Nodes / SDK / API used | Runtime Python 3 padrão; `!pip install` na 1ª célula |
| Credential type | Conta Google de quem executa (nenhuma credencial no repo) |
| Existing or to-create | Existe |
| Setup steps | 1. Abrir o `.ipynb` no Colab (upload). 2. *Runtime → Run all*. |

**Potential issues:** o Colab pode já trazer outra versão de numpy/pandas; instalar pgmpy 1.1.2 pode pedir *restart* do runtime (documentar no topo do notebook). Disco temporário: zip + xlsx + parquet ≈ 350 MB, ok.

**Overall feasibility:** ✅ (decisão de usar ou não está em aberto — CONTEXT §9 #4).

### 7.4 Overleaf (opcional)

Só se o relatório for escrito/compilado no Overleaf. Ler `.agents/skills/overleaf/SKILL.md` antes (integração Git exige plano pago + token). **Overall feasibility:** ⚠️ — depende da conta; o fallback é LaTeX local.

---

## 8. Pre-Build Checklist

- [ ] Responder as perguntas abertas de `CONTEXT.md` §9 — principalmente #1 (prazo), #3 (segundo método), #4 (Colab ou local). (owner: Bruno)
- [ ] Criar `.venv` do projeto: `python3 -m venv .venv && .venv/bin/pip install "pgmpy==1.1.2" pandas pyarrow python-calamine requests matplotlib jupyter nbconvert` (owner: agente)
- [ ] Rodar o smoke test da API (Build Order passo 1) e corrigir este plano se alguma assinatura divergir (owner: agente)
- [ ] Decidir o formato de citação (ABNT/APA/Vancouver) e onde o LaTeX vive (Overleaf ou local) (owner: Bruno)
- [ ] Confirmar se o TP é em grupo e os nomes para a capa (owner: Bruno)

---

## 9. Component-by-component breakdown

### C0 — Ambiente local

- **Type:** venv Python 3.12 em `.venv/` (gitignored).
- **Job:** permitir rodar e testar o notebook localmente com as mesmas versões do notebook.
- **Parameters / code:**
  ```bash
  python3 -m venv .venv
  .venv/bin/pip install "pgmpy==1.1.2" "pandas>=2.2" pyarrow python-calamine requests matplotlib jupyter nbconvert
  .venv/bin/python -c "import pgmpy; print(pgmpy.__version__)"   # 1.1.2
  ```
- **Output:** interpretador `.venv/bin/python`; kernel para o Jupyter.
- **Next:** C1.

### C1 — Notebook: setup do ambiente

- **Type:** células iniciais de `notebook/tp3_redes_bayesianas.ipynb`.
- **Job:** instalar dependências fixas, importar, fixar semente e imprimir versões.
- **Parameters / code:**
  ```python
  # %pip install -q "pgmpy==1.1.2" pandas pyarrow python-calamine requests matplotlib
  import random, numpy as np, pandas as pd, networkx as nx, matplotlib.pyplot as plt, pgmpy
  assert pgmpy.__version__ == "1.1.2", f"pgmpy {pgmpy.__version__}: o notebook foi escrito para 1.1.2"
  SEED = 42; random.seed(SEED); np.random.seed(SEED)
  print({"python": __import__("sys").version.split()[0], "pgmpy": pgmpy.__version__,
         "pandas": pd.__version__, "numpy": np.__version__, "networkx": nx.__version__})
  ```
  Primeira célula markdown: título, autores, como executar (*Run all*; no Colab, reiniciar o runtime se o `%pip` pedir), tempo esperado (~5 min com download).
- **Output:** ambiente pronto; versões impressas.
- **Next:** C2.

### C2 — Notebook: coleta e tratamento

- **Type:** célula `%%writefile coletar_birdstrikes.py` + `!python coletar_birdstrikes.py`.
- **Job:** reproduzir exatamente o pipeline que gerou `INPUTS/dados/processados/`.
- **Parameters / code:**
  - Conteúdo da célula: cópia literal de `INPUTS/scripts/coletar_birdstrikes.py` (fonte da verdade continua em `INPUTS/`; se o script mudar, a cópia no notebook é atualizada no mesmo commit).
  - Execução: `!python coletar_birdstrikes.py --ano-min 2017 --ano-max 2025` (gera `dados/brutos/…` e `dados/processados/…` no diretório corrente).
  - Fallback (célula comentada): se o download falhar, enviar `database_excel.zip` para `dados/brutos/` e rodar com `--sem-download`.
  - Mostrar `dados/processados/relatorio.md` renderizado (`IPython.display.Markdown`).
- **Output:** `dados/processados/strikes_rede.csv` (17 colunas, sem padding) e `relatorio.md`.
- **Next:** C3.

### C3 — Carga e validação

- **Type:** função `carregar_base(caminho) -> pd.DataFrame`.
- **Job:** ler o CSV de forma robusta (aceita a versão alinhada com espaços), fixar a ordem dos estados e validar.
- **Parameters / code:**
  ```python
  NOS = ["estacao", "periodo", "fase_voo", "altura", "ceu", "massa_aeronave", "motor", "animal",
         "tamanho_animal", "qtd_atingida", "avisado", "ingestao_motor", "houve_dano", "efeito_voo"]
  STATE_NAMES = {
      "estacao": ["inverno", "primavera", "verao", "outono"],
      "periodo": ["amanhecer", "dia", "anoitecer", "noite", "desconhecido"],
      "fase_voo": ["solo_taxi", "corrida_decolagem", "subida", "rota", "aproximacao", "corrida_pouso"],
      "altura": ["solo", "baixa", "media", "alta", "desconhecido"],
      "ceu": ["sem_nuvens", "algumas_nuvens", "encoberto", "desconhecido"],
      "massa_aeronave": ["leve", "media", "pesada", "desconhecido"],
      "motor": ["pistao", "turboelice", "jato", "helicoptero", "desconhecido"],
      "animal": ["ave", "morcego", "terrestre"],
      "tamanho_animal": ["pequeno", "medio", "grande", "desconhecido"],
      "qtd_atingida": ["um", "2_a_10", "mais_de_10", "desconhecido"],
      "avisado": ["sim", "nao", "desconhecido"],
      "ingestao_motor": ["nao", "sim"],
      "houve_dano": ["nao", "sim"],
      "efeito_voo": ["nenhum", "pouso_precaucao", "decolagem_abortada", "desligamento_motor", "outro"],
  }
  def carregar_base(caminho):
      df = pd.read_csv(caminho, dtype=str, skipinitialspace=True)
      df.columns = df.columns.str.strip()
      df = df.apply(lambda s: s.str.strip())
      assert set(NOS) <= set(df.columns), set(NOS) - set(df.columns)
      assert df[NOS].notna().all().all()
      for c in NOS:
          extras = set(df[c]) - set(STATE_NAMES[c])
          assert not extras, (c, extras)       # estado novo = agrupamento do script mudou
          df[c] = pd.Categorical(df[c], categories=STATE_NAMES[c], ordered=False)
      return df
  ```
  Checagens impressas: `len(df)` (esperado 72.877 com o arquivo de 2026-11-10 — se a FAA atualizar, aceitar diferença e registrar), contagens por estado, `pd.crosstab(df.houve_dano, df.nivel_dano)` (confirma o determinismo).
- **Output:** `df` (72.877 × 17); `dados = df[NOS]` para todo o aprendizado.
- **Next:** C4.

### C4 — Tarefa 1: domínio, pré-processamento e perguntas

- **Type:** células markdown + tabelas.
- **Job:** descrever a base, o pré-processamento e formular as perguntas que a rede deve responder.
- **Conteúdo:**
  1. Domínio: o que é a base da FAA, quem reporta (pilotos, aeroportos, companhias; verificar na documentação da FAA o quanto a notificação é voluntária → possível viés de notificação), por que 2017–2025.
  2. Funil: 360.384 → 159.245 → −65.745 (sem dano) → −20.623 (sem fase) → 72.877.
  3. Tabela de variáveis: nó | coluna(s) FAA | regra de agrupamento | estados | % `desconhecido`.
  4. Tratamento de faltantes: linhas removidas só por alvo (`DAMAGE_LEVEL`) e fase; demais faltantes = estado `desconhecido` (justificativa: não perder 50% da base por `WARNED`; custo: dependências espúrias via fonte do relato — retomado em C8).
  5. Discretização: `HEIGHT` → `solo` (=0), tercis dos valores > 0 (`pd.qcut(…, 3)`) → baixa/media/alta, vazio → desconhecido. Imprimir os limites dos tercis (calcular no notebook a partir de `strikes_bruto.parquet` filtrado igual ao script). `AC_MASS` é código ordinal FAA (1–5), agrupado por faixa de peso, não por quantis — explicar.
  6. Codificação: tabela de mapeamento de cada categoria original → estado (de `relatorio.md`, "Valores originais").
  7. Taxa de dano por estado de cada variável (gráfico de barras horizontais, ordenado).
- **Perguntas de interesse (propostas — confirmar):**
  - **Q1 (preditiva):** dado o perfil da colisão, qual a probabilidade de dano? `P(houve_dano=sim | massa_aeronave, motor, tamanho_animal, animal, fase_voo)` — evidências: (a) aeronave leve a pistão, animal terrestre; (b) jato pesado, ave pequena, aproximação; (c) só `tamanho_animal=grande`.
  - **Q2 (consequência operacional):** dado que houve ingestão pelo motor, quão provável é um efeito no voo (pouso de precaução, decolagem abortada, desligamento)? `P(efeito_voo | ingestao_motor=sim)` vs. `| ingestao_motor=nao`, e com `qtd_atingida=2_a_10`.
  - **Q3 (diagnóstica, inversa):** dado que o motor foi desligado, o que provavelmente atingiu a aeronave? `P(tamanho_animal, qtd_atingida | efeito_voo=desligamento_motor)`.
  - **Q4 (intervencional):** se todo piloto fosse avisado da fauna, o risco de dano mudaria? `P(houve_dano | do(avisado=sim))` vs. `P(houve_dano | avisado=sim)` — com a ressalva de que é causal só se a estrutura aprendida for lida causalmente.
- **Output:** seção 1 do notebook; tabelas reaproveitadas no relatório.
- **Next:** C5.

### C5 — Tarefa 2: rede elicitada

- **Type:** constante + figura.
- **Job:** codificar o desenho `INPUTS/rede_etapa2.png` e justificar cada aresta.
- **Parameters / code:**
  ```python
  from pgmpy.base import DAG
  ARESTAS_ELICITADAS = [
      ("estacao", "ceu"), ("ceu", "avisado"),
      ("estacao", "animal"), ("periodo", "animal"),
      ("fase_voo", "altura"), ("altura", "animal"),
      ("animal", "tamanho_animal"), ("animal", "qtd_atingida"),
      ("tamanho_animal", "houve_dano"), ("qtd_atingida", "houve_dano"),
      ("qtd_atingida", "ingestao_motor"),
      ("massa_aeronave", "motor"), ("motor", "ingestao_motor"),
      ("massa_aeronave", "houve_dano"),
      ("ingestao_motor", "houve_dano"), ("ingestao_motor", "efeito_voo"),
      ("houve_dano", "efeito_voo"),
  ]                                        # 17 arestas, 14 nós
  dag_elic = DAG(ARESTAS_ELICITADAS); dag_elic.add_nodes_from(NOS)
  assert len(dag_elic.edges()) == 17 and nx.is_directed_acyclic_graph(dag_elic)
  ```
  Tabela de justificativas (exemplos): `estacao → animal` (migração muda a fauna), `fase_voo → altura` (fase determina altitude), `massa_aeronave → motor` (aeronaves leves usam pistão), `qtd_atingida → ingestao_motor` (bando aumenta chance de ingestão), `houve_dano → efeito_voo` (dano leva a pouso de precaução). Observação para a discussão: `ceu → avisado` é a aresta mais especulativa do desenho.
- **Output:** `dag_elic`; figura `fig_rede_elicitada` (mesmo layout fixo usado nas outras — posições definidas uma vez em `POS = {...}` por camadas: contexto → animal → impacto → consequência).
- **Next:** C6.

### C6 — Tarefa 3a: Hill-Climbing + BIC

- **Type:** aprendizado de estrutura score-based.
- **Job:** aprender o DAG que maximiza o BIC partindo do grafo vazio.
- **Parameters / code:**
  ```python
  from pgmpy.causal_discovery import HillClimbSearch
  hc = HillClimbSearch(scoring_method="bic-d", return_type="dag", tabu_length=100,
                       max_indegree=None, show_progress=False)
  hc.fit(dados)                 # dados = df[NOS]
  dag_hc = hc.causal_graph_; dag_hc.add_nodes_from(NOS)
  ```
  Variante de controle: `tabu_length=0` (HC "puro", sem lista tabu). Se os dois DAGs forem iguais, o relatório diz isso em uma frase; se diferirem, apresentar o de maior BIC e comentar o efeito da lista tabu (slides p.18).
  Registrar: nº de arestas, grau de entrada máximo, nº de parâmetros livres (`sum((card(X)-1) * prod(card(Pa)))`), BIC (`StructureScore("bic-d")`), tempo de execução.
  Expectativa: com n = 72.877 a penalidade `(k/2)·log n ≈ 5,6·k` é fraca frente à verossimilhança — esperar uma rede **mais densa** que a elicitada, incluindo arestas entre estados `desconhecido` (ver Known Holes #2).
- **Output:** `dag_hc`, figura `fig_rede_hc`.
- **Next:** C7.

### C7 — Tarefa 3b: segundo método — Chow-Liu (proposto)

- **Type:** aprendizado de estrutura em árvore (seção 4 dos slides, p.42–59).
- **Job:** árvore geradora máxima ponderada por informação mútua, orientada a partir de uma raiz.
- **Por que Chow-Liu (recomendação):** é o método com mais espaço nos slides (teoria da informação, MST, orientação); está no pgmpy (`TreeSearch`); é determinístico e barato; contrasta bem com o HC (árvore com 13 arestas, um pai por nó vs. DAG livre) — dá uma discussão clara sobre o que se perde ao impor a árvore. Alternativas: **PC** (constraint-based, slide 7; com n grande tende a grafo denso e devolve PDAG) e **MMHC** (híbrido; API antiga). Decisão pendente com o Bruno.
- **Parameters / code:**
  ```python
  from pgmpy.estimators import TreeSearch
  def chow_liu(dados, raiz):
      return TreeSearch(dados, root_node=raiz).estimate(estimator_type="chow-liu", show_progress=False)
  # Toda orientação de uma árvore a partir de qualquer raiz é Markov-equivalente (não há v-estruturas),
  # então a raiz não muda o ajuste. Escolher a raiz que maximiza a concordância de orientação com a elicitada:
  melhor = max(NOS, key=lambda r: len(set(chow_liu(dados, r).edges()) & set(ARESTAS_ELICITADAS)))
  dag_cl = chow_liu(dados, melhor)
  ```
  Imprimir a matriz de informação mútua (heatmap 14 × 14) — figura útil para o relatório, explica cada aresta da árvore.
- **Output:** `dag_cl` (13 arestas), `fig_rede_chowliu`, `fig_info_mutua`.
- **Next:** C8.

### C8 — Tarefa 3c: comparação das estruturas

- **Type:** análise.
- **Job:** responder "onde concordou, onde discordou, por quê".
- **Parameters / code:**
  ```python
  from pgmpy.metrics import SHD, StructureScore
  def comparar(ref, est):
      R, E = set(ref.edges()), set(est.edges())
      inv = {(a, b) for (a, b) in E if (b, a) in R}
      return {"concorda": R & E, "invertida": inv,
              "so_aprendida": E - R - inv, "so_elicitada": R - E - {(b, a) for (a, b) in inv}}
  bic = StructureScore(scoring_method="bic-d")
  tabela = {nome: {"arestas": len(g.edges()), "BIC": bic(X=dados, causal_graph=g),
                   "SHD_vs_elicitada_CPDAG": SHD()(true_causal_graph=dag_elic.to_pdag(),
                                                  est_causal_graph=g.to_pdag())}
            for nome, g in {"elicitada": dag_elic, "HC+BIC": dag_hc, "Chow-Liu": dag_cl}.items()}
  ```
  (Confirmar no smoke test se `SHD` aceita PDAG; se não, comparar esqueletos com `nx.Graph(g)` e orientação só nas arestas compelidas.)
- **Discussão (roteiro):**
  1. Arestas que os dois algoritmos e a intuição compartilham (esperado: `tamanho_animal–houve_dano`, `ingestao_motor–efeito_voo`, `massa_aeronave–motor`).
  2. Arestas "invertidas": mostrar se são reversíveis no CPDAG (sem evidência contra a intuição) ou compelidas (há v-estrutura nos dados).
  3. Arestas só aprendidas: separar (a) dependências reais não previstas (ex. `motor–fase_voo`, `animal–estacao`), (b) **artefatos de faltantes**: estados `desconhecido` que co-ocorrem porque vêm do mesmo tipo de relato (`altura`, `ceu`, `avisado`, `periodo`, `tamanho_animal`) — demonstrar com `crosstab` dos `desconhecido`.
  4. Arestas só elicitadas: dependências fracas demais para o BIC (MI baixa) — ex. `ceu → avisado`, `estacao → ceu`. Mostrar a MI de cada uma.
  5. BIC da elicitada vs. aprendidas (quanto ajuste a intuição deixa na mesa) e nº de parâmetros.
  6. Limites: equivalência de Markov (slides p.39–42), máximo local do HC, viés de seleção (linhas removidas), causalidade ≠ dependência.
- **Output:** `tab_comparacao_arestas`, `tab_metricas_estruturas`, `fig_comparacao` (três grafos com arestas coloridas por categoria, mesmo `POS`).
- **Next:** C9.

### C9 — Tarefa 4: parâmetros e inferência

- **Type:** estimação + consultas.
- **Job:** ajustar CPTs sobre a estrutura aprendida (HC+BIC) e responder Q1–Q4.
- **Parameters / code:**
  ```python
  from pgmpy.models import DiscreteBayesianNetwork
  from pgmpy.parameter_estimator import DiscreteBayesianEstimator, DiscreteMLE
  from pgmpy.inference import VariableElimination, CausalInference
  def ajustar(dag, dados, estimador):
      m = DiscreteBayesianNetwork(dag.edges()); m.add_nodes_from(NOS)
      m.fit(dados, estimator=estimador); assert m.check_model(); return m
  # Escolha do ESS: treino/teste 80/20 (SEED), log-verossimilhança média no teste
  treino = dados.sample(frac=0.8, random_state=SEED); teste = dados.drop(treino.index)
  candidatos = {"MLE": DiscreteMLE(), **{f"BDeu ESS={e}": DiscreteBayesianEstimator(prior_type="BDeu", equivalent_sample_size=e)
                                          for e in (1, 5, 10, 50)}}
  # escolher o melhor no teste; reajustar com 100% dos dados → `modelo`
  infer = VariableElimination(modelo)
  q = infer.query(variables=["houve_dano"], evidence={"massa_aeronave": "leve", "motor": "pistao",
                                                      "animal": "terrestre"}, show_progress=False)
  ```
  O DataFrame passado ao `fit` tem dtype `category` com todas as categorias (`STATE_NAMES`), para que estados sem ocorrência num contexto apareçam nas CPTs. Verificar que `state_names` do modelo bate com `STATE_NAMES`; se não, passar `state_names=STATE_NAMES` ao estimador (conferir parâmetro no smoke test).
  Log-verossimilhança no teste: `pgmpy.metrics.StructureScore(scoring_method="ll-d")` não serve (é score de estrutura); calcular direto: soma de `log P(x)` por linha via CPDs (`modelo.get_cpds(no).get_value(**{no: v, **pais})`) vetorizado por `groupby`. Alternativa: `modelo.predict_probability`/`log_probability` se existir na 1.1.2 (checar no smoke test).
- **Consultas e checagem:** para cada Q, ≥ 2 conjuntos de evidência; tabela "rede vs. frequência empírica (n de suporte)". Diferenças grandes só são aceitas quando o suporte empírico é pequeno (aí a rede "empresta força" de outras configurações — ponto a discutir). Q4 usa `CausalInference(modelo).query(variables=["houve_dano"], do={"avisado": "sim"})` e compara com o condicional observacional.
- **CPTs para o relatório:** `houve_dano` e `efeito_voo` completas (podem ser grandes — mostrar heatmap se `houve_dano` tiver muitos pais), demais só no notebook.
- **Output:** `modelo` (BDeu, ESS escolhido), `tab_ess`, `tab_q1..q4`, `fig_q1` (barras P(dano) por perfil).
- **Next:** C10.

### C10 — Tarefa 5: explicação de uma predição

- **Type:** análise de explicabilidade.
- **Job:** pegar uma predição concreta e explicá-la só com propriedades da rede.
- **Caso:** um registro real com risco alto e evidência rica, escolhido assim: entre as linhas com `houve_dano=sim`, `ingestao_motor=sim`, `fase_voo` em {`subida`, `rota`}, a de maior P(`houve_dano=sim` | demais variáveis exceto `houve_dano` e `efeito_voo`). Citar o `id` FAA. Usar como evidência as variáveis observáveis **antes** do desfecho (todas exceto `houve_dano`, `efeito_voo`).
- **Técnicas (todas):**
  1. **Markov blanket:** `modelo.get_markov_blanket("houve_dano")` — mostra que, dado o blanket, as demais evidências não importam (conferir numericamente: posterior com evidência completa = posterior só com o blanket).
  2. **Sensibilidade leave-one-out:** para cada variável de evidência, remover só ela e medir Δ = P(dano | e) − P(dano | e sem Xi). Gráfico tornado ordenado por |Δ|.
  3. **Sensibilidade por estado:** para as 3 variáveis mais influentes, variar o estado mantendo o resto; tabela P(dano) por estado.
  4. **Caminhos de influência:** para cada evidência, `is_dconnected(Xi, "houve_dano", observed=resto)`; listar os caminhos ativos (`nx.all_simple_paths` no esqueleto, filtrados pela regra de d-separação) e marcar na figura.
  5. **Intervenção / contrafactual:** `P(dano | do(tamanho_animal=pequeno), resto)` e `P(dano | do(ingestao_motor=nao), resto)` vs. condicionais; explicar a diferença (corta caminhos de trás).
  6. **MAP:** `infer.map_query(variables=[...], evidence=...)` — explicação "mais provável" para o desfecho (opcional).
  7. **Texto em linguagem natural:** função `explicar(caso)` que monta um parágrafo do tipo "A rede estima X% de chance de dano (base: 7,7%). O fator que mais pesa é `tamanho_animal=grande` (+Y p.p.); sem ele, a estimativa cairia para Z%…". Template determinístico, números vindos dos passos 1–5.
- **Output:** `fig_tornado`, `fig_caminhos`, `tab_intervencoes`, parágrafo gerado; tudo citado no relatório.
- **Next:** C11.

### C11 — Figuras e tabelas

- **Type:** funções utilitárias no notebook.
- **Job:** exportar cada figura para `relatorio/figuras/{nome}.pdf` (vetorial) + `.png`, e tabelas para `relatorio/tabelas/{nome}.tex` (`DataFrame.to_latex(index=False, escape=True)` com booktabs).
- **Lista:** `fig_taxa_dano_por_estado`, `fig_rede_elicitada`, `fig_rede_hc`, `fig_rede_chowliu`, `fig_info_mutua`, `fig_comparacao`, `fig_q1`, `fig_tornado`, `fig_caminhos`; `tab_variaveis`, `tab_funil`, `tab_comparacao_arestas`, `tab_metricas_estruturas`, `tab_ess`, `tab_q1`…`tab_q4`, `tab_intervencoes`.
- **Detalhe:** o notebook grava em `relatorio/figuras/` só se a pasta existir (execução local no repo); no Colab grava em `figuras/` local. Paleta e layout `POS` fixos para todas as redes.
- **Next:** C12.

### C12 — Relatório LaTeX

- **Type:** `relatorio/main.tex` + `relatorio/referencias.bib` + `relatorio/figuras/` + `relatorio/tabelas/`.
- **Job:** cumprir requirements §4.
- **Estrutura:**
  1. Introdução — problema, base, objetivos, perguntas Q1–Q4.
  2. Domínio e dados — FAA, funil, variáveis, pré-processamento (faltantes, discretização em tercis, codificação). *(Tarefa 1)*
  3. Fundamentos — RB, fatoração, d-separação; BIC; Hill-Climbing (operadores, máximos locais, tabu); Chow-Liu (MI, MST, orientação); MLE vs. BDeu. *(exigido: "explicação básica do algoritmo… e dos métodos de estimação")*
  4. Estrutura elicitada — figura + justificativas. *(Tarefa 2)*
  5. Estruturas aprendidas e comparação. *(Tarefa 3)*
  6. Parâmetros e inferência — escolha do ESS, CPTs, respostas Q1–Q4 com checagem empírica. *(Tarefa 4)*
  7. Explicando uma predição. *(Tarefa 5)*
  8. Limitações e conclusão.
  9. Referências (formato único; mínimo: Koller & Friedman 2009; Poole & Mackworth 2023; Chow & Liu 1968; Schwarz 1978 (BIC); Heckerman, Geiger & Chickering 1995 (BDeu); Ankan & Panda — pgmpy; FAA Wildlife Strike Database + fieldlist).
- **Regras:** pt-BR; toda figura/tabela com `\ref` no texto; revisar com `.agents/skills/humanize-text` antes de fechar.
- **Next:** C13.

### C13 — Entrega

- **Type:** processo.
- **Job:** garantir que o que é submetido roda e bate com o relatório.
- **Passos:** (1) executar o notebook do zero num venv novo (`jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=1800`) e no Colab, se for o alvo; (2) conferir que os números citados no relatório são os da execução; (3) congelar `entregas/tp3_v<N>.ipynb` (com saídas) e `entregas/relatorio_v<N>.pdf`; (4) nunca sobrescrever uma versão já entregue.

---

## 10. Known Holes & Open Items

| # | Item | Status | Action |
|---|---|---|---|
| 1 | Prazo de entrega e forma de submissão desconhecidos | Blocker | Bruno informa (CONTEXT §9 #1) |
| 2 | Estados `desconhecido` (até 51% em `avisado`) podem gerar arestas espúrias entre variáveis que só compartilham a fonte do relato | Open | Quantificar em C8 com crosstab dos `desconhecido`; discutir. Definitiva (Phase 2): tratar como faltante e estimar com EM (`DiscreteEM`) ou modelar um nó "fonte do relato" |
| 3 | Segundo método não decidido (Chow-Liu recomendado; PC/MMHC alternativas) | Blocker | Bruno decide (CONTEXT §9 #3) |
| 4 | A FAA atualiza o zip; reexecutar pode mudar contagens (72.877 hoje) | Low risk | Notebook imprime contagens e data (`Last-Modified`); relatório cita a data do download; C3 avisa em vez de falhar se n ≠ 72.877 |
| 5 | CSV commitado alinhado com espaços | Low risk | C3 lê de forma robusta; notebook usa o CSV regenerado pelo script |
| 6 | `SPEED` é lida pelo script mas não vira nó; só `HEIGHT` é contínua discretizada | Open | Decidir com Bruno (CONTEXT §9 #6). Incluir `velocidade` em tercis reforça o requisito "contínuas em três faixas por quantis" e provavelmente se liga a `fase_voo`/`altura` |
| 7 | `M?` (dano indeterminado) codificado como `leve`; `EFFECT` vazio vira `nenhum` | Open | Justificar no relatório (C4); sensibilidade opcional removendo `M?` |
| 8 | Viés de seleção: removidas 65.745 linhas sem dano informado e 20.623 sem fase | Open | Discutir em Limitações; mostrar taxa de dano por ano estável (0,4–0,8% grave) |
| 9 | `nivel_dano` determinístico em relação a `houve_dano` | Low risk | Fora do aprendizado; C3 confirma por crosstab |
| 10 | Assinaturas pgmpy 1.1.2 não executadas (SHD com PDAG, `state_names` no estimador, log-prob) | Open | Smoke test (Build Order 1) |
| 11 | Repo privado: notebook não pode buscar nada do GitHub | Low risk | Script embutido via `%%writefile` (C2) |
| 12 | Leitura causal das intervenções (`do()`) depende de assumir o DAG aprendido como causal | Open | Ressalva explícita em C9/C10 e no relatório |
| 13 | TP individual ou em grupo; formato de citação; Overleaf ou local | Open | Bruno (CONTEXT §9 #2, #5) |

---

## 11. Build Order

1. **Smoke test da API** (C0) — criar `.venv`, rodar em `tmp/smoke.py` cada chamada de §7.2 sobre uma amostra de 5.000 linhas do CSV (lido via C3). Verificar: `HillClimbSearch(...).fit` + `causal_graph_` é `DAG`; `TreeSearch` chow-liu; `StructureScore("bic-d")`; `SHD` com DAG e com PDAG; `DiscreteBayesianNetwork.fit` com `DiscreteBayesianEstimator` e categorias completas; `VariableElimination.query`; `CausalInference.query(do=...)`; `get_markov_blanket`; `is_dconnected`. Corrigir §7.2/§9 se algo divergir.
2. **Esqueleto do notebook** (C1, C2, C3) — `notebook/tp3_redes_bayesianas.ipynb` com setup, script embutido, carga validada. Verificar: *Run all* local termina e imprime 72.877 linhas e 14 nós.
3. **Tarefa 1** (C4) — tabelas e gráfico de taxa de dano; perguntas Q1–Q4 fixadas com o Bruno.
4. **Tarefa 2** (C5) — `dag_elic` + figura com `POS` fixo. Verificar: 17 arestas, acíclico, figura igual ao PNG.
5. **Tarefa 3** (C6, C7, C8) — HC (tabu 100 e 0), Chow-Liu (ou método escolhido), comparação. Verificar: tabelas e figuras geradas; BIC(HC) ≥ BIC(elicitada) e ≥ BIC(Chow-Liu) — se não, investigar.
6. **Tarefa 4** (C9) — ESS por holdout, ajuste final, Q1–Q4 com checagem empírica. Verificar: `check_model()` ok; toda distribuição consultada soma 1; diferenças rede × empírico explicadas.
7. **Tarefa 5** (C10) — caso escolhido, todas as técnicas, texto gerado. Verificar: posterior com Markov blanket = posterior com evidência completa (tolerância 1e-9).
8. **Exportação** (C11) — figuras e tabelas em `relatorio/`.
9. **Relatório** (C12) — escrever, compilar, revisar com `humanize-text`.
10. **Entrega** (C13) — execução limpa, congelar em `entregas/`, push.

---

## 12. Appendices

### A. Test protocol

| Test | Input | Expected output | Result |
|---|---|---|---|
| T1 Versões | célula C1 | `pgmpy 1.1.2` impresso; assert passa | ⬜ |
| T2 Coleta | `!python coletar_birdstrikes.py` | `strikes_rede.csv` com 17 colunas, sem padding; `relatorio.md` gerado | ⬜ |
| T3 Carga | `carregar_base` | 72.877 linhas (ou diferença registrada), 0 NaN, nenhum estado fora de `STATE_NAMES` | ⬜ |
| T4 Determinismo do alvo | `crosstab(houve_dano, nivel_dano)` | só diagonais nao/nenhum e sim/{leve, grave} | ⬜ |
| T5 Elicitada | `dag_elic` | 14 nós, 17 arestas, acíclico | ⬜ |
| T6 HC | `dag_hc` | DAG (não PDAG), acíclico, 14 nós; BIC ≥ BIC(elicitada) | ⬜ |
| T7 Chow-Liu | `dag_cl` | árvore: 13 arestas, cada nó ≤ 1 pai, conexo | ⬜ |
| T8 Modelo | `modelo.check_model()` | True; todas as CPDs somam 1 por coluna | ⬜ |
| T9 Consultas | Q1–Q4 | cada fator soma 1; com suporte ≥ 500 linhas, |rede − empírico| < 2 p.p. (senão, explicar) | ⬜ |
| T10 Markov blanket | caso da Tarefa 5 | P(alvo | evidência completa) = P(alvo | só blanket) ± 1e-9 | ⬜ |
| T11 Reprodutibilidade | duas execuções completas | mesmas estruturas, mesmos números | ⬜ |
| T12 Execução limpa | venv novo / Colab, *Run all* | termina sem erro; tempo registrado | ⬜ |
| T13 Relatório | `latexmk -pdf main.tex` | compila sem `??` (refs quebradas); toda figura/tabela citada | ⬜ |

### B. AI test prompts

Não se aplica (o projeto não usa LLMs; o texto explicativo da Tarefa 5 é gerado por template).

### C. Mapeamento enunciado → entrega

| Item do enunciado | Onde é cumprido |
|---|---|
| §2 < 60 variáveis, categorias naturais, discretização justificada | C3, C4; relatório §2 |
| T1 domínio, faltantes, tercis por quantis, codificação, ≥1 pergunta | C4; relatório §1–2 |
| T2 estrutura desenhada à mão | C5; relatório §4 |
| T3 HC + BIC + outro método dos slides; comparação | C6–C8; relatório §3, §5 |
| T4 CPTs (MLE/bayesiano) + inferência com evidências variadas | C9; relatório §3, §6 |
| T5 explicar uma predição | C10; relatório §7 |
| §4 relatório LaTeX, figuras referenciadas, referências num formato | C11, C12 |
| §5 notebook reproduzível com discussão após cada bloco | C1–C11, C13 |
