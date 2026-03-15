from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import duckdb
import pandas as pd
import numpy as np
import os
import traceback

app = FastAPI(
    title="BAAI - Inteligência Analítica em Saúde",
    version="2.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"]
)

# ------------------------------
# Conexão MotherDuck
# ------------------------------
def get_connection():
    token = os.getenv("MOTHERDUCK_TOKEN")

    if not token:
        raise Exception("MOTHERDUCK_TOKEN não configurado")

    return duckdb.connect(f"md:baai?motherduck_token={token}")


# ------------------------------
# Limpeza dataframe
# ------------------------------
def clean_df(df):
    df = df.replace([np.inf, -np.inf], None)
    df = df.replace({np.nan: None})
    return df


# ------------------------------
# Home
# ------------------------------
@app.get("/")
def home():
    return {
        "sistema": "BAAI",
        "versao": "2.1",
        "status": "API ativa"
    }


# ------------------------------
# Health check
# ------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ------------------------------
# Endpoint MERCADO (CSV)
# ------------------------------
@app.get("/looker/mercado")
def looker_mercado():

    try:

        con = get_connection()

        query = """
        SELECT
            cod_municipio,
            municipio,
            populacao,
            beneficiarios,
            estabelecimentos,
            taxa_suplementar,
            beneficiarios_por_estabelecimento,
            estab_por_100k_hab
        FROM analytics_mercado_municipio
        LIMIT 500
        """

        df = con.execute(query).df()

        con.close()

        df = clean_df(df)

        return df.to_csv(index=False)

    except Exception as e:

        traceback.print_exc()

        return {"erro": str(e)}


# ------------------------------
# Endpoint CAPACIDADE
# ------------------------------
@app.get("/looker/capacidade")
def looker_capacidade():

    con = get_connection()

    query = """
    SELECT *
    FROM analytics_capacidade_assistencial
    LIMIT 500
    """

    df = con.execute(query).df()

    con.close()

    df = clean_df(df)

    return df.to_dict(orient="records")


# ------------------------------
# Endpoint PRESSAO
# ------------------------------
@app.get("/looker/pressao")
def looker_pressao():

    con = get_connection()

    query = """
    SELECT *
    FROM analytics_pressao_assistencial
    LIMIT 500
    """

    df = con.execute(query).df()

    con.close()

    df = clean_df(df)

    return df.to_dict(orient="records")


# ------------------------------
# Endpoint SUFICIENCIA
# ------------------------------
@app.get("/looker/suficiencia")
def looker_suficiencia():

    con = get_connection()

    query = """
    SELECT *
    FROM analytics_suficiencia_especialidade
    LIMIT 500
    """

    df = con.execute(query).df()

    con.close()

    df = clean_df(df)

    return df.to_dict(orient="records")

from fastapi.responses import PlainTextResponse

@app.get("/looker/mercado_csv", response_class=PlainTextResponse)
def looker_mercado_csv():

    con = get_connection()

    query = """
    SELECT
        cod_municipio,
        municipio,
        populacao,
        beneficiarios,
        estabelecimentos,
        taxa_suplementar,
        beneficiarios_por_estabelecimento,
        estab_por_100k_hab
    FROM analytics_mercado_municipio
    LIMIT 500
    """

    df = con.execute(query).df()
    con.close()

    csv = df.to_csv(index=False)

    return csv
