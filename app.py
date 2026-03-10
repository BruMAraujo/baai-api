from fastapi import FastAPI
import duckdb
import pandas as pd
import numpy as np

app = FastAPI(
    title="BAAI - Inteligência Analítica em Saúde",
    version="1.2"
)

# --------------------------------
# conexão MotherDuck
# --------------------------------
def get_connection():

    con = duckdb.connect()

    con.execute("INSTALL motherduck;")
    con.execute("LOAD motherduck;")

    con.execute("ATTACH 'md:baai'")

    return con


# --------------------------------
# limpeza dataframe
# --------------------------------
def clean_dataframe(df):

    df = df.replace([np.inf, -np.inf], None)
    df = df.replace({np.nan: None})

    return df


# --------------------------------
# root
# --------------------------------
@app.get("/")
def home():

    return {
        "sistema": "BAAI",
        "status": "API ativa",
        "engine": "DuckDB + MotherDuck"
    }


# --------------------------------
# health
# --------------------------------
@app.get("/health")
def health():

    return {"status": "ok"}


# --------------------------------
# mercado
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
    FROM baai.baai_mercado_municipio
    ORDER BY beneficiarios DESC
    LIMIT 100
    """

    df = con.execute(query).df()

    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# --------------------------------
# capacidade médica
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
    FROM baai.baai_capacidade_medica
    ORDER BY beneficiarios_por_profissional DESC
    LIMIT 100
    """

    df = con.execute(query).df()

    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# --------------------------------
# capacidade assistencial
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
    FROM baai.baai_capacidade_assistencial
    ORDER BY beneficiarios_por_profissional DESC
    LIMIT 100
    """

    df = con.execute(query).df()

    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# --------------------------------
# endpoint looker mercado
# --------------------------------
@app.get("/looker/mercado")
def looker_mercado():

    con = get_connection()

    query = """
    SELECT *
    FROM baai.baai_mercado_municipio
    """

    df = con.execute(query).df()

    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# --------------------------------
# endpoint looker capacidade médica
# --------------------------------
@app.get("/looker/capacidade_medica")
def looker_capacidade_medica():

    con = get_connection()

    query = """
    SELECT *
    FROM baai.baai_capacidade_medica
    """

    df = con.execute(query).df()

    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# --------------------------------
# endpoint looker capacidade assistencial
# --------------------------------
@app.get("/looker/capacidade_assistencial")
def looker_capacidade_assistencial():

    con = get_connection()

    query = """
    SELECT *
    FROM baai.baai_capacidade_assistencial
    """

    df = con.execute(query).df()

    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")
