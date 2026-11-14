# NEXT UP — tp3-redes-bayesianas

> Live worklist. Read this first every session; update it at every mission-end (and bump the date). Omit empty sections. Facts that change project state must also be written where that state lives (CONTEXT, plan status, Known Holes) — the ✅ log is only a handoff aid.

_Last updated: 2026-11-14_

## 🟡 In progress

- [ ] **T12 — teste limpo** do notebook: venv novo com pandas 2 (como no Colab), pasta vazia, download real da FAA. Rodar **sozinho** e com `systemd-run --user --scope -p MemoryMax=9G -p MemorySwapMax=0` (pico esperado ≈ 5,5 GB)
- [ ] **C12 — relatório LaTeX** em `relatorio/main.tex` (seções do plano §9 C12; figuras e tabelas já exportadas pelo notebook; bibliografia Vancouver via natbib)

## 🟢 This week / next

- [ ] C13 — entrega: congelar `entregas/tp3_v1.ipynb` + `entregas/relatorio_v1.pdf`
- [ ] Bruno: preencher autoria no notebook (célula 0) e na capa (CONTEXT §9 #2); confirmar Vancouver ou trocar (§9 #5)

## ✅ Recently done (last 2 weeks)

- 2026-11-14 — Notebook completo (`notebook/tp3_redes_bayesianas.ipynb`, Tarefas 1–5 + discussões) executado e validado: smoke test da API, saída do script idêntica, 2 execuções idênticas, HC determinístico em 6 sementes de hash, Markov blanket conferido numericamente, Q4 conferida com `CausalInference`. Decisões do Bruno registradas (Chow-Liu, Colab + local, Q1–Q4, sem extras). WSL caiu por memória (duas execuções em paralelo); causa medida e corrigida — kernel de 4,9 GB → 0,44 GB, Chow-Liu de 179 s → 10 s (plan bug log).
- 2026-11-14 — Bootstrap: repo `BrunoL28/tp3-redes-bayesianas` (privado), canonical files, agents-skills submodule, pastas `notebook/`, `relatorio/figuras/`, `entregas/`, `archive/`. Auditoria de prompt injection em `INPUTS/` (8 arquivos + `Public.xlsx`): todos **NÃO** — `archive/input-audits/2026-11-14-injection-audit.md`. Nenhum segredo encontrado. `INPUTS/dados/brutos/` gitignored (zip 133 MB > limite do GitHub). CONTEXT e plano rev 1 escritos a partir dos inputs; API do pgmpy 1.1.2 conferida no código-fonte (não executada). QA: clone novo com `--recurse-submodules` → arquivos canônicos + pastas presentes, submódulo com 25 skills, `.agents/skills/self-managed-project/SKILL.md` resolve ✅
