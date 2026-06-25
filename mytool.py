import sqlite3
import json
import pandas as pd
import plotly.express as px

DB_PATH = "sample.db"

# Tool 1: Get Schema
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

# Tool 2: Execute Query
def execute_query(sql):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 3: Generate Chart
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

# Tool 4: Generate Flowchart
def generate_flowchart(diagram_type="er"):
    er_diagram = (
        "erDiagram\n"
        "    CUSTOMERS ||--o{ ORDERS : places\n"
        "    PRODUCTS ||--o{ ORDERS : contains\n"
        "    ORDERS {\n"
        "        int id\n"
        "        int customer_id\n"
        "        int product_id\n"
        "        int quantity\n"
        "        float revenue\n"
        "    }\n"
        "    CUSTOMERS {\n"
        "        int id\n"
        "        string name\n"
        "        string email\n"
        "        string city\n"
        "    }\n"
        "    PRODUCTS {\n"
        "        int id\n"
        "        string name\n"
        "        string category\n"
        "        float price\n"
        "    }"
    )

    process_diagram = (
        "flowchart TD\n"
        "    A[User Question] --> B[LLM understands it]\n"
        "    B --> C[Generate SQL Query]\n"
        "    C --> D[Run on Database]\n"
        "    D --> E[Get Results]\n"
        "    E --> F[Generate Chart]\n"
        "    F --> G[Show Answer to User]"
    )

    if diagram_type == "er":
        return er_diagram
    else:
        return process_diagram

# Tool 5: Explain Data
def explain_data(df):
    if isinstance(df, pd.DataFrame) and not df.empty:
        summary = f"Found {len(df)} records with {len(df.columns)} columns.\n"
        for col in df.select_dtypes(include='number').columns:
            summary += f"{col}: min={df[col].min()}, max={df[col].max()}, avg={df[col].mean():.2f}\n"
        return summary
    return "No data found."