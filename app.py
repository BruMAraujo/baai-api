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
        fr
