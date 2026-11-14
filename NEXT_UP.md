# NEXT UP — tp3-redes-bayesianas

> Live worklist. Read this first every session; update it at every mission-end (and bump the date). Omit empty sections. Facts that change project state must also be written where that state lives (CONTEXT, plan status, Known Holes) — the ✅ log is only a handoff aid.

_Last updated: 2026-11-14_

## 🟡 In progress

- [ ] **Revisão do grupo** do notebook rev 2 e de `relatorio/main.pdf` (4 páginas, ABNT)
- [ ] **T12 da rev 2** — rodar `notebook/tp3_redes_bayesianas.ipynb` no Colab (*Run all*) e conferir que os números batem com o relatório (72.812 colisões; BIC camadas −697.125,0; caso 1577229 = 91,8%)

## 🟢 This week / next

- [ ] Bruno: matrícula da Eduarda Amaral (célula 0 do notebook e `\author` em `relatorio/main.tex`)
- [ ] C13 — entrega: congelar `entregas/tp3_v1.ipynb` + `entregas/relatorio_v1.pdf` depois dos dois itens acima

## ✅ Recently done (last 2 weeks)

- 2026-11-14 — Rev 2 (decidida pelo Bruno a partir de uma revisão externa): `qtd_atingida` fundida (base 72.812), **HC + BIC por camadas** como rede das Tarefas 4–5 (custo 1.010 de BIC), variante com `ingestao_motor → efeito_voo` forçada (conserta a Q2, estraga a Q3), Q4 = `do(tamanho_animal = pequeno)`, 2º caso da Tarefa 5 (falso negativo FAA 971157). Bug achado e corrigido: HC livre não determinístico (ordem de `set` + empates de BIC) → subclasse com desempate ordenado; 2 execuções com `PYTHONHASHSEED` diferentes → tabelas idênticas. Texto do notebook humanizado (skill humanize-text, `ai_tells.py` sem marcas). **Relatório** `relatorio/main.tex` → PDF de 4 páginas, 2 colunas, ABNT, compila sem `??`/overfull. Plano rev 1 arquivado. T12 da rev 1 feito pelo Bruno no Colab (pico ≈ 8 GB).

- 2026-11-14 — Notebook completo (`notebook/tp3_redes_bayesianas.ipynb`, Tarefas 1–5 + discussões) executado e validado: smoke test da API, saída do script idêntica, 2 execuções idênticas, HC determinístico em 6 sementes de hash, Markov blanket conferido numericamente, Q4 conferida com `CausalInference`. Decisões do Bruno registradas (Chow-Liu, Colab + local, Q1–Q4, sem extras). WSL caiu por memória (duas execuções em paralelo); causa medida e corrigida — kernel de 4,9 GB → 0,44 GB, Chow-Liu de 179 s → 10 s (plan bug log).
- 2026-11-14 — Bootstrap: repo `BrunoL28/tp3-redes-bayesianas` (privado), canonical files, agents-skills submodule, pastas `notebook/`, `relatorio/figuras/`, `entregas/`, `archive/`. Auditoria de prompt injection em `INPUTS/` (8 arquivos + `Public.xlsx`): todos **NÃO** — `archive/input-audits/2026-11-14-injection-audit.md`. Nenhum segredo encontrado. `INPUTS/dados/brutos/` gitignored (zip 133 MB > limite do GitHub). CONTEXT e plano rev 1 escritos a partir dos inputs; API do pgmpy 1.1.2 conferida no código-fonte (não executada). QA: clone novo com `--recurse-submodules` → arquivos canônicos + pastas presentes, submódulo com 25 skills, `.agents/skills/self-managed-project/SKILL.md` resolve ✅
