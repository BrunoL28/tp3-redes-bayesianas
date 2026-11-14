#!/usr/bin/env python3
"""
Coleta e limpeza da FAA National Wildlife Strike Database para o TP de Redes Bayesianas.

Fonte: https://wildlife.faa.gov  ->  "Download Excel"
       arquivo estático: https://wildlife.faa.gov/assets/database_excel.zip  (~133 MB, contém Public.xlsx)
       dicionário de campos: https://wildlife.faa.gov/assets/fieldlist.pdf

Uso (da raiz do repo):
    pip install pandas requests python-calamine pyarrow
    python coletar_birdstrikes.py                      # baixa, lê, limpa
    python coletar_birdstrikes.py --ano-min 2017 --ano-max 2025   # recorte (padrão)
    python coletar_birdstrikes.py --sem-download       # reaproveita o zip já baixado

Saídas:
    dados/brutos/database_excel.zip          download original
    dados/brutos/strikes_bruto.parquet       planilha inteira convertida (leitura do Excel só acontece 1 vez)
    dados/processados/strikes_rede.csv       1 linha por colisão, só variáveis discretas para a rede
    dados/processados/relatorio.md           valores originais x agrupados, faltantes, dano por estado
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

URL = "https://wildlife.faa.gov/assets/database_excel.zip"
RAIZ = Path("dados")
BRUTOS, PROC = RAIZ / "brutos", RAIZ / "processados"
ZIP = BRUTOS / "database_excel.zip"
CACHE = BRUTOS / "strikes_bruto.parquet"

# Colunas usadas (nomes do fieldlist.pdf). Texto livre e dados de quem reportou ficam de fora.
COLUNAS = [
    "INDEX_NR", "INCIDENT_YEAR", "INCIDENT_MONTH", "TIME_OF_DAY", "PHASE_OF_FLIGHT",
    "HEIGHT", "SPEED", "SKY", "PRECIPITATION", "AC_MASS", "TYPE_ENG",
    "SPECIES", "SIZE", "NUM_STRUCK", "WARNED", "DAMAGE_LEVEL", "EFFECT",
    "ING_ENG1", "ING_ENG2", "ING_ENG3", "ING_ENG4",
]
# Alguns campos mudaram de nome entre versões da base; aceitamos os dois.
SINONIMOS = {
    "PHASE_OF_FLT": "PHASE_OF_FLIGHT",
    "PRECIP": "PRECIPITATION",
    "BIRDS_STRUCK": "NUM_STRUCK",
    "DAMAGE": "DAMAGE_LEVEL",
    "INDEX NR": "INDEX_NR",
}


# --------------------------------------------------------------------------- #
# 1. Download e leitura
# --------------------------------------------------------------------------- #
def baixar():
    import requests

    BRUTOS.mkdir(parents=True, exist_ok=True)
    print(f"Baixando {URL} (~133 MB)...")
    with requests.get(URL, stream=True, timeout=120) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        feito = 0
        with open(ZIP, "wb") as f:
            for bloco in r.iter_content(1 << 20):
                f.write(bloco)
                feito += len(bloco)
                if total:
                    print(f"\r  {feito / total:6.1%}", end="")
    print("\n  ok")


def ler_planilha() -> pd.DataFrame:
    if CACHE.exists():
        print(f"Lendo cache {CACHE}")
        return pd.read_parquet(CACHE)
    if not ZIP.exists():
        sys.exit(f"{ZIP} não existe. Rode sem --sem-download.")
    print("Lendo o Excel (360 mil linhas; com python-calamine leva ~1–2 min)...")
    with zipfile.ZipFile(ZIP) as z:
        nome = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
        with z.open(nome) as f:
            try:
                df = pd.read_excel(f, engine="calamine", dtype=str)
            except (ImportError, ValueError):
                print("  python-calamine ausente: usando openpyxl (bem mais lento, ~10 min)")
                df = pd.read_excel(f, engine="openpyxl", dtype=str)
    df.columns = [str(c).strip().upper() for c in df.columns]
    df = df.rename(columns={k: v for k, v in SINONIMOS.items() if k in df.columns and v not in df.columns})
    try:
        df.to_parquet(CACHE, index=False)
        print(f"  cache salvo em {CACHE}")
    except ImportError:
        print("  (instale pyarrow para salvar o cache e não reler o Excel)")
    return df


# --------------------------------------------------------------------------- #
# 2. Funções de agrupamento
# --------------------------------------------------------------------------- #
def norm(s: pd.Series) -> pd.Series:
    """Texto em minúsculas, sem espaços extras; vazios viram NA."""
    s = s.astype("string").str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
    return s.replace({"": pd.NA, "nan": pd.NA, "none specified": pd.NA, "unknown": pd.NA})


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def booleano(s: pd.Series) -> pd.Series:
    m = {"true": True, "1": True, "y": True, "yes": True, "-1": True,
         "false": False, "0": False, "n": False, "no": False}
    return norm(s).map(m)


def por_regras(s: pd.Series, regras: list[tuple[str, str]], padrao="outro", faltante="desconhecido"):
    """Aplica a primeira regex que casar. Regras em ordem de prioridade."""
    def f(v):
        if pd.isna(v):
            return faltante
        for rotulo, padrao_re in regras:
            if re.search(padrao_re, v):
                return rotulo
        return padrao
    return norm(s).map(f)


FASE = [
    ("corrida_decolagem", r"take.?off|takeoff"),
    ("subida", r"climb|departure"),
    ("rota", r"en ?route|local"),
    ("aproximacao", r"approach|descent|arrival"),
    ("corrida_pouso", r"landing"),
    ("solo_taxi", r"taxi|parked"),
]
PERIODO = [("amanhecer", r"dawn"), ("dia", r"^day"), ("anoitecer", r"dusk"), ("noite", r"night")]
CEU = [("sem_nuvens", r"no cloud"), ("algumas_nuvens", r"some cloud"), ("encoberto", r"overcast")]
TAMANHO = [("pequeno", r"small"), ("medio", r"medium"), ("grande", r"large")]
QTD = [("um", r"^1$"), ("2_a_10", r"2.?-.?10"), ("mais_de_10", r"11|over|more")]
MOTOR = [  # códigos A–F do fieldlist.pdf
    ("pistao", r"^a$"), ("jato", r"^[bd]$"), ("turboelice", r"^c$"),
    ("helicoptero", r"^f$"),
    ("desconhecido", r"^[ey]$"),  # planador/outro: só 4 casos
]
EFEITO = [
    ("desligamento_motor", r"engine shut"),
    ("decolagem_abortada", r"abort"),
    ("pouso_precaucao", r"precaution"),
    ("nenhum", r"^none$"),
]
NAO_AVES = [
    # aves cujo nome contém palavra de mamífero (killdeer, rock pigeon, cattle egret, fox sparrow...)
    ("ave", r"\bbird|killdeer|pigeon|dove|egret|sparrow|heron|hawk|owl|gull|duck|goose"),
    ("morcego", r"\bbats?\b"),
    ("terrestre", r"\b(deer|coyotes?|fox(es)?|rabbits?|jackrabbits?|hares?|skunks?|raccoons?|armadillos?|dogs?|"
                  r"cats?|opossums?|woodchucks?|groundhogs?|squirrels?|muskrats?|beavers?|elk|moose|pronghorn|"
                  r"antelopes?|cattle|horses?|pigs?|hogs?|bears?|marmots?|badgers?|minks?|otters?|porcupines?|"
                  r"turtles?|tortoises?|alligators?|snakes?|lizards?|iguanas?|terrapins?)\b"),
]


def dano(s: pd.Series) -> pd.Series:
    # N nenhum | M leve | M? indeterminado (houve dano) | S substancial | D destruído | vazio = desconhecido
    m = {"n": "nenhum", "m": "leve", "m?": "leve", "s": "grave", "d": "grave"}  # M? = houve dano, nível indeterminado
    return norm(s).map(m)


def tercis_com_zero(s: pd.Series, rot0: str, rotulos=("baixa", "media", "alta")) -> pd.Series:
    """Zero vira um estado próprio (no solo / parado); o resto em tercis, como pede o enunciado."""
    out = pd.Series("desconhecido", index=s.index, dtype="string")
    out[s == 0] = rot0
    pos = s > 0
    if pos.sum() > 3:
        cod = pd.qcut(s[pos], 3, labels=False, duplicates="drop")  # empates podem fundir faixas
        n = int(cod.max()) + 1
        nomes = list(rotulos) if n == 3 else [rotulos[0], rotulos[-1]][:n]
        out[pos] = cod.map(lambda c: nomes[int(c)])
    return out


# --------------------------------------------------------------------------- #
# 3. Limpeza
# --------------------------------------------------------------------------- #
def limpar(df: pd.DataFrame, ano_min: int, ano_max: int) -> tuple[pd.DataFrame, list[str]]:
    faltam = [c for c in COLUNAS if c not in df.columns]
    if faltam:
        print("ATENÇÃO, colunas não encontradas:", faltam)
        print("Colunas disponíveis:", ", ".join(df.columns))
    rel = [f"# Relatório — FAA Wildlife Strikes\n",
           f"- linhas na planilha: {len(df):,}; colunas: {df.shape[1]}"]

    d = df.copy()
    for c in COLUNAS:  # coluna ausente vira vazia (aparece como "desconhecido") em vez de quebrar
        if c not in d.columns:
            d[c] = pd.NA
    d["ano"] = num(d["INCIDENT_YEAR"])
    d = d[d["ano"].between(ano_min, ano_max)]
    rel.append(f"- de {ano_min} a {ano_max}: {len(d):,}")

    d["dano"] = dano(d["DAMAGE_LEVEL"])
    rel.append(f"- sem nível de dano informado (removidas): {d['dano'].isna().sum():,}")
    d = d[d["dano"].notna()].copy()
    # sem fase do voo = em geral carcaça achada na pista, sem relato do voo (quase tudo vira "desconhecido")
    sem_fase = norm(d["PHASE_OF_FLIGHT"]).isna()
    rel.append(f"- sem fase do voo (carcaças sem relato; removidas): {sem_fase.sum():,}")
    d = d[~sem_fase].copy()

    out = pd.DataFrame(index=d.index)
    out["id"] = d["INDEX_NR"]
    out["ano"] = d["ano"].astype(int)

    mes = num(d["INCIDENT_MONTH"])
    out["estacao"] = mes.map(lambda m: "desconhecido" if pd.isna(m) else
                             {12: "inverno", 1: "inverno", 2: "inverno", 3: "primavera", 4: "primavera",
                              5: "primavera", 6: "verao", 7: "verao", 8: "verao"}.get(int(m), "outono"))
    out["periodo"] = por_regras(d["TIME_OF_DAY"], PERIODO)
    out["fase_voo"] = por_regras(d["PHASE_OF_FLIGHT"], FASE)
    out["altura"] = tercis_com_zero(num(d["HEIGHT"]), "solo")
    out["ceu"] = por_regras(d["SKY"], CEU)

    massa = num(d["AC_MASS"])
    out["massa_aeronave"] = massa.map(lambda m: "desconhecido" if pd.isna(m) else
                                      ("leve" if m <= 2 else "media" if m == 3 else "pesada"))
    out["motor"] = por_regras(d["TYPE_ENG"], MOTOR)

    out["animal"] = por_regras(d["SPECIES"], NAO_AVES, padrao="ave", faltante="ave")
    out["tamanho_animal"] = por_regras(d["SIZE"], TAMANHO)
    out["qtd_atingida"] = por_regras(d["NUM_STRUCK"], QTD)
    out["avisado"] = booleano(d["WARNED"]).map({True: "sim", False: "nao"}).fillna("desconhecido")

    ing = pd.concat([booleano(d[c]) for c in ["ING_ENG1", "ING_ENG2", "ING_ENG3", "ING_ENG4"]], axis=1)
    out["ingestao_motor"] = ing.fillna(False).any(axis=1).map({True: "sim", False: "nao"})

    out["houve_dano"] = d["dano"].map({"nenhum": "nao", "leve": "sim", "grave": "sim"})
    out["nivel_dano"] = d["dano"]  # 3 estados; use se quiser trabalhar a gravidade
    out["efeito_voo"] = por_regras(d["EFFECT"], EFEITO, padrao="outro", faltante="nenhum")

    # ---- relatório: valores ORIGINAIS de cada coluna categórica (para conferir os agrupamentos)
    rel.append("\n## Valores originais (top 15) — conferir se os agrupamentos cobrem tudo")
    for c in ["TIME_OF_DAY", "PHASE_OF_FLIGHT", "SKY", "PRECIPITATION", "AC_MASS", "TYPE_ENG",
              "SIZE", "NUM_STRUCK", "WARNED", "DAMAGE_LEVEL", "EFFECT", "ING_ENG1"]:
        if c in df.columns:
            vc = df.loc[d.index, c].astype("string").fillna("<vazio>").value_counts().head(15)
            rel.append(f"\n### {c}\n```\n{vc.to_string()}\n```")
    for grupo in ["morcego", "terrestre"]:
        esp = d.loc[out["animal"].eq(grupo), "SPECIES"].value_counts().head(15)
        rel.append(f"\n### Espécies em '{grupo}' (top 15)\n```\n{esp.to_string()}\n```")

    return out, rel


def resumo(out: pd.DataFrame, rel: list[str]):
    rel.append(f"\n## Base final: {len(out):,} colisões, {out.shape[1] - 3} nós (+ nivel_dano extra)")
    rel.append("\n## Nível de dano por ano (%)\n```\n" +
               pd.crosstab(out["ano"], out["nivel_dano"], normalize="index").mul(100).round(1).to_string() + "\n```")
    for c in [c for c in out.columns if c not in ("id", "ano", "nivel_dano")]:
        t = pd.crosstab(out[c], out["nivel_dano"], margins=True, margins_name="total")
        pct = (t.div(t["total"], axis=0) * 100).round(1)
        tab = t[["total"]].join(pct.drop(columns="total").add_prefix("%"))
        rel.append(f"\n### {c}\n```\n{tab.to_string()}\n```")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sem-download", action="store_true")
    p.add_argument("--ano-min", type=int, default=2017)  # critério de dano estável a partir daqui
    p.add_argument("--ano-max", type=int, default=2025)  # 2026 ainda incompleto
    a = p.parse_args()
    if not a.sem_download and not ZIP.exists():
        baixar()
    df = ler_planilha()
    out, rel = limpar(df, a.ano_min, a.ano_max)
    resumo(out, rel)
    PROC.mkdir(parents=True, exist_ok=True)
    out.to_csv(PROC / "strikes_rede.csv", index=False)
    (PROC / "relatorio.md").write_text("\n".join(rel), encoding="utf-8")
    print(f"\nPronto: {PROC / 'strikes_rede.csv'} ({len(out):,} linhas) e {PROC / 'relatorio.md'}")


if __name__ == "__main__":
    main()