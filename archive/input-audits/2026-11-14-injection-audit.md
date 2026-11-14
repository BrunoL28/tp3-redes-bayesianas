# Auditoria de prompt injection

**Data:** 2026-11-14 · **Arquivos analisados:** 8 (+ `Public.xlsx` extraído do zip) · **Scanner estrutural:** executado (`scan_injection.py` + PyMuPDF em `tmp/venv`) para PDF/MD/PY/CSV; para XLSX/Parquet foi feita varredura das strings com os mesmos `INSTRUCTION_PATTERNS` do scanner + busca de caracteres invisíveis (zero-width, bidi, Unicode tags).

Modo: ingestão (`INPUTS/`), executado antes de qualquer leitura/destilação para `CONTEXT.md`.

## Veredito

| Arquivo | Papel no trabalho | sha256 | Prompt injection |
|---|---|---|---|
| `INPUTS/requirements.md` | enunciado (adaptado) — guia o trabalho | 8dc8178384fa1aaf69be8c8792e24a523cf4af7793bdfcee5e83a60ddb882960 | **NÃO** |
| `INPUTS/FUND_IA_Chapter_9_RBs_BNSL (1).pdf` | referência (slides do curso, 63 p.) | 784cdfebbfe452f896241a111d4b331bb420d9d7cc3fd33aefc63b78a588abe3 | **NÃO** |
| `INPUTS/rede_etapa2.png` | rede elicitada manualmente (Tarefa 2) | c681d254fac2b5ab6d1f51e30d1fc97614b132d379aad04bb57176150b4820a1 | **NÃO** |
| `INPUTS/scripts/coletar_birdstrikes.py` | script de coleta/limpeza | 03a6f3481f80c9abdfe7647704b8890cc5b9c669ac1b0810d84868b1f7979972 | **NÃO** |
| `INPUTS/dados/processados/relatorio.md` | dicionário/relatório gerado pelo script | 306f34e7488e4f13bab250350e65244633c7c929be308d15d928f7381111f14a | **NÃO** |
| `INPUTS/dados/processados/strikes_rede.csv` | base tratada (72.877 linhas) | 3030fd42c059442119bd8325f06efa21f05d4b90aed1732cbcf894aa4c149f1f | **NÃO** |
| `INPUTS/dados/brutos/strikes_bruto.parquet` | cache da planilha bruta (360.384 × 102) | 2bff48566e46f527d11abdf6c8be231215032c05fd512949d7d6aec170e1df0b | **NÃO** |
| `INPUTS/dados/brutos/database_excel.zip` (→ `Public.xlsx`) | download original da FAA | c9f866fa76bfcb5a14934c12b0596ad2c98e6fe1a910178665e9c06b88e1db84 | **NÃO** |

## Itens descartados

- `FUND_IA_Chapter_9…pdf`, p. 63, bboxes (8,3,173,14), (16,20,128,31), (8,57,113,68) — scanner: "text painted over by a later shade" (HIGH) — legítimo: são o título, a seção e o título do frame do tema Beamer; o render (`tmp/audit/png/…p063.png`) mostra os três textos visíveis sobre as faixas coloridas. Texto da camada idêntico ao visível.
- `FUND_IA_Chapter_9…pdf` — 128 links: todos internos (navegação Beamer), nenhum URI externo. Sem anotações, sem arquivos embutidos; metadados (título/autores/pdfTeX) sem texto instrucional.
- `Public.xlsx` / `strikes_bruto.parquet` — 527 ocorrências do padrão de nomes de modelos de IA: 514× "COPILOT" (copiloto da aeronave nos campos `REMARKS`/`COMMENTS`), "GEMINI AIR CARGO"/"GEMINI AVIATION SERVICES" (operadores), "CLAUDE MOREAU" (operador), "RIDGELAND-CLAUDE DEAN AIRPORT", "MIST" (METAR). Legítimo: texto livre de relatos de pilotos/aeroportos.
- `Public.xlsx` / parquet — "DO NOT MENTION" (2×: "AIRPORT RECORDS AT CLT DO NOT MENTION DMG"), "NEW INSTRUCTIONS" (1×: ATC "ISSUED NEW INSTRUCTIONS OF RWY HEADING"), "RATHER THAN … ASSUME" (3×: relatos operacionais) — legítimo: linguagem operacional de aviação.
- `Public.xlsx` — heurística extra "AI/assistant/instruction" (356 strings): voos de instrução ("INSTRUCTION FLT"), "AIRFIELD ASSISTANT", taxiway "AI", truncamentos de "AIRCRAFT", voo Air India "AI-101", motor "AI-25TL". Legítimo.
- `Public.xlsx` — estrutura: 1 planilha visível (`Sheet1`), sem planilhas ocultas, sem comentários, sem `docProps`, sem macros. Nenhuma string com caracteres invisíveis em 609.588 shared strings / 27,7 M strings do parquet.
- `rede_etapa2.png` — PNG com apenas chunks `IHDR`/`IDAT`/`IEND`, sem chunks de texto e sem bytes após `IEND`; conteúdo visual = diagrama da rede (14 nós).

## Limitações desta análise

- As figuras dentro do PDF (p. 16–18, 23–25, 29, 32, 41, 44, 46, 54 só têm título na camada de texto) não passaram por OCR; texto em imagem é visível ao humano igualmente, então não constitui texto oculto, mas não foi lido semanticamente.
- `strikes_rede.csv` contém apenas rótulos categóricos (sem texto livre), varrido pelo scanner de texto.
- Os campos de texto livre da base bruta (`REMARKS`, `COMMENTS`, `OTHER_SPECIFY`, `EFFECT_OTHER`) **não** entram na rede bayesiana (o script não os usa), o que reduz o risco residual a zero para o trabalho em si.
