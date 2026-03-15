from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import duckdb
import pandas as pd
import numpy as np
import os
import traceback

app = FastAPI(
    title="BAAI - Inteligência Analítica em Saúde",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"]
)

# ── Conexão MotherDuck ─────────────────────────────────────────
def get_connection():
    token = os.getenv("MOTHERDUCK_TOKEN")
    if not token:
        raise Exception("MOTHERDUCK_TOKEN ausente nas variáveis de ambiente")
    return duckdb.connect(f"md:baai?motherduck_token={token}")

# ── Limpeza de dataframe ───────────────────────────────────────
def clean_df(df):
    df = df.replace([np.inf, -np.inf], None)
    df = df.replace({np.nan: None})
    return df

# ── Executor genérico ──────────────────────────────────────────
def run(query: str, uf: str = None):
    try:
        con = get_connection()
        if uf:
            query += f" WHERE uf_ibge = '{uf}'"
        df = con.execute(query).df()
        con.close()
        return clean_df(df).to_dict(orient="records")
    except Exception as e:
        traceback.print_exc()
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))

# ── Root e health ──────────────────────────────────────────────
@app.get("/")
def home():
    return {"sistema": "BAAI", "versao": "2.0", "status": "API ativa"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ── Endpoints /looker/* (consumidos pelo Looker Studio) ────────

@app.get("/looker/mercado")
def looker_mercado(uf: str = Query(None)):
    return run("SELECT * FROM analytics_mercado_municipio", uf)

@app.get("/looker/capacidade")
def looker_capacidade(uf: str = Query(None)):
    return run("SELECT * FROM analytics_capacidade_assistencial", uf)

@app.get("/looker/pressao")
def looker_pressao(uf: str = Query(None)):
    return run("SELECT * FROM analytics_pressao_assistencial", uf)

@app.get("/looker/suficiencia")
def looker_suficiencia(uf: str = Query(None)):
    return run("SELECT * FROM analytics_suficiencia_especialidade", uf)

@app.get("/looker/oportunidade")
def looker_oportunidade(uf: str = Query(None)):
    return run("SELECT * FROM analytics_oportunidade_credenciamento", uf)

@app.get("/looker/dashboard_rede")
def looker_dashboard_rede(uf: str = Query(None)):
    return run("SELECT * FROM analytics_dashboard_rede", uf)

@app.get("/looker/score")
def looker_score(uf: str = Query(None)):
    return run("SELECT * FROM analytics_score_oportunidade", uf)

@app.get("/looker/roi")
def looker_roi(uf: str = Query(None)):
    return run("SELECT * FROM analytics_roi_clinica", uf)

# ── Endpoints legados mantidos por compatibilidade ─────────────
# (redirecionam para os nomes corretos)

@app.get("/mercado")
def mercado(uf: str = Query(None)):
    return run("SELECT * FROM analytics_mercado_municipio LIMIT 100")

@app.get("/capacidade_assistencial")
def capacidade_assistencial():
    return run("SELECT * FROM analytics_capacidade_assistencial LIMIT 100")
