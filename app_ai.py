import streamlit as st
import pandas as pd
import plotly.express as px
import io

# =====================================================================
# 1. CORE SYSTEM SETUP & PREMIUM GOOGLE STYLE CSS
# =====================================================================
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

st.markdown("""
    <style>
    /* Kuficha navigation ya kawaida ya Streamlit ili kutumia yetu safi */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Muundo wa Kisasa wa Upau wa Pembeni (Google Sidebar Look) */
    .sidebar-brand {
        font-size: 24px;
        font-weight: bold;
        color: #1a73e8;
        margin-bottom: 20px;
        font-family: 'Google Sans', sans-serif;
    }
    .sidebar-section-title {
        font-size: 14px;
        color: #70757a;
        margin-top: 20px;
        margin-bottom: 8px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .history-item {
        font-size: 14px;
        color: #3c4043;
        padding: 6px 8px;
        border-radius: 4px;
        background-color: #f8f9fa;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Mapovu ya Mazungumzo ya Ask MIKA */
    .user-bubble { background-color: #e2f0d9; padding: 14px; border-radius: 8px; margin-bottom: 8px; color: #1e3d14; font-family: sans-serif; }
    .mika-bubble { background-color: #f1f1f1; padding: 14px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #28a745; color: #222222; font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. CORP DATA MATRIX POOLS
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

# Initialize Dynamic Chat Memory Arrays securely
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "search_logs" not in st.session_state:
    st.session_state["search_logs"] = ["top leading brands", "Nairobi region sales Q4"]

# Dictionary ya Lugha zote mbili
text = {
    "English": {
        "title": "🖥️ MIKA Global Enterprise Sales Command Dashboard",
        "desc": "Automated system processing transactional revenue logs and official target metrics independently.",
        "risk_banner": "⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack identified stockist data.",
        "chart1_title": "🌍 Regional Market Share Distribution (Plotly Visual)",
        "chart2_title": "💳 Liquidity Exposure & Credit Terms Pipeline"
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata mapato ya miamala na vyanzo rasmi vya malengo kando.",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za wauzaji maalum.",
        "chart1_title": "🌍 Uchangiaji wa Mauzo Kimkoa (Grafu ya Plotly)",
        "chart2_title": "💳 Masharti ya Malipo na Hali ya ukwasi wa Mtaji"
    }
}

# =====================================================================
# 3. CLEAN CUSTOM GOOGLE SIDEBAR INTEGRATION
# =====================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🤖 mika chat bot</div>', unsafe_allow_html=True)
    
    lang = st.radio("⚡ Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    page = st.radio(
        "Select Dashboard View:" if lang == "English" else "Chagua Mtazamo:",
        ["📈 Executive Overview & Pipeline", "🧠 Simulated n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"]
    )
    st.write("---")
    
    # ☰ Orodha ya Vitu Vilivyotafutwa (Search Logs List Icon view)
    st.markdown('<div class="sidebar-section-title">☰ Orodha ya Utafutaji / Search Logs</div>', unsafe_allow_html=True)
    
    if not st.session_state["search_logs"]:
        st.caption("No logs recorded." if lang == "English" else "Hakuna rekodi zilizopatikana.")
    else:
        for idx, log in enumerate(st.session_state["search_logs"]):
            st.markdown(f'<div class="history-item">🔍 {log}</div>', unsafe_allow_html=True)
            
    st.write("---")
    
    # 📌 Safisha Kumbukumbu kwa kutumia mtindo mdogo wa vitone vitatu (Three-Dots options menu simulation)
    options_menu = st.selectbox("⚙️ Options / Chaguzi:", ["-- Action Menu --", "🗑️ Delete / Clear History"])
    if options_menu == "🗑️ Delete / Clear History":
        st.session_state["chat_history"] = []
        st.session_state["search_logs"] = []
        st.toast("Kumbukumbu zote zimefutwa kwa mafanikio!")
        st.rerun()

# =====================================================================
# 4. PRIMARY DISPLAY PANEL CONTROLLER
# =====================================================================
st.title(text[lang]["title"])
st.caption(text[lang]["desc"])
st.warning(text[lang]["risk_banner"])
st.write("---")

# --- VIEW 1: FIXED EXECUTIVE DASHBOARD WITH LIVE PLOTLY GRAPHS ---
if page == "📈 Executive Overview & Pipeline":
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Regional Raw Metrics")
        st.dataframe(df_region, use_container_width=True, hide_index=True)
        
    with col2:
        st.subheader(text[lang]["chart1_title"])
        # Kuchora Grafu ya kwanza ya Bar Chart kwa kutumia Plotly Express (Marekebisho makubwa ya Grafu)
        fig_region = px.bar(df_region, x="Region Name", y="Total_Sales", color="Region Name", text_auto='.2s', title="Sales Volume per Territory")
        st.plotly_chart(fig_region, use_container_width=True)
        
    st.write("---")
    
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("📋 Credit Pipeline Matrix")
        st.dataframe(df_payment, use_container_width=True, hide_index=True)
        
    with col4:
        st.subheader(text[lang]["chart2_title"])
        # Kuchora Grafu ya pili ya Pie Chart kwa ajili ya kuonyesha asilimia za malipo
        fig_payment = px.pie(df_payment, values="Value Exc. VAT", names="Payment Terms", hole=0.4, title="Credit Term Allocations")
        st.plotly_chart(fig_payment, use_container_width=True)

# --- VIEW 2: FIXED N8N SIMULATED CORE WITH ENGAGING DETAILED RESPONSE ---
elif page == "🧠 Simulated n8n Orchestration Core":
    st.subheader("🧠 Simulated n8n Webhook Node Engine Integration")
    st.write("Press the core activation node pipeline to parse database transactional strings.")
    
    if st.button("🚀 Trigger Local n8n Orchestration Pipeline", type="primary"):
        st.success("✅ [Status 200 OK] Live Pipeline Webhook Response Stream Complete!")
        
        # Matrix terminal output representation explaining data flows
        with st.expander("📂 View Simulated Node Processing Payload Logs", expanded=True):
            st.code("""
[15:00:21] - Initializing payload extraction from raw CSV strings...
[15:00:22] - Successfully loaded 1,562 active transactional rows into node data frames.
[15:00:23] - Executing data cleanup scripts: Matched 7 geographical sales branches inside Kenya.
[15:00:24] - Metrics computation completed: Total verified database footprint aggregated to memory.
[15:00:25] - Pipeline run completed successfully. Outbound channel state: IDLE.
            """, language="bash")
    else:
        st.info("💡 Standby Mode: Local simulator execution channel waiting for trigger action input.")

# --- VIEW 3: FIXED ASK MIKA CHATBOT WITH NO-DUPLICATING CHAT ENGINE ---
elif page == "💬 Ask MIKA Market Chatbot":
    st.subheader("💬 Ask MIKA — Limitless Market Intelligence Chatbot")
    
    # Render historical chat logs from memory sequentially inside uniform visual bubbles
    for chat in st.session_state["chat_history"]:
        if chat["role"] == "user":
            st.markdown(f'<div class="user-bubble"><b>You:</b> {chat["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="mika-bubble"><b>🤖 MIKA:</b> {chat["text"]}</div>', unsafe_allow_html=True)
            
    # Tumesakinisha st.chat_input ya kisasa ili kuzuia kujirudia kwa maandishi au makosa ya kurefresha
    query_box = st.chat_input("Ask any business or competitor query here...")
    
    if query_box:
        # Save query directly into dynamic sidebar search lists
        if query_box not in st.session_state["search_logs"]:
            st.session_state["search_logs"].insert(0, query_box)
            
        # Append parameters to chat histories seamlessly
        st.session_state["chat_history"].append({"role": "user", "text": query_box})
        
        # Create clear single system automated intelligence answer string
        bot_response = f"Analyzing raw logs for your query: '{query_box}'. Our baseline records confirm Nairobi Region handles 49.46% of transaction footprints."
        st.session_state["chat_history"].append({"role": "mika", "text": bot_response})
        st.rerun()
