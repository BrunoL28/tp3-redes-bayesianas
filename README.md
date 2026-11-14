# tp3-redes-bayesianas

> **TL;DR** — TP3 de *Fundamentos de Inteligência Artificial* (DEE): construir, aprender (Hill-Climbing/BIC + um segundo método), parametrizar, consultar e explicar uma **rede bayesiana** sobre a base de colisões de fauna com aeronaves da FAA (2017–2025, 72.812 colisões, 14 nós). Entregáveis: **notebook reproduzível** (instala dependências, baixa a base, roda o tratamento e todas as tarefas) + **relatório em LaTeX**. Fase atual: **Phase 1 — notebook (rev 2) e relatório prontos para revisão do grupo; falta a entrega (`entregas/`)**.

This is a **self-managed project**: all working state lives in versioned markdown in this repo. Agents and humans resume from the docs below — no handoff call needed. Protocol: [`.agents-skills/.agents/skills/self-managed-project/SKILL.md`](.agents-skills/.agents/skills/self-managed-project/SKILL.md).

## Onboarding order

Read in this order:

1. [`NEXT_UP.md`](NEXT_UP.md) — what is being worked on right now, and what's blocking.
2. [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) — start at **Current Implementation Status**.
3. [`CLAUDE.md`](CLAUDE.md) / [`AGENTS.md`](AGENTS.md) — rules for agents in this repo.
4. [`CONTEXT.md`](CONTEXT.md) — domain background (enunciado, dados, rede elicitada).

## Stack

| Layer | Tech | Notes |
|---|---|---|
| Linguagem | Python 3.12 (local: WSL Ubuntu, `python3` 3.12.3) | `pip` do sistema bloqueado (PEP 668) → usar `.venv/` (gitignored) |
| Redes bayesianas | **pgmpy 1.1.2** (fixar versão) | API nova `pgmpy.causal_discovery.HillClimbSearch(...).fit(df)`; a antiga `pgmpy.estimators.HillClimbSearch` emite `FutureWarning` |
| Dados | pandas, pyarrow, python-calamine, requests | Leitura do `Public.xlsx` (FAA) via calamine (~1–2 min) |
| Grafos / figuras | networkx, matplotlib (graphviz opcional) | Figuras exportadas para `relatorio/figuras/` |
| Notebook | Jupyter (`.ipynb`), executável no Colab ou local | Deve ser **autossuficiente**: `pip install`, download da base, tratamento, tarefas 1–5 |
| Relatório | LaTeX local (`relatorio/main.tex`, `latexmk -pdf`) | 2 colunas, até 4 páginas; referências em ABNT |

## Quick links

| What | Link |
|---|---|
| Repo | <https://github.com/BrunoL28/tp3-redes-bayesianas> (privado) |
| Fonte dos dados | <https://wildlife.faa.gov> — zip estático `https://wildlife.faa.gov/assets/database_excel.zip` (~133 MB) |
| Dicionário oficial de campos | <https://wildlife.faa.gov/assets/fieldlist.pdf> |
| Documentação pgmpy | <https://pgmpy.org> |

Credentials: o projeto não usa segredos até agora. Se surgir algum, criar `CREDENTIALS.md` (repo privado) — nunca em outro lugar.

## Repository layout

```
.
├── README.md                 # this file
├── CONTEXT.md                # enunciado, domínio, dados e rede elicitada (destilados)
├── IMPLEMENTATION_PLAN.md    # current plan (rev N) — old revisions in archive/
├── NEXT_UP.md                # live worklist
├── CLAUDE.md / AGENTS.md     # agent rules
├── INPUTS/                   # raw material (read-only) — enunciado, slides, rede da Tarefa 2, script, dados
│   └── dados/brutos/         #   ⚠ gitignored (zip de 133 MB > limite de 100 MB do GitHub) — regenerar pelo script
├── notebook/                 # notebook de trabalho (git-versionado)
├── relatorio/                # fonte LaTeX do relatório + figuras/
├── entregas/                 # snapshots congelados do que for submetido (versão no nome: tp3_v1.ipynb, relatorio_v1.pdf)
├── archive/                  # old revisions + input-audits/ — never delete
├── tmp/                      # scratch (gitignored)
└── .agents-skills/           # agents-skills submodule (symlinked to .agents and .claude/skills)
```

## Getting started (fresh clone)

```bash
git clone --recurse-submodules https://github.com/BrunoL28/tp3-redes-bayesianas && cd tp3-redes-bayesianas
ln -s .agents-skills/.agents .agents
mkdir -p .claude && ln -s ../.agents-skills/.agents/skills .claude/skills
python3 -m venv .venv && .venv/bin/pip install "pgmpy==1.1.2" pandas pyarrow python-calamine requests matplotlib jupyter
# dados brutos não vêm no clone: o notebook (ou o script) baixa da FAA
```

_Last updated: 2026-11-14_
