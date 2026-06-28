🔮 ChartBot AI — Intelligent Database Chat Agent

Built for AVIT Student Hackathon 2026 | Team Project

An AI-powered conversational database assistant that allows users to query databases using plain English and get instant charts, insights, and diagrams!

📸 Features

💬 Natural Language to SQL — Ask questions in plain English, get SQL queries automatically
📊 Smart Charts — Auto-generated Bar, Line, Pie, and Scatter charts using Plotly
🗺️ ER Diagrams — Entity-Relationship diagrams using Mermaid.js
🔄 Process Flow Diagrams — Order flow visualization
🎤 Voice Input — Speech-to-text query support (Chrome/Edge)
🌙 Dark / Light Mode — Toggle between themes
⚙️ Settings Panel — Edit username, clear chat, logout
🤖 General AI Q&A — Ask anything about AI, ML, Python, SQL and more
🔒 Login System — Name and email based login

🛠️ Tech Stack

ComponentTechnologyFrontendStreamlitLLM ProviderOllama (qwen2.5-coder:3b)DatabaseSQLiteChartsPlotly ExpressDiagramsMermaid.jsLanguagePython 3.11+

📁 Project Structure

db_chat_agent/
├── main.py # Main Streamlit UI application
├── myagent.py # LLM Agent - processes questions
├── mytool.py # Tools - SQL execution, charts, diagrams
├── database.py # SQLite database setup with sample data
├── requirements.txt # Python dependencies
├── .env.example # Environment variables template
└── README.md # Project documentation

🗄️ Database Schema

The project uses a sample E-commerce SQLite database with 3 tables:

products — id, name, category, price, stock
customers — id, name, email, city
orders — id, product_id, customer_id, quantity, revenue, order_date

⚙️ Agent Tools

ToolPurposeOutputget_schemaRetrieve database schemaJSON schemaexecute_queryExecute SQL queriesDataFramegenerate_chartCreate visualizationsPlotly chartgenerate_flowchartCreate ER/flow diagramsMermaid diagramexplain_dataGenerate data insightsNatural language

🚀 How to Run Locally

Step 1: Clone the repository

bashgit clone https://github.com/Aishu-1112006/chartbot-ai.git
cd chartbot-ai

Step 2: Install dependencies

bashpip install -r requirements.txt

Step 3: Install and start Ollama

bash# Download Ollama from https://ollama.com
ollama pull qwen2.5-coder:3b
ollama serve

Step 4: Create database

bashpython database.py

Step 5: Run the app

bashstreamlit run main.py

Step 6: Open in browser

http://localhost:8501

💡 Sample Questions to Ask

Database Queries

Show top 5 products by revenue
Which city has most customers?
Show monthly order trends
What is total revenue?
Best selling products
Revenue by category
Show all orders
Compare product categories

Visualizations

Show ER diagram
Create flowchart for order flow
Show scatter plot
Revenue trend over last year

General Knowledge

What is machine learning?
What is artificial intelligence?
What is deep learning?
What is Python?
What is SQL?
