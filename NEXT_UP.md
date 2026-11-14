# NEXT UP — tp3-redes-bayesianas

> Live worklist. Read this first every session; update it at every mission-end (and bump the date). Omit empty sections. Facts that change project state must also be written where that state lives (CONTEXT, plan status, Known Holes) — the ✅ log is only a handoff aid.

_Last updated: 2026-11-14_

## 🔴 Blockers

- [ ] Complete bootstrap → Bruno revisa `IMPLEMENTATION_PLAN.md` (§3 Scope, §9 C4 perguntas Q1–Q4, §9 C7 segundo método, §9 C9 BDeu/ESS, §10 Known Holes) e `CONTEXT.md`
- [ ] Bruno responde CONTEXT §9: **#1 prazo/forma de entrega**, **#3 segundo método** (Chow-Liu recomendado vs. PC/MMHC), **#4 Colab ou Jupyter local**

## 🟢 This week / next

- [ ] Build Order 1 — `.venv` + smoke test da API pgmpy 1.1.2 (`tmp/smoke.py`); corrigir plano §7.2/§9 se alguma assinatura divergir
- [ ] Build Order 2 — esqueleto do notebook (C1 setup, C2 script embutido via `%%writefile`, C3 carga validada)
- [ ] Build Order 3–4 — Tarefa 1 (tabelas, perguntas) e Tarefa 2 (`dag_elic` + figura)
- [ ] Respostas menores (CONTEXT §9 #2 grupo, #5 Overleaf/citação, #6 `SPEED`, #7 estações)

## 🔵 Deferred / Phase 2

- Tratar `desconhecido` como faltante com EM (`DiscreteEM`) em vez de estado — solução definitiva para arestas espúrias (plan Known Holes #2)
- Terceiro método (PC ou MMHC) e HC com `ExpertKnowledge` como comparações extras
- `nivel_dano` (3 estados) como alvo alternativo

## ✅ Recently done (last 2 weeks)

- 2026-11-14 — Bootstrap: repo `BrunoL28/tp3-redes-bayesianas` (privado), canonical files, agents-skills submodule, pastas `notebook/`, `relatorio/figuras/`, `entregas/`, `archive/`. Auditoria de prompt injection em `INPUTS/` (8 arquivos + `Public.xlsx`): todos **NÃO** — `archive/input-audits/2026-11-14-injection-audit.md`. Nenhum segredo encontrado. `INPUTS/dados/brutos/` gitignored (zip 133 MB > limite do GitHub). CONTEXT e plano rev 1 escritos a partir dos inputs; API do pgmpy 1.1.2 conferida no código-fonte (não executada).
