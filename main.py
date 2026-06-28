import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from myagent import ask_agent
from mytool import execute_query, generate_chart, generate_flowchart, explain_data
import time

# ── Session defaults ──
for key, val in {
    "logged_in": False, "username": "", "email": "",
    "messages": [], "chat_history": [],
    "dark_mode": True, "show_settings": False, "edit_username": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

dark = st.session_state.dark_mode

# ── THEME VARIABLES ──
if dark:
    BG        = "linear-gradient(135deg,#0a0a1a 0%,#0f0f2e 40%,#0a1628 100%)"
    CARD      = "rgba(255,255,255,0.04)"
    CARD_BOR  = "rgba(139,92,246,0.25)"
    TEXT      = "#f1f5f9"
    SUBTEXT   = "rgba(167,139,250,0.7)"
    BTN_BG    = "linear-gradient(135deg,#7c3aed,#6366f1)"
    BTN_HVR   = "linear-gradient(135deg,#8b5cf6,#7c3aed)"
    INPUT_BG  = "rgba(255,255,255,0.06)"
    INPUT_BOR = "rgba(139,92,246,0.5)"
    INPUT_TXT = "#ffffff"
    SIDE_BG   = "linear-gradient(180deg,#0d0d2b,#0a0a1e)"
    ACCENT    = "#c4b5fd"
    HDR_BG    = "rgba(124,58,237,0.25)"
    HDR_BOR   = "rgba(139,92,246,0.35)"
    BADGE_BG  = "rgba(124,58,237,0.2)"
    BADGE_BOR = "rgba(139,92,246,0.4)"
    BADGE_CLR = "#c4b5fd"
    MSG_BG    = "rgba(255,255,255,0.04)"
    INFO_BG   = "rgba(99,102,241,0.12)"
    INFO_BOR  = "rgba(139,92,246,0.25)"
    PLOT_BG   = "rgba(30,27,75,0.5)"
    GRID_CLR  = "rgba(139,92,246,0.15)"
    AXIS_CLR  = "#a78bfa"
    LOGO_GRAD = "linear-gradient(135deg,#7c3aed,#6366f1,#4f46e5)"
    SET_BG    = "rgba(15,15,45,0.98)"
    SET_BOR   = "rgba(139,92,246,0.3)"
    CHAT_BG   = "rgba(255,255,255,0.05)"
    CHAT_BOR  = "rgba(139,92,246,0.4)"
    CHAT_TXT  = "#ffffff"
    CHAT_PH   = "rgba(167,139,250,0.5)"
else:
    BG        = "linear-gradient(135deg,#f0f4ff 0%,#ffffff 50%,#e8f0fe 100%)"
    CARD      = "rgba(255,255,255,0.95)"
    CARD_BOR  = "rgba(21,101,192,0.15)"
    TEXT      = "#1e293b"
    SUBTEXT   = "#64748b"
    BTN_BG    = "linear-gradient(135deg,#1565C0,#42A5F5)"
    BTN_HVR   = "linear-gradient(135deg,#1976D2,#1565C0)"
    INPUT_BG  = "#ffffff"
    INPUT_BOR = "rgba(21,101,192,0.4)"
    INPUT_TXT = "#1e293b"
    SIDE_BG   = "linear-gradient(180deg,#1565C0,#1976D2)"
    ACCENT    = "#1565C0"
    HDR_BG    = "linear-gradient(135deg,#1565C0,#42A5F5)"
    HDR_BOR   = "rgba(21,101,192,0.2)"
    BADGE_BG  = "rgba(21,101,192,0.1)"
    BADGE_BOR = "rgba(21,101,192,0.3)"
    BADGE_CLR = "#1565C0"
    MSG_BG    = "rgba(255,255,255,0.9)"
    INFO_BG   = "rgba(21,101,192,0.08)"
    INFO_BOR  = "rgba(21,101,192,0.2)"
    PLOT_BG   = "rgba(240,244,255,0.8)"
    GRID_CLR  = "rgba(21,101,192,0.1)"
    AXIS_CLR  = "#1565C0"
    LOGO_GRAD = "linear-gradient(135deg,#1565C0,#42A5F5)"
    SET_BG    = "rgba(240,244,255,0.98)"
    SET_BOR   = "rgba(21,101,192,0.2)"
    CHAT_BG   = "#ffffff"
    CHAT_BOR  = "rgba(21,101,192,0.4)"
    CHAT_TXT  = "#1e293b"
    CHAT_PH   = "#94a3b8"

st.set_page_config(page_title="ChartBot AI", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
*,*::before,*::after{{font-family:'Plus Jakarta Sans',sans-serif!important;box-sizing:border-box;}}
#MainMenu,footer,header{{visibility:hidden;}}
.stApp{{background:{BG}!important;min-height:100vh;}}

/* ── INPUTS ── */
.stTextInput>div>div>input{{
    background:{INPUT_BG}!important;
    border:1.5px solid {INPUT_BOR}!important;
    border-radius:14px!important;
    color:{INPUT_TXT}!important;
    font-size:15px!important;font-weight:500!important;
    padding:14px 18px!important;transition:all 0.3s!important;
}}
.stTextInput>div>div>input:focus{{
    border-color:{ACCENT}!important;
    box-shadow:0 0 0 3px {BADGE_BG}!important;
    background:{INPUT_BG}!important;
}}
.stTextInput>div>div>input::placeholder{{color:{CHAT_PH}!important;}}
.stTextInput label{{color:{ACCENT}!important;font-size:11px!important;font-weight:700!important;
    text-transform:uppercase!important;letter-spacing:1.5px!important;}}

/* ── BUTTONS ── */
.stButton>button{{
    background:{BTN_BG}!important;color:white!important;border:none!important;
    border-radius:12px!important;font-size:14px!important;font-weight:700!important;
    padding:12px 20px!important;width:100%!important;transition:all 0.3s!important;
    box-shadow:0 4px 16px rgba(0,0,0,0.15)!important;
}}
.stButton>button:hover{{background:{BTN_HVR}!important;transform:translateY(-2px)!important;box-shadow:0 8px 24px rgba(0,0,0,0.2)!important;}}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"]{{background:{SIDE_BG}!important;border-right:1px solid {CARD_BOR}!important;}}
section[data-testid="stSidebar"] *{{color:white!important;}}
section[data-testid="stSidebar"] .stButton>button{{
    background:rgba(255,255,255,0.12)!important;border:1px solid rgba(255,255,255,0.2)!important;
    color:white!important;font-size:13px!important;padding:10px 14px!important;
    border-radius:10px!important;box-shadow:none!important;
}}
section[data-testid="stSidebar"] .stButton>button:hover{{background:rgba(255,255,255,0.22)!important;transform:translateY(-1px)!important;}}
section[data-testid="stSidebar"] hr{{border-color:rgba(255,255,255,0.15)!important;}}

/* ── CHAT MESSAGES ── */
.stChatMessage{{
    background:{MSG_BG}!important;border:1px solid {CARD_BOR}!important;
    border-radius:18px!important;margin-bottom:12px!important;backdrop-filter:blur(10px)!important;
}}

/* ── CHAT INPUT BOX ── */
.stChatInput{{background:transparent!important;padding:0!important;}}
.stChatInput>div{{
    background:{CHAT_BG}!important;
    border:2px solid {CHAT_BOR}!important;
    border-radius:18px!important;
    backdrop-filter:blur(20px)!important;
    box-shadow:0 4px 24px rgba(0,0,0,0.15)!important;
}}
.stChatInput textarea{{
    background:{CHAT_BG}!important;
    border:none!important;
    color:{CHAT_TXT}!important;
    font-size:15px!important;
    font-weight:500!important;
    min-height:60px!important;
    caret-color:{ACCENT}!important;
}}
.stChatInput textarea:focus{{
    outline:none!important;
    border:none!important;
    box-shadow:none!important;
    background:{CHAT_BG}!important;
    color:{CHAT_TXT}!important;
}}
.stChatInput textarea::placeholder{{
    color:{CHAT_PH}!important;
    font-size:14px!important;
    font-weight:400!important;
}}
/* Remove black bar / bottom border */
.stChatInput button{{
    background:{BTN_BG}!important;
    border-radius:12px!important;
    border:none!important;
}}
div[data-testid="stBottom"]{{
    background:transparent!important;
    border:none!important;
    box-shadow:none!important;
    padding:0!important;
}}
div[data-testid="stBottom"] > div{{
    background:transparent!important;
    border:none!important;
    box-shadow:none!important;
}}
.stChatFloatingInputContainer{{
    background:transparent!important;
    border:none!important;
    box-shadow:none!important;
    padding-bottom:8px!important;
}}
/* full bottom area match theme */
[data-testid="stAppViewBlockContainer"]{{
    padding-bottom:80px!important;
}}

/* ── EXPANDER ── */
.streamlit-expanderHeader{{
    background:{INFO_BG}!important;border:1px solid {INFO_BOR}!important;
    border-radius:10px!important;color:{ACCENT}!important;font-weight:600!important;
}}

/* ── INFO / DATA ── */
.stInfo{{background:{INFO_BG}!important;border:1px solid {INFO_BOR}!important;border-radius:10px!important;color:{TEXT}!important;}}
.stDataFrame{{border:1px solid {CARD_BOR}!important;border-radius:12px!important;overflow:hidden!important;}}
.stError,.stSuccess,.stWarning{{border-radius:10px!important;}}

/* Fix expander arrow overlap */
.streamlit-expanderHeader{{
    display:flex!important;align-items:center!important;gap:8px!important;
    padding:12px 16px!important;
}}
.streamlit-expanderHeader p{{
    font-size:13px!important;font-weight:600!important;
    margin:0!important;white-space:nowrap!important;
    overflow:hidden!important;text-overflow:ellipsis!important;
}}
details summary svg{{flex-shrink:0!important;}}
</style>
""", unsafe_allow_html=True)


def render_mermaid(code, height=380):
    theme = "dark" if dark else "default"
    pc = '#7c3aed' if dark else '#1565C0'
    tc = '#e2e8f0' if dark else '#1e293b'
    lc = '#a78bfa' if dark else '#42A5F5'
    bg = 'transparent' if dark else '#f0f4ff'
    components.html(f"""<!DOCTYPE html><html><head>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
    *{{margin:0;padding:0;box-sizing:border-box;}}
    body{{background:{bg};overflow:hidden;padding:4px;}}
    .mermaid{{width:100%;text-align:center;}}
    .mermaid svg{{
        max-width:100%!important;
        width:100%!important;
        height:auto!important;
        max-height:360px!important;
    }}
    </style></head><body>
    <div class="mermaid">{code}</div>
    <script>
    mermaid.initialize({{
        startOnLoad:true,theme:'{theme}',
        flowchart:{{useMaxWidth:true,htmlLabels:true,curve:'basis',nodeSpacing:20,rankSpacing:30}},
        er:{{useMaxWidth:true,diagramPadding:5,entityPadding:5,fontSize:11}},
        themeVariables:{{primaryColor:'{pc}',primaryTextColor:'{tc}',lineColor:'{lc}',fontSize:'11px'}}
    }});
    setTimeout(()=>{{
        const s=document.querySelector('.mermaid svg');
        if(s){{
            s.removeAttribute('height');
            s.setAttribute('width','100%');
            s.style.maxHeight='360px';
            s.style.width='100%';
            s.style.height='auto';
        }}
    }},400);
    </script></body></html>""", height=height)

def process_render(result, key_suffix=""):
    explanation = result.get("explanation", "Here are the results!")
    sql         = result.get("sql")
    chart_type  = result.get("chart_type", "none")
    df = None; fig = None

    if explanation:
        st.markdown(f"<p style='color:{TEXT};font-size:15px;line-height:1.8;margin:0 0 12px 0;'>{explanation}</p>", unsafe_allow_html=True)

    if chart_type == "er_diagram":
        render_mermaid(generate_flowchart("er"))
    elif chart_type == "flowchart":
        render_mermaid(generate_flowchart("process"))
    elif sql:
        with st.expander("View SQL Query"):
            st.code(sql, language="sql")
        df = execute_query(sql)
        if isinstance(df, pd.DataFrame) and not df.empty:
            st.dataframe(df, use_container_width=True)
            insight = explain_data(df)
            if insight:
                st.info(f"📊 {insight}")
            if chart_type not in ["none", "er_diagram", "flowchart"]:
                x_col = result.get("x_col", "")
                y_col = result.get("y_col", "")
                if x_col not in df.columns: x_col = df.columns[0]
                if y_col not in df.columns: y_col = df.columns[-1] if len(df.columns) > 1 else df.columns[0]
                fig = generate_chart(df, chart_type, x_col, y_col, result.get("title", "Chart"))
                if fig:
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=PLOT_BG,
                        font=dict(color=TEXT, family='Plus Jakarta Sans'),
                        title=dict(font=dict(color=TEXT, size=16)),
                        xaxis=dict(gridcolor=GRID_CLR, color=AXIS_CLR),
                        yaxis=dict(gridcolor=GRID_CLR, color=AXIS_CLR),
                    )
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_{key_suffix}_{int(time.time()*1000)}")
        elif df is not None:
            st.warning("Query returned no results.")
    return df, fig


# ══════════════════════════════
# 🏠 LOGIN PAGE
# ══════════════════════════════
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Logo — clean chart icon, no emoji issues
        st.markdown(f"""
        <div style='text-align:center;margin-bottom:28px;'>
            <div style='
                width:96px;height:96px;
                background:{LOGO_GRAD};
                border-radius:28px;
                display:inline-flex;align-items:center;justify-content:center;
                font-size:48px;
                box-shadow:0 12px 48px rgba(99,102,241,0.4),0 0 0 1px rgba(255,255,255,0.08);
            '>📊</div>
            <div style='margin-top:8px;font-size:11px;color:{SUBTEXT};font-weight:700;letter-spacing:3px;text-transform:uppercase;'>
                AI Powered
            </div>
            <h1 style='
                font-size:48px;font-weight:800;margin:10px 0 6px 0;
                background:{LOGO_GRAD};
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                letter-spacing:-2px;line-height:1;
            '>ChartBot AI</h1>
            <p style='color:{SUBTEXT};font-size:16px;margin:0;font-weight:400;'>
                Your intelligent database chat assistant
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Feature badges
        badges = ['📊 Smart Charts', '🗄️ SQL Queries', '🎤 Voice Input', '📈 ER Diagrams', '🤖 AI Powered']
        st.markdown(f"""
        <div style='text-align:center;margin-bottom:28px;display:flex;flex-wrap:wrap;gap:8px;justify-content:center;'>
            {''.join([f"<span style='background:{BADGE_BG};border:1px solid {BADGE_BOR};color:{BADGE_CLR};border-radius:30px;padding:6px 14px;font-size:12px;font-weight:600;'>{b}</span>" for b in badges])}
        </div>
        """, unsafe_allow_html=True)

        # Login card
        st.markdown(f"""
        <div style='
            background:{CARD};border:1px solid {CARD_BOR};
            border-radius:28px;padding:32px 28px 8px 28px;
            backdrop-filter:blur(20px);
            box-shadow:0 24px 80px rgba(0,0,0,0.12);
        '>
            <h3 style='color:{TEXT};font-size:22px;font-weight:800;margin:0 0 6px 0;'>👋 Welcome!</h3>
            <p style='color:{SUBTEXT};font-size:13px;margin:0 0 8px 0;'>
                Enter your details to start chatting with your data
            </p>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("👤 YOUR NAME", placeholder="e.g. Gokul", key="inp_user")
        email    = st.text_input("📧 EMAIL ADDRESS", placeholder="e.g. gokul@email.com", key="inp_email")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Launch ChartBot AI →", use_container_width=True):
            if not username.strip():
                st.error("⚠️ Please enter your name!")
            elif not email.strip() or "@" not in email:
                st.error("⚠️ Please enter a valid email!")
            else:
                st.session_state.logged_in = True
                st.session_state.username  = username.strip()
                st.session_state.email     = email.strip()
                st.rerun()

        st.markdown(f"""
        <p style='text-align:center;color:{SUBTEXT};font-size:12px;margin-top:16px;margin-bottom:8px;'>
            🔒 No account needed &nbsp;•&nbsp; 100% Local AI &nbsp;•&nbsp; Data stays private
        </p>
        """, unsafe_allow_html=True)


# ══════════════════════════════
# 💬 CHAT PAGE
# ══════════════════════════════
else:
    username = st.session_state.username

    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center;padding:20px 0 14px 0;'>
            <div style='
                width:64px;height:64px;background:{LOGO_GRAD};
                border-radius:20px;display:inline-flex;align-items:center;
                justify-content:center;font-size:32px;margin-bottom:10px;
                box-shadow:0 6px 24px rgba(0,0,0,0.3);
            '>📊</div>
            <div style='font-size:20px;font-weight:800;color:white;letter-spacing:-0.5px;'>ChartBot AI</div>
            <div style='color:rgba(255,255,255,0.45);font-size:11px;margin-top:3px;'>Intelligent Data Assistant</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        # User card
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.18);
        border-radius:14px;padding:14px 16px;margin-bottom:14px;'>
            <div style='color:white;font-weight:700;font-size:15px;'>👤 {st.session_state.username}</div>
            <div style='color:rgba(255,255,255,0.55);font-size:11px;margin-top:4px;'>📧 {st.session_state.email}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.show_settings = not st.session_state.show_settings
            st.rerun()

        st.markdown("---")
        st.markdown("<div style='color:rgba(255,255,255,0.45);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;'>⚡ Quick Actions</div>", unsafe_allow_html=True)

        if st.button("🔗 ER Diagram", use_container_width=True):
            st.session_state.messages.append({
                "role": "assistant", "chart_type": "er_diagram",
                "explanation": "Here is the Entity-Relationship Diagram of your database!",
                "sql": None, "dataframe": None, "chart": None
            })
            st.rerun()

        if st.button("🔄 Process Flow", use_container_width=True):
            st.session_state.messages.append({
                "role": "assistant", "chart_type": "flowchart",
                "explanation": "Here is the Order Process Flow Diagram!",
                "sql": None, "dataframe": None, "chart": None
            })
            st.rerun()

        st.markdown("---")
        st.markdown("<div style='color:rgba(255,255,255,0.45);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;'>💡 Try Asking</div>", unsafe_allow_html=True)
        for q in [
            "Show top 5 products by revenue",
            "Which city has most customers?",
            "Show monthly order trends",
            "What is total revenue?",
            "Best selling products",
            "Revenue by category",
            "Show ER diagram",
            "What is machine learning?",
        ]:
            st.markdown(f"<div style='color:rgba(255,255,255,0.7);font-size:12px;padding:4px 0 4px 10px;border-left:2px solid rgba(255,255,255,0.25);margin-bottom:5px;'>• {q}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<div style='color:rgba(255,255,255,0.45);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;'>🎤 Voice Input</div>", unsafe_allow_html=True)

        # ── VOICE (Browser Web Speech API) ──
        components.html(f"""
        <!DOCTYPE html><html><head>
        <style>
        *{{margin:0;padding:0;box-sizing:border-box;font-family:'Plus Jakarta Sans',sans-serif;}}
        body{{background:transparent;padding:4px;}}
        #micBtn{{
            width:100%;padding:13px 16px;
            background:rgba(255,255,255,0.12);
            border:1px solid rgba(255,255,255,0.25);
            border-radius:12px;color:white;font-size:13px;font-weight:700;
            cursor:pointer;transition:all 0.3s;
        }}
        #micBtn:hover{{background:rgba(255,255,255,0.22);}}
        #micBtn.listening{{
            background:linear-gradient(135deg,rgba(220,38,38,0.6),rgba(239,68,68,0.5));
            border-color:rgba(239,68,68,0.7);
            animation:pulse 1s infinite;
        }}
        @keyframes pulse{{0%{{box-shadow:0 0 0 0 rgba(239,68,68,0.6);}}70%{{box-shadow:0 0 0 10px rgba(239,68,68,0);}}100%{{box-shadow:0 0 0 0 rgba(239,68,68,0);}}}}
        #status{{color:rgba(255,255,255,0.6);font-size:11px;text-align:center;margin-top:7px;min-height:16px;line-height:1.5;}}
        #resultBox{{
            background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);
            border-radius:10px;padding:8px 12px;color:white;font-size:12px;
            margin-top:7px;display:none;word-break:break-word;line-height:1.5;
        }}
        #sendBtn{{
            width:100%;padding:11px;margin-top:7px;
            background:linear-gradient(135deg,#059669,#10b981);
            border:none;border-radius:10px;color:white;
            font-size:13px;font-weight:700;cursor:pointer;display:none;transition:all 0.3s;
        }}
        #sendBtn:hover{{background:linear-gradient(135deg,#047857,#059669);transform:translateY(-1px);}}
        </style></head><body>
        <button id="micBtn" onclick="toggleVoice()">🎤 Start Speaking</button>
        <div id="status">Use Chrome or Edge browser</div>
        <div id="resultBox"></div>
        <button id="sendBtn" onclick="sendToChat()">✅ Send to Chat</button>
        <script>
        let recognition=null,isListening=false,finalText="";
        function toggleVoice(){{isListening?stopVoice():startVoice();}}
        function startVoice(){{
            const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
            if(!SR){{document.getElementById("status").textContent="❌ Use Chrome or Edge!";return;}}
            recognition=new SR();
            recognition.lang="en-US";
            recognition.continuous=false;
            recognition.interimResults=true;
            isListening=true;finalText="";
            document.getElementById("micBtn").textContent="🔴 Listening... Click to Stop";
            document.getElementById("micBtn").classList.add("listening");
            document.getElementById("status").textContent="🎤 Speak your question now...";
            document.getElementById("resultBox").style.display="none";
            document.getElementById("sendBtn").style.display="none";
            recognition.onresult=function(e){{
                let interim="";
                for(let i=e.resultIndex;i<e.results.length;i++){{
                    if(e.results[i].isFinal)finalText+=e.results[i][0].transcript;
                    else interim+=e.results[i][0].transcript;
                }}
                const display=finalText||interim;
                if(display){{
                    document.getElementById("resultBox").style.display="block";
                    document.getElementById("resultBox").textContent="🎤 "+display;
                }}
            }};
            recognition.onend=function(){{
                isListening=false;
                document.getElementById("micBtn").textContent="🎤 Start Speaking";
                document.getElementById("micBtn").classList.remove("listening");
                if(finalText.trim()){{
                    document.getElementById("status").textContent="✅ Click Send to submit";
                    document.getElementById("sendBtn").style.display="block";
                    document.getElementById("resultBox").textContent="🎤 "+finalText.trim();
                    document.getElementById("resultBox").style.display="block";
                }}else{{
                    document.getElementById("status").textContent="⚠️ No speech detected. Try again.";
                }}
            }};
            recognition.onerror=function(e){{
                isListening=false;
                document.getElementById("micBtn").textContent="🎤 Start Speaking";
                document.getElementById("micBtn").classList.remove("listening");
                const msgs={{'no-speech':'No speech detected.','audio-capture':'Mic not found!','not-allowed':'Allow mic permission!'}};
                document.getElementById("status").textContent="❌ "+(msgs[e.error]||e.error);
            }};
            try{{recognition.start();}}catch(e){{
                document.getElementById("status").textContent="❌ Mic error: "+e.message;
                isListening=false;
            }}
        }}
        function stopVoice(){{if(recognition)recognition.stop();}}
        function sendToChat(){{
            if(!finalText.trim())return;
            try{{
                const textareas=window.parent.document.querySelectorAll('textarea');
                let sent=false;
                textareas.forEach(function(ta){{
                    const ph=ta.getAttribute('placeholder')||'';
                    if(!sent&&(ph.includes('Ask')||ph.includes('anything')||ph.includes('question'))){{
                        const nativeSetter=Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype,'value').set;
                        nativeSetter.call(ta,finalText.trim());
                        ta.dispatchEvent(new Event('input',{{bubbles:true}}));
                        ta.dispatchEvent(new Event('change',{{bubbles:true}}));
                        setTimeout(function(){{
                            ta.dispatchEvent(new KeyboardEvent('keydown',{{key:'Enter',code:'Enter',keyCode:13,bubbles:true,cancelable:true}}));
                        }},200);
                        sent=true;
                        document.getElementById("status").textContent="✅ Sent!";
                        document.getElementById("sendBtn").style.display="none";
                        finalText="";
                    }}
                }});
                if(!sent){{document.getElementById("status").textContent="⚠️ Click in chat box first, then Send";}}
            }}catch(e){{document.getElementById("status").textContent="⚠️ Click chat box then Send";}}
        }}
        </script></body></html>
        """, height=200)

        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()

    # ══════════════════════════════
    # ⚙️ SETTINGS PANEL
    # ══════════════════════════════
    if st.session_state.show_settings:
        # Settings header
        st.markdown(f"""
        <div style='background:{CARD};border:1px solid {CARD_BOR};border-radius:20px;
        padding:24px 28px 20px 28px;margin-bottom:16px;
        box-shadow:0 8px 32px rgba(0,0,0,0.1);'>
            <div style='display:flex;align-items:center;justify-content:space-between;'>
                <div>
                    <h2 style='color:{TEXT};font-size:22px;font-weight:800;margin:0 0 4px 0;'>⚙️ Settings</h2>
                    <p style='color:{SUBTEXT};font-size:13px;margin:0;'>Manage your account and preferences</p>
                </div>
            </div>
            <hr style='border-color:{CARD_BOR};margin:16px 0 0 0;'>
        </div>
        """, unsafe_allow_html=True)

        # Row 1: Account + Appearance side by side
        sc1, sc2 = st.columns([1,1])

        with sc1:
            st.markdown(f"""
            <div style='background:{CARD};border:1px solid {CARD_BOR};border-radius:16px;
            padding:20px;height:100%;'>
                <div style='color:{ACCENT};font-size:10px;font-weight:700;text-transform:uppercase;
                letter-spacing:1.5px;margin-bottom:14px;'>👤 Account Details</div>
                <div style='display:flex;justify-content:space-between;align-items:center;padding:10px 0;
                border-bottom:1px solid {CARD_BOR};'>
                    <span style='color:{SUBTEXT};font-size:13px;'>Name</span>
                    <span style='color:{TEXT};font-size:14px;font-weight:700;'>{st.session_state.username}</span>
                </div>
                <div style='display:flex;justify-content:space-between;align-items:center;padding:10px 0;'>
                    <span style='color:{SUBTEXT};font-size:13px;'>Email</span>
                    <span style='color:{TEXT};font-size:13px;font-weight:500;'>{st.session_state.email}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.session_state.edit_username:
                new_name = st.text_input("New Name", value=st.session_state.username, key="new_uname")
                col_s, col_c = st.columns(2)
                with col_s:
                    if st.button("💾 Save Name", use_container_width=True):
                        if new_name.strip():
                            st.session_state.username = new_name.strip()
                            st.session_state.edit_username = False
                            st.success("✅ Name updated!")
                            st.rerun()
                with col_c:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.edit_username = False
                        st.rerun()
            else:
                if st.button("✏️ Edit Username", use_container_width=True):
                    st.session_state.edit_username = True
                    st.rerun()

        with sc2:
            st.markdown(f"""
            <div style='background:{CARD};border:1px solid {CARD_BOR};border-radius:16px;padding:20px;'>
                <div style='color:{ACCENT};font-size:10px;font-weight:700;text-transform:uppercase;
                letter-spacing:1.5px;margin-bottom:14px;'>🎨 Appearance</div>
            </div>
            """, unsafe_allow_html=True)
            cd, cl = st.columns(2)
            with cd:
                if st.button(f"🌙 Dark {'✓' if dark else ''}", use_container_width=True):
                    st.session_state.dark_mode = True
                    st.session_state.show_settings = False
                    st.rerun()
            with cl:
                if st.button(f"☀️ Light {'✓' if not dark else ''}", use_container_width=True):
                    st.session_state.dark_mode = False
                    st.session_state.show_settings = False
                    st.rerun()
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:{ACCENT};font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;'>🔧 Actions</div>", unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca:
                if st.button("🗑️ Clear Chat", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state.chat_history = []
                    st.session_state.show_settings = False
                    st.rerun()
            with cb:
                if st.button("✖️ Close", use_container_width=True):
                    st.session_state.show_settings = False
                    st.session_state.edit_username = False
                    st.rerun()
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("🚪 Logout", use_container_width=True):
                for k in ["logged_in","username","email","messages","chat_history"]:
                    st.session_state[k] = False if k=="logged_in" else "" if k in ["username","email"] else []
                st.session_state.show_settings = False
                st.rerun()

        st.markdown("---")

    # ── MAIN CHAT AREA ──
    if not st.session_state.show_settings:
        msg_count   = len([m for m in st.session_state.messages if m.get("role")=="user"])
        sql_count   = sum(1 for m in st.session_state.messages if m.get("sql"))
        chart_count = sum(1 for m in st.session_state.messages if m.get("chart") is not None)

        # Header
        hdr_txt = "white" if dark else "white"
        st.markdown(f"""
        <div style='
            background:{HDR_BG};border:1px solid {HDR_BOR};
            border-radius:20px;padding:20px 28px;margin-bottom:20px;
            backdrop-filter:blur(20px);box-shadow:0 8px 32px rgba(0,0,0,0.12);
            display:flex;align-items:center;gap:16px;
        '>
            <div style='width:52px;height:52px;background:{LOGO_GRAD};border-radius:16px;
            display:flex;align-items:center;justify-content:center;font-size:28px;flex-shrink:0;
            box-shadow:0 4px 16px rgba(0,0,0,0.2);'>📊</div>
            <div style='flex:1;'>
                <div style='font-size:22px;font-weight:800;color:{hdr_txt};'>ChartBot AI</div>
                <div style='color:rgba(255,255,255,0.75);font-size:13px;margin-top:2px;'>
                    Welcome, <b>{username}</b>! Ask anything about your data.
                </div>
            </div>
            <div style='display:flex;gap:8px;flex-shrink:0;'>
                <div style='background:rgba(34,197,94,0.2);border:1px solid rgba(34,197,94,0.35);
                border-radius:20px;padding:6px 14px;color:#4ade80;font-size:12px;font-weight:700;'>🟢 Online</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Mode toggle
        mc1, mc2, mc3 = st.columns([4, 1, 1])
        with mc3:
            mode_lbl = "☀️ Light" if dark else "🌙 Dark"
            if st.button(mode_lbl, key="mode_main"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()

        # Stats
        c1,c2,c3,c4 = st.columns(4)
        for col,icon,num,label in [
            (c1,"💬",msg_count,"Questions"),
            (c2,"🗄️",sql_count,"SQL Queries"),
            (c3,"📈",chart_count,"Charts"),
            (c4,"👤",username[:10],"Logged In"),
        ]:
            with col:
                st.markdown(f"""
                <div style='background:{CARD};border:1px solid {CARD_BOR};border-radius:16px;
                padding:16px 12px;text-align:center;backdrop-filter:blur(10px);
                box-shadow:0 4px 16px rgba(0,0,0,0.06);'>
                    <div style='font-size:22px;margin-bottom:4px;'>{icon}</div>
                    <div style='font-size:22px;font-weight:800;color:{ACCENT};'>{num}</div>
                    <div style='font-size:10px;color:{SUBTEXT};text-transform:uppercase;letter-spacing:0.8px;margin-top:2px;'>{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Welcome banner
        if not st.session_state.messages:
            badges2 = ['📊 Bar/Line/Pie/Scatter','🗺️ ER Diagrams','🔄 Flow Charts','🤖 AI Q&A','🎤 Voice Input']
            st.markdown(f"""
            <div style='background:{CARD};border:1px solid {CARD_BOR};border-radius:20px;
            padding:36px;text-align:center;backdrop-filter:blur(20px);margin-bottom:24px;
            box-shadow:0 8px 32px rgba(0,0,0,0.08);'>
                <div style='font-size:52px;margin-bottom:14px;'>👋</div>
                <h3 style='color:{TEXT};font-size:24px;font-weight:800;margin:0 0 10px 0;'>Hello, {username}!</h3>
                <p style='color:{SUBTEXT};font-size:15px;margin:0;line-height:1.7;'>
                    I'm <b style="color:{ACCENT};">ChartBot AI</b> — your intelligent database assistant.<br>
                    Ask about sales, trends, customers, or any general question!
                </p>
                <div style='display:flex;gap:10px;justify-content:center;margin-top:18px;flex-wrap:wrap;'>
                    {''.join([f"<span style='background:{BADGE_BG};border:1px solid {BADGE_BOR};color:{BADGE_CLR};border-radius:20px;padding:6px 14px;font-size:12px;font-weight:600;'>{b}</span>" for b in badges2])}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Display messages
        for i, message in enumerate(st.session_state.messages):
            if message.get("role") == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(f"<p style='color:{TEXT};font-size:15px;margin:0;font-weight:500;'>{message.get('content','')}</p>", unsafe_allow_html=True)
            else:
                with st.chat_message("assistant", avatar="📊"):
                    explanation = message.get("explanation","")
                    if explanation:
                        st.markdown(f"<p style='color:{TEXT};font-size:15px;line-height:1.8;margin:0 0 10px 0;'>{explanation}</p>", unsafe_allow_html=True)
                    ct = message.get("chart_type","")
                    if ct == "er_diagram":
                        render_mermaid(generate_flowchart("er"))
                    elif ct == "flowchart":
                        render_mermaid(generate_flowchart("process"))
                    else:
                        if message.get("sql"):
                            with st.expander("View SQL Query"):
                                st.code(message["sql"], language="sql")
                        if message.get("dataframe") is not None:
                            st.dataframe(message["dataframe"], use_container_width=True)
                        if message.get("chart") is not None:
                            fig = message["chart"]
                            fig.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=PLOT_BG,
                                font=dict(color=TEXT, family='Plus Jakarta Sans'),
                                title=dict(font=dict(color=TEXT, size=16)),
                                xaxis=dict(gridcolor=GRID_CLR, color=AXIS_CLR),
                                yaxis=dict(gridcolor=GRID_CLR, color=AXIS_CLR),
                            )
                            st.plotly_chart(fig, use_container_width=True, key=f"msg_{i}_chart")

        # Chat input
        if prompt := st.chat_input(f"Ask me anything, {username}... (data, charts, diagrams, general questions)"):
            st.session_state.messages.append({"role":"user","content":prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"<p style='color:{TEXT};font-size:15px;margin:0;font-weight:500;'>{prompt}</p>", unsafe_allow_html=True)
            with st.chat_message("assistant", avatar="📊"):
                with st.spinner("🤔 Thinking..."):
                    result = ask_agent(prompt, st.session_state.chat_history)
                key_sfx = f"new_{len(st.session_state.messages)}"
                df, fig = process_render(result, key_suffix=key_sfx)
            explanation = result.get("explanation","Here are the results!")
            sql         = result.get("sql")
            chart_type  = result.get("chart_type","none")
            st.session_state.chat_history.append({"role":"user","content":prompt})
            st.session_state.chat_history.append({"role":"assistant","content":explanation})
            st.session_state.messages.append({
                "role":"assistant","explanation":explanation,"sql":sql,
                "dataframe":df,"chart":fig,"chart_type":chart_type
            })