import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from myagent import ask_agent
from mytool import execute_query, generate_chart, generate_flowchart, explain_data

# Page config
st.set_page_config(
    page_title="DB Chat Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Intelligent Database Chat Agent")
st.caption("Ask anything about your data in plain English!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.header("⚡ Quick Actions")

    if st.button("🔗 Show ER Diagram"):
        diagram = generate_flowchart("er")
        st.session_state.messages.append({
            "role": "assistant",
            "type": "diagram",
            "content": diagram,
            "explanation": "Here is the ER Diagram of the database:"
        })
        st.rerun()

    if st.button("🔄 Show Process Flow"):
        diagram = generate_flowchart("process")
        st.session_state.messages.append({
            "role": "assistant",
            "type": "diagram",
            "content": diagram,
            "explanation": "Here is the Process Flow Diagram:"
        })
        st.rerun()

    st.divider()
    st.markdown("**💡 Try asking:**")
    st.markdown("- Show top 5 products by revenue")
    st.markdown("- Which city has most customers?")
    st.markdown("- Show monthly order trends")
    st.markdown("- What is total revenue?")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# Display all chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message.get("explanation", ""))

            if message.get("type") == "diagram":
                mermaid_code = message["content"]
                components.html(
                    f"""
                    <div class="mermaid">{mermaid_code}</div>
                    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                    <script>mermaid.initialize({{startOnLoad: true}});</script>
                    """,
                    height=400
                )
            else:
                if message.get("sql"):
                    with st.expander("🔍 View SQL Query"):
                        st.code(message["sql"], language="sql")

                if message.get("dataframe") is not None:
                    st.dataframe(message["dataframe"], use_container_width=True)

                if message.get("chart") is not None:
                    st.plotly_chart(message["chart"], use_container_width=True)

# Chat input box
if prompt := st.chat_input("Ask about your data..."):

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            result = ask_agent(prompt, st.session_state.chat_history)

        explanation = result.get("explanation", "Here are the results!")
        sql = result.get("sql")
        chart_type = result.get("chart_type", "none")

        st.write(explanation)

        df = None
        fig = None

        if sql:
            with st.expander("🔍 View SQL Query"):
                st.code(sql, language="sql")

            df = execute_query(sql)

            if isinstance(df, pd.DataFrame) and not df.empty:
                st.dataframe(df, use_container_width=True)

                insight = explain_data(df)
                st.info(f"📊 {insight}")

                if chart_type != "none":
                    x_col = result.get("x_col", df.columns[0])
                    y_col = result.get("y_col", df.columns[-1])
                    title = result.get("title", "Chart")
                    fig = generate_chart(df, chart_type, x_col, y_col, title)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

        # Save to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": explanation
        })

        st.session_state.messages.append({
            "role": "assistant",
            "explanation": explanation,
            "sql": sql,
            "dataframe": df,
            "chart": fig
        })