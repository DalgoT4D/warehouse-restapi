import os
from fastapi import FastAPI, HTTPException, Header
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# clients warehouse
warehouse_config = {
    "dbname": os.getenv("WAREHOUSE_DB_NAME"),
    "user": os.getenv("WAREHOUSE_DB_USER"),
    "password": os.getenv("WAREHOUSE_DB_PASSWORD"),
    "host": os.getenv("WAREHOUSE_DB_HOST"),
    "port": os.getenv("WAREHOUSE_DB_PORT"),
}

# our multi tenant db
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


def execute_warehouse_query(query, data=None):
    conn = psycopg2.connect(**warehouse_config)
    cur = conn.cursor()
    cur.execute(query, data)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result


def execute_db_query(query, data=None):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute(query, data)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result


def check_valid_api_key(api_key: str):
    query = f"SELECT id FROM orgs WHERE api_key = '{api_key}'"
    result = execute_db_query(query)
    if len(result) == 0:
        return False
    return True


@app.post("/api/read/")
def read_records(filter_data: dict, authorization: str = Header(None)):
    if authorization is None:
        return HTTPException(status_code=401, detail="unauthorized")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    api_key = authorization.split("Bearer ")[1]

    if not check_valid_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid api key")

    page = filter_data.get("page", 1)
    limit = filter_data.get("limit", 10)
    tablename = filter_data.get("tablename", "")
    select_cols = filter_data.get("select_cols", [])
    # [{"col_name": "<>", "search": "<>", "lt": "", "gt": ""}]
    conds = filter_data.get("where", [])

    if tablename is None or tablename == "":
        raise HTTPException(status_code=400, detail="tablename is required")

    offset = (page - 1) * limit
    col_names = ",".join(select_cols) if len(select_cols) > 0 else "*"
    where = "WHERE 1=1 "
    for cond in conds:
        if cond.get("search", "") != "":
            where += f" AND {cond.get('col_name', '')} ILIKE '%{cond.get('search', '')}%' "

        if cond.get("lt", "") != "":
            where += f" AND {cond.get('col_name', '')} < {cond.get('lt', '')} "

        if cond.get("gt", "") != "":
            where += f" AND {cond.get('col_name', '')} > {cond.get('gt', '')} "

    query = f"SELECT {col_names} FROM {tablename} {where} LIMIT {limit} OFFSET {offset}"
    results = execute_warehouse_query(query)
    return results
