import streamlit as st
import pandas as pd
import plotly.express as px
import io
import requests
from groq import Groq

# =====================================================================
# 1. CORE ENTERPRISE INITIALIZATION & GOOGLE SIDEBAR CSS STYLING
# =====================================================================
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

st.markdown("""
    <style>
    /* Ficha muundo wa kawaida wa kurasa za Streamlit Nav */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Mtindo wa Upau Vaux Pembeni wa Google (Google Sidebar Styling) */
    .google-brand {
        font-size: 24px;
        font-weight: 500;
        color: #1a73e8;
        font-family: 'Google Sans', 'Segoe UI', Arial, sans-serif;
        margin-bottom: 25px;
        padding-left: 8px;
    }
    
    /* Mistari ya amri yenye ikoni ndogo (Google Menu Item Style) */
    .google-menu-item {
        font-size: 15px;
        color: #3c4043;
        font-family: sans-serif;
        padding: 10px 8px;
        display: flex;
        align-items: center;
        gap: 14px;
        cursor: pointer;
        border-radius: 4px;
    }
    .google-menu-item:hover {
        background-color: #f1f3f4;
    }
    
    .google-section-title {
        font-size: 13px;
        font-weight: 500;
        color: #70757a;
        margin-top: 25px;
        margin-bottom: 12px;
        padding-left: 8px;
    }
    
    /* Orodha ya vitu vilivyotafutwa hivi karibuni */
    .google-history-item {
        font-size: 14px;
        color: #3c4043;
        padding: 8px 8px;
        margin-bottom: 2px;
        border-radius: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .google-history-item:hover {
        background-color: #f1f3f4;
        cursor: pointer;
    }
    
    /* Mapovu mapya ya Chat ya Ask MIKA */
    .chat-user-row { background-color: #e2f0d9; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; color: #1e3d14; }
    .chat-mika-row { background-color: #f1f1f1; padding: 12px 16px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #1a73e8; color: #222222; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. REAL CORPORATE DATA MATRIX POOLS
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

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "search_logs" not in st.session_state:
    st.session_state["search_logs"] = [
        "i want to start a new project as i l...",
        "what's up i'm not getting any fee...",
        "how to use postman tool on my l...",
        "can you outline the differences b..."
    ]

# ZILE MA-WHYS NA TEXTS ZAKO ZOTE ZA MWANZO KUKAMILIKA (100% Restored)
text_dict = {
    "English": {
        "title": "🖥️ MIKA Global Enterprise Sales Command Dashboard",
        "desc": "Automated system processing transactional revenue logs and official target metrics independently.",
        "risk_banner": "⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack identified stockist data. This is a tracking concern, not an immediate financial loss.",
        "chart1": "🌍 Regional Market Share & Contribution",
        "chart2": "💳 Credit Terms & Liquidity Exposure Pipeline",
        "ai_header": "🧠 Simulated n8n Automation & Audit Engine",
        "ai_prompt": "Activate the simulated backend node pipeline to clean raw records and stream insights.",
        "ai_btn": "🚀 Trigger Local n8n Orchestration Pipeline",
        "ai_idle": "💡 Local n8n Simulator Core: Idle. Pipeline waiting for execution command.",
        "chat_header": "💬 Ask MIKA — Limitless Market Intelligence Chatbot",
        "chat_desc": "Ask any business, competitor (Samsung, LG, Ramtons, Hisense, Alyassin), supply chain, stockout, or market query related to Kenya.",
        "chat_ph": "Type your query here and press enter...",
        "chat_title": "Ya hivi majuzi"
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata mapato ya miamala na vyanzo rasmi vya malengo kando.",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za wauzaji maalum. Hili ni suala la ufuatiliaji, sio upotezaji wa kifedha wa haraka.",
        "chart1": "🌍 Uchangiaji wa Mauzo Kimkoa",
        "chart2": "💳 Masharti ya Malipo na Hali ya ukwasi wa Mtaji",
        "ai_header": "🧠 Mfumo wa Kiotomatiki wa n8n",
        "ai_prompt": "Washa mfumo wa n8n kusafisha data na kutoa ripoti.",
        "ai_btn": "🚀 Washa n8n Pipeline ya Ndani",
        "ai_idle": "💡 Mfumo wa n8n: Hausumbuki. Unasubiri amri yako.",
        "chat_header": "💬 Uliza MIKA — Chatbot ya Soko la Kimataifa",
        "chat_desc": "Uliza swali lolote kuhusu biashara, washindani (Samsung, LG, Ramtons, Hisense, Alyassin), usambazaji, au upungufu wa bidhaa nchini Kenya.",
        "chat_ph": "Andika swali lako hapa na ubonyeze enter...",
        "chat_title": "Ya hivi majuzi"
    }
}

# =====================================================================
# 3. REAL GOOGLE SIDEBAR INTEGRATION
# =====================================================================
with st.sidebar:
    st.markdown('<div class="google-brand">G &nbsp; mika chat bot</div>', unsafe_allow_html=True)
    lang = st.radio("Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    groq_api_key = st.text_input("Groq API Key:", type="password", help="Weka Groq API Key yako")
    st.write("---")
    
    st.markdown('<div class="google-menu-item">📝 Mazungumzo mapya</div>', unsafe_allow_html=True)
    st.markdown('<div class="google-menu-item">🔍 Tafuta mazungumzo</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="google-section-title">Kompyuta ndogo</div>', unsafe_allow_html=True)
    st.markdown('<div class="google-menu-item">➕ Weka daftari</div>', unsafe_allow_html=True)
    st.markdown('<div class="google-menu-item">📁 poe business project</div>', unsafe_allow_html=True)
    st.write("---")
    
    page = st.radio(
        "Chagua Mtazamo:",
        ["📈 Executive Overview & Pipeline", "🧠 Simulated n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"],
        label_visibility="collapsed"
    )
    st.write("---")
    
    st.markdown(f'<div class="google-section-title">{text_dict[lang]["chat_title"]}</div>', unsafe_allow_html=True)
    if st.session_state["search_logs"]:
        for idx, log in enumerate(st.session_state["search_logs"]):
            st.markdown(f'<div class="google-history-item">💬 {log}</div>', unsafe_allow_html=True)
            
    st.write("---")
    clear_action = st.checkbox("🗑️ Clear History & Logs")
    if clear_action:
        st.session_state["chat_history"] = []
        st.session_state["search_logs"] = []
        st.rerun()

# =====================================================================
# 4. PRIMARY MAIN PANEL CONTROLLER (100% NO ELSE BLOCKS)
# =====================================================================
st.title(text_dict[lang]["title"])
st.caption(text_dict[lang]["desc"])
st.warning(text_dict[lang]["risk_banner"])
st.write("---")

# --- VIEW 1: EXECUTIVE OVERVIEW ---
if page == "📈 Executive Overview & Pipeline":
    st.header(text_dict[lang]["chart1"])
    st.dataframe(df_region, use_container_width=True, hide_index=True)
    
    fig_region = px.bar(df_region, x="Region Name", y="Total_Sales", color="Region Name", title="Visual representation of Sales Volume per Territory", template="plotly_white")
    st.plotly_chart(fig_region, use_container_width=True)
    
    st.write("---")
    st.header(text_dict[lang]["chart2"])
    st.dataframe(df_payment, use_container_width=True, hide_index=True)
    
    fig_payment = px.pie(df_payment, values="Value Exc. VAT", names="Payment Terms", hole=0.4, title="Credit Term Allocations Share Breakdown")
    st.plotly_chart(fig_payment, use_container_width=True)

# --- VIEW 2: REAL N8N CORE AUTOMATION ---
if page == "🧠 Simulated n8n Orchestration Core":
    st.subheader(text_dict[lang]["ai_header"])
    st.write(text_dict[lang]["ai_prompt"])
    
    n8n_url = st.text_input("n8n Webhook URL Target Endpoint:", value="http://localhost:5678/webhook/mika-data-sync")
    
    if st.button(text_dict[lang]["ai_btn"], type="primary"):
        st.info("Firing outbound trigger parameters to local n8n automation lane...")
        try:
            payload = {
                "source": "streamlit_command_center",
                "region_matrix": region_csv,
                "payment_matrix": payment_csv
            }
            response = requests.post(n8n_url, json=payload, timeout=8)
            if response.status_code == 200:
                st.success("✅ n8n Pipeline completed execution step successfully!")
                st.json(response.json() if response.headers.get('content-type') == 'application/json' else {"response": response.text})
            if response.status_code != 200:
                st.error(f"❌ Automation server returned code: {response.status_code}")
