import ollama
import json
from mytool import get_schema

def ask_agent(user_question, chat_history=[]):
    schema = get_schema()
    
    system_prompt = f"""You are an expert data analyst AI assistant.
You are connected to a SQLite database with this schema:
{schema}

STRICT SQLITE RULES - Always follow these:
- Use strftime('%Y-%m', order_date) for date formatting
- NEVER use DATE_FORMAT, it does not exist in SQLite
- NEVER use backticks, use regular quotes or nothing
- Use COUNT(*), SUM(), AVG(), MIN(), MAX() for aggregations
- Always write complete valid SQLite queries
- For top N queries use: ORDER BY column DESC LIMIT N

RESPONSE RULES:
- Respond ONLY in valid JSON format
- No markdown, no code blocks, no extra text
- Always include all 6 fields

Expected JSON format:
{{
    "sql": "complete SELECT query here",
    "chart_type": "bar or line or pie or scatter or none",
    "x_col": "exact column name for x axis",
    "y_col": "exact column name for y axis",
    "title": "descriptive chart title",
    "explanation": "friendly plain English explanation"
}}

EXAMPLES:

User: Show top 5 products by revenue
Response:
{{
    "sql": "SELECT p.name, SUM(o.revenue) as total_revenue FROM products p JOIN orders o ON p.id = o.product_id GROUP BY p.name ORDER BY total_revenue DESC LIMIT 5",
    "chart_type": "bar",
    "x_col": "name",
    "y_col": "total_revenue",
    "title": "Top 5 Products by Revenue",
    "explanation": "This shows the top 5 products ranked by their total revenue."
}}

User: Show monthly order trends
Response:
{{
    "sql": "SELECT strftime('%Y-%m', order_date) as month, COUNT(*) as num_orders FROM orders GROUP BY month ORDER BY month",
    "chart_type": "line",
    "x_col": "month",
    "y_col": "num_orders",
    "title": "Monthly Order Trends",
    "explanation": "This shows how many orders were placed each month over time."
}}

User: Which city has most customers
Response:
{{
    "sql": "SELECT city, COUNT(*) as total_customers FROM customers GROUP BY city ORDER BY total_customers DESC",
    "chart_type": "pie",
    "x_col": "city",
    "y_col": "total_customers",
    "title": "Customers by City",
    "explanation": "This shows the distribution of customers across different cities."
}}

User: What is total revenue
Response:
{{
    "sql": "SELECT SUM(revenue) as total_revenue FROM orders",
    "chart_type": "none",
    "x_col": "none",
    "y_col": "total_revenue",
    "title": "Total Revenue",
    "explanation": "The total revenue from all orders combined."
}}"""

    messages = [{'role': 'system', 'content': system_prompt}]
    for msg in chat_history[-6:]:
        messages.append(msg)
    messages.append({'role': 'user', 'content': user_question})
    
    try:
        response = ollama.chat(model='qwen2.5:3b', messages=messages)
        raw_response = response['message']['content'].strip()
        
        clean = raw_response.replace('```json', '').replace('```', '').strip()
        start = clean.find('{')
        end = clean.rfind('}') + 1
        
        return json.loads(clean[start:end])
    except Exception as e:
        return {
            'sql': None,
            'chart_type': 'none',
            'explanation': f"Sorry I could not understand that question. Please try again. Error: {str(e)}"
        }