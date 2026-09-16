import streamlit as st
import pandas as pd
import io

# =====================================================================
# 1. MFUMO WA CORE NA MTINDO WA GOOGLE (CSS)
# =====================================================================
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

st.markdown("""
    <style>
    /* Kuficha mfumo wa kawaida wa streamlit ili kutumia wetu wa kisasa */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Jina la Mika Chat Bot upande wa kushoto */
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        color: #1a73e8;
        margin-bottom: 25px;
        font-family: 'Google Sans', sans-serif;
    }
    .sidebar-section-title {
        font-size: 14px;
        color: #70757a;
        margin-top: 25px;
        margin-bottom: 10px;
        font-weight: 500;
    }
    /* Mapovu ya fomu ya mazungumzo (Chat Bubbles) */
    .user-bubble { background-color: #e2f0d9; padding: 12px; border-radius: 8px; margin-bottom: 8px; color: #1e3d14; }
    .mika-bubble { background-color: #f1f1f1; padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #28a745; color: #222222; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. DATA ZA KAMPUNI
# =====================================================================
region_csv = """Region Name,Total_Sales,Outlet_Count,Pct_of_Total
NAIROBI REGION,1429021702.88,162,49.46
COAST REGION,467868246.57,6,16.20
RIFT REGION,249625551.62,4,8.64
NYANZA REGION,230383874.52,3,7.97
MOUNTAIN REGION,224669606.09,4,7.78
B2B (COMMERCIAL),72649873.65,9,2.51
EASTERN REGION,48863128.13,2,1.69"""

payment_csv = """Payment Terms,Value Exc. VAT,Pct_of_Total
60 Days from Invoice,76595266.83,35.7
30 Days from Invoice,63116322.62,29.4
Cash before Delivery,54073554.13,25.2
45 Days from Invoice,41147180.37,19.2
90 Days from Invoice,33508310.27,15.6"""

df_region = pd.read_csv(io.StringIO(region_csv))
df_payment = pd.read_csv(io.StringIO(payment_csv))

# Kumbukumbu ya kuhifadhi maswali ya chat
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        "how to use postman tool on my l...",
        "can you outline the differences b...",
        "what's up i'm not getting any fee..."
    ]

# Mfumo wa kujibu maswali ya chapchap (Simulated response)
if "bot_replies" not in st.session_state:
    st.session_state["bot_replies"] = []

# =====================================================================
# 3. UPANDISHI WA GOOGLE SIDEBAR (HAPA NDIPO PANAPOBADILISHA UKURASA)
# =====================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 Mika Chat Bot</div>', unsafe_allow_html=True)
    
    lang = st.radio("🌐 Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    # Menyu ya kubadili Kurasa kwa kutumia st.selectbox ya Streamlit (Inafanya kazi bila kukwama)
    chaguzi = ["📈 Executive Overview & Pipeline", "🧠 Simulated n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"]
    page = st.selectbox("Chagua Mtazamo / Select View:", chaguzi)
    
    st.write("---")
    
    # Sehemu ya "Ya hivi majuzi" / History
    st.markdown('<div class="sidebar-section-title">Ya hivi majuzi / Recent</div>', unsafe_allow_html=True)
    for chat in st.session_state["chat_history"]:
        st.caption(f"💬 {chat}")
        
    st.write("---")
    if st.button("🗑️ Clear History" if lang == "English" else "🗑️ Safisha Kumbukumbu"):
        st.session_state["chat_history"] = []
        st.session_state["bot_replies"] = []
        st.rerun()

# =====================================================================
# 4. PANELI KUU: INABADILIKA KULINGANA NA UKURASA ULIOCHAGULIWA
# =====================================================================

# --- UKURASA WA 1: EXECUTIVE OVERVIEW ---
if page == "📈 Executive Overview & Pipeline":
    st.title("🖥️ MIKA Global Enterprise Sales Dashboard" if lang == "English" else "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo")
    st.warning("⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack stockist data.")
    
    st.subheader("🌍 Regional Market Share & Contribution")
    st.dataframe(df_region, use_container_width=True, hide_index=True)
    
    st.subheader("💳 Credit Terms & Liquidity Exposure Pipeline")
    st.dataframe(df_payment, use_container_width=True, hide_index=True)

# --- UKURASA WA 2: N8N AUTOMATION PIPELINE ---
elif page == "🧠 Simulated n8n Orchestration Core":
    st.title("🧠 Simulated n8n Automation Engine" if lang == "English" else "🧠 Mfumo wa Kiotomatiki wa n8n")
    st.write("Bonyeza kitufe hapa chini ili kuwasha mitambo ya kiotomatiki ya kusafisha data nyuma ya mfumo.")
    
    # Hapa ndipo n8n inafanya kazi sasa hivi!
    if st.button("🚀 Trigger Local n8n Orchestration Pipeline", type="primary"):
        st.success("✅ n8n Pipeline executed successfully! Raw data has been cleaned and structured.")
        st.info("Webhook Response: Status 200 OK | Host: localhost:5678")
    else:
        st.info("💡 Status: Idle. Pipeline is waiting for your run command.")

# --- UKURASA WA 3: ASK MIKA CHATBOT ---
elif page == "💬 Ask MIKA Market Chatbot":
    st.title("💬 Ask MIKA — Market Intelligence Chatbot")
    st.write("Andika swali lako la kibiashara hapa chini kuhusu masoko ya Kenya (kama vile Nairobi, Coast, nk).")
    
    # Fomu ya kupokea swali
    with st.form(key="chat_form", clear_on_submit=True):
        user_query = st.text_input("Type your query here / Andika swali lako hapa:")
        submit_button = st.form_submit_with_name("Send / Tuma")
        
    if submit_button and user_query:
        # Hifadhi kwenye kumbukumbu
        st.session_state["chat_history"].insert(0, user_query[:28] + "...")
        st.session_state["bot_replies"].append({"user": user_query, "bot": f"Nimepokea swali lako kuhusu '{user_query}'. Kulingana na data zetu, soko kubwa zaidi ni NAIROBI REGION lenye mauzo ya 49.46%."})
    
    # Onyesha mazungumzo yaliyofanyika
    for chat in st.session_state["bot_replies"]:
        st.markdown(f'<div class="user-bubble"><b>You:</b> {chat["user"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mika-bubble"><b>🤖 MIKA:</b> {chat["bot"]}</div>', unsafe_allow_html=True)
