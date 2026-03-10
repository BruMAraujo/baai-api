from fastapi import FastAPI
import duckdb
import pandas as pd
import numpy as np

app = FastAPI(
    title="BAAI - Inteligência Analítica em Saúde",
    version="1.0"
)

# --------------------------------
# Banco de dados (MotherDuck)
# --------------------------------
DB_PATH = "md:baai"


# --------------------------------
# Conexão segura com o banco
# --------------------------------
def get_connection():
    return duckdb.connect(DB_PATH, read_only=True)


# --------------------------------
# Limpeza de dados para JSON
# remove NaN e Infinity
# --------------------------------
def clean_dataframe(df):

    df = df.replace([np.inf, -np.inf], None)
    df = df.replace({np.nan: None})

    return df


# --------------------------------
# Endpoint raiz
# --------------------------------
@app.get("/")
def home():
    return {
        "sistema": "BAAI",
        "status": "API ativa",
        "engine": "DuckDB + MotherDuck"
    }


# --------------------------------
# Health check (Render / Monitoramento)
# --------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# --------------------------------
# Mercado de saúde suplementar
# --------------------------------
@app.get("/mercado")
def mercado():

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
    FROM baai_mercado_municipio
    ORDER BY beneficiarios DESC
    LIMIT 100
    """

    df = con.execute(query).df()
    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# --------------------------------
# Capacidade médica
# --------------------------------
@app.get("/capacidade_medica")
def capacidade_medica():

    con = get_connection()

    query = """
    SELECT
        municipio,
        profissao,
        profissionais,
        beneficiarios,
        beneficiarios_por_profissional
    FROM baai_capacidade_medica
    ORDER BY beneficiarios_por_profissional DESC
    LIMIT 100
    """

    df = con.execute(query).df()
    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# --------------------------------
# Capacidade assistencial geral
# --------------------------------
@app.get("/capacidade_assistencial")
def capacidade_assistencial():

    con = get_connection()

    query = """
    SELECT
        municipio,
        especialidade_grupo,
        profissionais,
        beneficiarios,
        beneficiarios_por_profissional
    FROM baai_capacidade_assistencial
    ORDER BY beneficiarios_por_profissional DESC
    LIMIT 100
    """

    df = con.execute(query).df()
    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# --------------------------------
# Endpoint completo para Looker
# --------------------------------
@app.get("/looker/mercado")
def looker_mercado():

    con = get_connection()

    query = """
    SELECT *
    FROM baai_mercado_municipio
    """

    df = con.execute(query).df()
    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# --------------------------------
# Endpoint completo capacidade médica
# --------------------------------
@app.get("/looker/capacidade_medica")
def looker_capacidade_medica():

    con = get_connection()

    query = """
    SELECT *
    FROM baai_capacidade_medica
    """

    df = con.execute(query).df()
    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# --------------------------------
# Endpoint completo capacidade assistencial
# --------------------------------
@app.get("/looker/capacidade_assistencial")
def looker_capacidade_assistencial():

    con = get_connection()

    query = """
    SELECT *
    FROM baai_capacidade_assistencial
    """

    df = con.execute(query).df()
    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


