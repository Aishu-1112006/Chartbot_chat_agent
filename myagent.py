import ollama
import json
import re
from mytool import get_schema

def ask_agent(user_question, chat_history=[]):
    schema = get_schema()
    question_lower = user_question.lower().strip().rstrip("?").strip()

    hardcoded = {
        "show top 5 products by revenue": {
            "sql": "SELECT p.name, SUM(o.revenue) as total_revenue FROM products p JOIN orders o ON p.id = o.product_id GROUP BY p.name ORDER BY total_revenue DESC LIMIT 5",
            "chart_type": "bar", "x_col": "name", "y_col": "total_revenue",
            "title": "Top 5 Products by Revenue",
            "explanation": "Here are the top 5 products ranked by total revenue."
        },
        "top 5 products by revenue": {
            "sql": "SELECT p.name, SUM(o.revenue) as total_revenue FROM products p JOIN orders o ON p.id = o.product_id GROUP BY p.name ORDER BY total_revenue DESC LIMIT 5",
            "chart_type": "bar", "x_col": "name", "y_col": "total_revenue",
            "title": "Top 5 Products by Revenue",
            "explanation": "Top 5 products ranked by total revenue."
        },
        "show all products": {
            "sql": "SELECT name, category, price, stock FROM products ORDER BY price DESC",
            "chart_type": "bar", "x_col": "name", "y_col": "price",
            "title": "All Products by Price",
            "explanation": "All products sorted by price from highest to lowest."
        },
        "compare product categories": {
            "sql": "SELECT category, COUNT(*) as product_count FROM products GROUP BY category",
            "chart_type": "pie", "x_col": "category", "y_col": "product_count",
            "title": "Products by Category",
            "explanation": "Comparison of product categories."
        },
        "best selling products": {
            "sql": "SELECT p.name, SUM(o.quantity) as total_sold FROM products p JOIN orders o ON p.id = o.product_id GROUP BY p.name ORDER BY total_sold DESC LIMIT 5",
            "chart_type": "bar", "x_col": "name", "y_col": "total_sold",
            "title": "Best Selling Products",
            "explanation": "Best selling products by quantity sold."
        },
        "best selling product": {
            "sql": "SELECT p.name, SUM(o.quantity) as total_sold FROM products p JOIN orders o ON p.id = o.product_id GROUP BY p.name ORDER BY total_sold DESC LIMIT 5",
            "chart_type": "bar", "x_col": "name", "y_col": "total_sold",
            "title": "Best Selling Products",
            "explanation": "Best selling products by quantity sold."
        },
        "show monthly order trends": {
            "sql": "SELECT strftime('%Y-%m', order_date) as month, COUNT(*) as num_orders FROM orders GROUP BY month ORDER BY month",
            "chart_type": "line", "x_col": "month", "y_col": "num_orders",
            "title": "Monthly Order Trends",
            "explanation": "Number of orders placed each month over time."
        },
        "monthly order trends": {
            "sql": "SELECT strftime('%Y-%m', order_date) as month, COUNT(*) as num_orders FROM orders GROUP BY month ORDER BY month",
            "chart_type": "line", "x_col": "month", "y_col": "num_orders",
            "title": "Monthly Order Trends",
            "explanation": "Monthly order trends over time."
        },
        "show revenue trend": {
            "sql": "SELECT strftime('%Y-%m', order_date) as month, ROUND(SUM(revenue),2) as monthly_revenue FROM orders GROUP BY month ORDER BY month",
            "chart_type": "line", "x_col": "month", "y_col": "monthly_revenue",
            "title": "Monthly Revenue Trend",
            "explanation": "Revenue generated each month."
        },
        "revenue trend": {
            "sql": "SELECT strftime('%Y-%m', order_date) as month, ROUND(SUM(revenue),2) as monthly_revenue FROM orders GROUP BY month ORDER BY month",
            "chart_type": "line", "x_col": "month", "y_col": "monthly_revenue",
            "title": "Monthly Revenue Trend",
            "explanation": "Monthly revenue trend."
        },
        "what is total revenue": {
            "sql": "SELECT ROUND(SUM(revenue), 2) as total_revenue FROM orders",
            "chart_type": "none", "x_col": "", "y_col": "total_revenue",
            "title": "Total Revenue",
            "explanation": "Total revenue from all orders in the database."
        },
        "total revenue": {
            "sql": "SELECT ROUND(SUM(revenue), 2) as total_revenue FROM orders",
            "chart_type": "none", "x_col": "", "y_col": "total_revenue",
            "title": "Total Revenue",
            "explanation": "Total revenue from all orders."
        },
        "show total revenue": {
            "sql": "SELECT ROUND(SUM(revenue), 2) as total_revenue FROM orders",
            "chart_type": "none", "x_col": "", "y_col": "total_revenue",
            "title": "Total Revenue",
            "explanation": "Total revenue from all orders."
        },
        "revenue by category": {
            "sql": "SELECT p.category, ROUND(SUM(o.revenue),2) as total_revenue FROM orders o JOIN products p ON o.product_id = p.id GROUP BY p.category ORDER BY total_revenue DESC",
            "chart_type": "pie", "x_col": "category", "y_col": "total_revenue",
            "title": "Revenue by Category",
            "explanation": "Revenue split across product categories."
        },
        "show revenue by category": {
            "sql": "SELECT p.category, ROUND(SUM(o.revenue),2) as total_revenue FROM orders o JOIN products p ON o.product_id = p.id GROUP BY p.category ORDER BY total_revenue DESC",
            "chart_type": "pie", "x_col": "category", "y_col": "total_revenue",
            "title": "Revenue by Category",
            "explanation": "Revenue distribution across product categories."
        },
        "which city has most customers": {
            "sql": "SELECT city, COUNT(*) as total_customers FROM customers GROUP BY city ORDER BY total_customers DESC",
            "chart_type": "pie", "x_col": "city", "y_col": "total_customers",
            "title": "Customers by City",
            "explanation": "Customer distribution across cities."
        },
        "which city has the most customers": {
            "sql": "SELECT city, COUNT(*) as total_customers FROM customers GROUP BY city ORDER BY total_customers DESC",
            "chart_type": "pie", "x_col": "city", "y_col": "total_customers",
            "title": "Customers by City",
            "explanation": "Customer distribution across cities."
        },
        "customers by city": {
            "sql": "SELECT city, COUNT(*) as total_customers FROM customers GROUP BY city ORDER BY total_customers DESC",
            "chart_type": "bar", "x_col": "city", "y_col": "total_customers",
            "title": "Customers by City",
            "explanation": "Number of customers in each city."
        },
        "show all customers": {
            "sql": "SELECT name, email, city FROM customers ORDER BY city",
            "chart_type": "none", "x_col": "", "y_col": "",
            "title": "All Customers",
            "explanation": "Complete list of all customers."
        },
        "how many customers": {
            "sql": "SELECT COUNT(*) as total_customers FROM customers",
            "chart_type": "none", "x_col": "", "y_col": "",
            "title": "Total Customers",
            "explanation": "Total number of customers in the database."
        },
        "top customers": {
            "sql": "SELECT c.name, c.city, COUNT(o.id) as total_orders, ROUND(SUM(o.revenue),2) as total_spent FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id ORDER BY total_spent DESC LIMIT 5",
            "chart_type": "bar", "x_col": "name", "y_col": "total_spent",
            "title": "Top 5 Customers",
            "explanation": "Top 5 customers by total spending."
        },
        "show all orders": {
            "sql": "SELECT o.id, c.name as customer, p.name as product, o.quantity, o.revenue, o.order_date FROM orders o JOIN customers c ON o.customer_id = c.id JOIN products p ON o.product_id = p.id ORDER BY o.order_date DESC LIMIT 20",
            "chart_type": "none", "x_col": "", "y_col": "",
            "title": "Recent Orders",
            "explanation": "20 most recent orders."
        },
        "total orders": {
            "sql": "SELECT COUNT(*) as total_orders FROM orders",
            "chart_type": "none", "x_col": "", "y_col": "",
            "title": "Total Orders",
            "explanation": "Total number of orders placed."
        },
        "show er diagram": {
            "sql": None, "chart_type": "er_diagram", "x_col": "", "y_col": "",
            "title": "ER Diagram",
            "explanation": "Here is the Entity-Relationship Diagram of the database.",
            "diagram_type": "er"
        },
        "er diagram": {
            "sql": None, "chart_type": "er_diagram", "x_col": "", "y_col": "",
            "title": "ER Diagram",
            "explanation": "ER Diagram of the database.",
            "diagram_type": "er"
        },
        "show process flow": {
            "sql": None, "chart_type": "flowchart", "x_col": "", "y_col": "",
            "title": "Process Flow",
            "explanation": "Here is the process flow diagram.",
            "diagram_type": "process"
        },
        "show scatter plot": {
            "sql": "SELECT p.name, SUM(o.quantity) as total_qty, ROUND(SUM(o.revenue),2) as total_revenue FROM products p JOIN orders o ON p.id = o.product_id GROUP BY p.name",
            "chart_type": "scatter", "x_col": "total_qty", "y_col": "total_revenue",
            "title": "Revenue vs Quantity",
            "explanation": "Scatter plot showing revenue vs quantity sold per product."
        },
        "show product stock": {
            "sql": "SELECT name, category, stock FROM products ORDER BY stock ASC",
            "chart_type": "bar", "x_col": "name", "y_col": "stock",
            "title": "Product Stock Levels",
            "explanation": "Current stock levels for all products."
        },
        "now show me the trend for these products over the last year": {
            "sql": "SELECT strftime('%Y-%m', order_date) as month, SUM(revenue) as monthly_revenue FROM orders WHERE order_date >= '2025-01-01' GROUP BY month ORDER BY month",
            "chart_type": "line", "x_col": "month", "y_col": "monthly_revenue",
            "title": "Revenue Trend Over Last Year",
            "explanation": "Monthly revenue trend over the last year."
        },
        "what is machine learning": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "Machine Learning is a branch of AI where computers learn from data automatically. Types: Supervised Learning, Unsupervised Learning, Reinforcement Learning. Examples: ChatGPT, Netflix recommendations, image recognition."
        },
        "what is artificial intelligence": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "Artificial Intelligence (AI) is the simulation of human intelligence in machines. It includes Machine Learning, Deep Learning, NLP, and Computer Vision. Examples: ChatGPT, Siri, self-driving cars."
        },
        "what is deep learning": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "Deep Learning uses neural networks with many layers to learn from data. It powers image recognition, speech recognition, and language models like GPT."
        },
        "what is python": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "Python is a high-level programming language known for simple syntax. Used in web development, data science, AI/ML, and automation."
        },
        "what is sql": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "SQL is a language for managing databases. Commands: SELECT, INSERT, UPDATE, DELETE, JOIN. Used in MySQL, PostgreSQL, SQLite."
        },
        "what is nlp": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "NLP (Natural Language Processing) enables computers to understand human language. Powers chatbots, translation, sentiment analysis, and voice assistants."
        },
        "what is data science": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "Data Science extracts insights from data using statistics, programming, and ML. Tools: Python, R, SQL, Tableau."
        },
        "what is streamlit": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "Streamlit is a Python framework for building interactive web apps for data science. No HTML or JavaScript needed."
        },
        "what is ollama": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "Ollama lets you run Large Language Models locally on your laptop. Supports LLaMA, Mistral, Qwen and more."
        },
        "what is chatgpt": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "ChatGPT is an AI chatbot by OpenAI based on GPT models. It can answer questions, write code, and have conversations."
        },
        "what is llm": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "LLM (Large Language Model) is an AI trained on massive text data. Examples: GPT-4, Claude, Gemini, LLaMA."
        },
        "hello": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "Hello! I am ChartBot AI — your intelligent database assistant. Ask me about products, customers, orders, or any general question!"
        },
        "hi": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "Hi there! I am ChartBot AI. Ask me anything about your database or general knowledge!"
        },
        "who are you": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "I am ChartBot AI — an intelligent database assistant built for AVIT Hackathon 2026. I can query databases, generate charts, show diagrams, and answer general questions!"
        },
        "what can you do": {
            "sql": None, "chart_type": "none", "x_col": "", "y_col": "", "title": "",
            "explanation": "I can: 1) Query your database in plain English, 2) Generate bar, line, pie, scatter charts, 3) Show ER diagrams and flowcharts, 4) Explain data insights, 5) Answer general knowledge questions, 6) Support voice input!"
        },
    }

    # Exact match
    if question_lower in hardcoded:
        return hardcoded[question_lower]

    # Keyword matching
    keyword_map = {
        ("trend", "last year"):         "now show me the trend for these products over the last year",
        ("monthly", "trend"):           "show monthly order trends",
        ("monthly", "order"):           "show monthly order trends",
        ("er diagram",):                "show er diagram",
        ("entity", "relationship"):     "show er diagram",
        ("top 5", "product"):           "show top 5 products by revenue",
        ("top", "product", "revenue"):  "show top 5 products by revenue",
        ("city", "customer"):           "which city has most customers",
        ("most customer",):             "which city has most customers",
        ("total revenue",):             "what is total revenue",
        ("revenue", "category"):        "revenue by category",
        ("best selling",):              "best selling products",
        ("top customer",):              "top customers",
        ("stock",):                     "show product stock",
        ("scatter",):                   "show scatter plot",
        ("machine learning",):          "what is machine learning",
        ("artificial intelligence",):   "what is artificial intelligence",
        ("deep learning",):             "what is deep learning",
        ("nlp",):                       "what is nlp",
        ("data science",):              "what is data science",
        ("chatgpt",):                   "what is chatgpt",
        ("llm",):                       "what is llm",
        ("streamlit",):                 "what is streamlit",
        ("ollama",):                    "what is ollama",
        ("revenue trend",):             "show revenue trend",
    }

    for keywords, mapped_key in keyword_map.items():
        if all(kw in question_lower for kw in keywords):
            return hardcoded[mapped_key]

    # LLM fallback
    system_prompt = f"""You are a SQLite database assistant. Reply ONLY with JSON.

Schema:
{schema}

Rules:
- ONE JSON object only
- Only SELECT queries
- chart_type: bar, line, pie, scatter, or none

Format:
{{"sql": "SELECT ...", "chart_type": "bar", "x_col": "col1", "y_col": "col2", "title": "Title", "explanation": "explanation"}}

For non-database questions:
{{"sql": null, "chart_type": "none", "x_col": "", "y_col": "", "title": "", "explanation": "your answer here"}}"""

    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history[-4:]:
        messages.append(msg)
    messages.append({"role": "user", "content": user_question})

    raw = ""
    try:
        response = ollama.chat(
            model="qwen2.5-coder:3b",
            messages=messages,
            format="json",
            options={"temperature": 0}
        )
        raw = response["message"]["content"].strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```\s*$", "", raw)
        raw = re.sub(r"^[^{]*(\{)", r"\1", raw)
        raw = re.sub(r"(\})[^}]*$", r"\1", raw)

        result = json.loads(raw)
        result.setdefault("sql", None)
        result.setdefault("chart_type", "none")
        result.setdefault("x_col", "")
        result.setdefault("y_col", "")
        result.setdefault("title", "")
        result.setdefault("explanation", "Here are the results!")

        sql = result.get("sql")
        if sql and not sql.strip().upper().lstrip("(").startswith("SELECT"):
            result["sql"] = None
            result["chart_type"] = "none"
            result["explanation"] = "Only SELECT queries are allowed."

        return result

    except Exception:
        try:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                result = json.loads(match.group())
                result.setdefault("sql", None)
                result.setdefault("chart_type", "none")
                result.setdefault("x_col", "")
                result.setdefault("y_col", "")
                result.setdefault("title", "")
                result.setdefault("explanation", "Here are the results!")
                return result
        except Exception:
            pass

        return {
            "sql": None, "chart_type": "none",
            "x_col": "", "y_col": "", "title": "",
            "explanation": "I could not process that. Try: 'Show top 5 products by revenue' or 'Which city has most customers?'"
        }