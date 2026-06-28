import sqlite3
import json
import pandas as pd
import plotly.express as px

DB_PATH = "sample.db"

def get_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    schema = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema[table_name] = [
            {"column": col[1], "type": col[2]}
            for col in columns
        ]
    conn.close()
    return json.dumps(schema, indent=2)

def execute_query(sql):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        return None

def generate_chart(df, chart_type, x_col, y_col, title):
    try:
        if chart_type == "bar":
            fig = px.bar(df, x=x_col, y=y_col, title=title)
        elif chart_type == "line":
            fig = px.line(df, x=x_col, y=y_col, title=title)
        elif chart_type == "pie":
            fig = px.pie(df, names=x_col, values=y_col, title=title)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col, title=title)
        else:
            return None
        return fig
    except Exception:
        return None

def generate_flowchart(diagram_type="er"):
    er_diagram = """erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    PRODUCTS ||--o{ ORDERS : contains
    CUSTOMERS { int id string name string city }
    PRODUCTS { int id string name float price }
    ORDERS { int id int quantity float revenue }"""

    process_diagram = """flowchart LR
    A[User Question] --> B[LLM]
    B --> C{DB?}
    C -->|Yes| D[SQL]
    C -->|No| G[Answer]
    D --> E[(DB)]
    E --> F[Chart]
    F --> I[Show User]
    G --> I"""

    if diagram_type == "er":
        return er_diagram
    else:
        return process_diagram
def explain_data(df):
    if isinstance(df, pd.DataFrame) and not df.empty:
        summary = f"Found {len(df)} records with {len(df.columns)} columns.\n"
        for col in df.select_dtypes(include='number').columns:
            summary += f"{col}: min={df[col].min()}, max={df[col].max()}, avg={df[col].mean():.2f}\n"
        return summary
    return "No data found."