from fastapi import FastAPI
import duckdb
import pandas as pd
import numpy as np

app = FastAPI(
    title="BAAI - Inteligência Analítica em Saúde",
    version="1.3"
)

# -----------------------------
# conexão MotherDuck
# -----------------------------
def get_connection():

    con = duckdb.connect("md:baai")

    return con


# -----------------------------
# limpeza dataframe
# -----------------------------
def clean_dataframe(df):

    df = df.replace([np.inf, -np.inf], None)
    df = df.replace({np.nan: None})

    return df


# -----------------------------
# root
# -----------------------------
@app.get("/")
def home():

    return {
        "sistema": "BAAI",
        "status": "API ativa",
        "engine": "DuckDB + MotherDuck"
    }


# -----------------------------
# health
# -----------------------------
@app.get("/health")
def health():

    return {"status": "ok"}


# -----------------------------
# mercado
# -----------------------------
@app.get("/mercado")
def mercado():

    con = get_connection()

    query = """
    SELECT *
    FROM baai_mercado_municipio
    LIMIT 100
    """

    df = con.execute(query).df()

    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# -----------------------------
# capacidade médica
# -----------------------------
@app.get("/capacidade_medica")
def capacidade_medica():

    con = get_connection()

    query = """
    SELECT *
    FROM baai_capacidade_medica
    LIMIT 100
    """

    df = con.execute(query).df()

    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# -----------------------------
# capacidade assistencial
# -----------------------------
@app.get("/capacidade_assistencial")
def capacidade_assistencial():

    con = get_connection()

    query = """
    SELECT *
    FROM baai_capacidade_assistencial
    LIMIT 100
    """

    df = con.execute(query).df()

    con.close()

    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# -----------------------------
# endpoint looker mercado
# -----------------------------
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


# -----------------------------
# endpoint looker capacidade médica
# -----------------------------
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


# -----------------------------
# endpoint looker capacidade assistencial
# -----------------------------
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
