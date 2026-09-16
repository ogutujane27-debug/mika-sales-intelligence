import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. ENTERPRISE SUITE INITIALIZATION (Inatakiwa iwe moja tu juu kabisa)
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

# Premium CSS parsing kwa ajili ya muundo wa kileo na mtindo wa Google
st.markdown("""
    <style>
    @keyframes slideUp { 
        0% { opacity: 0; transform: translateY(15px); } 
        100% { opacity: 1; transform: translateY(0); } 
    }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stMetric, .element-container { animation: slideUp 0.5s ease-out forwards; }
    
    /* Green Run/Execute button theme */
    .stButton>button { 
        background-color: #28a745 !important; color: white !important; font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(40,167,69,0.25); border-radius: 6px !important; width: 100%; height: 45px;
    }
    .stDownloadButton>button {
        background-color: #007bff !important; color: white !important; font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0,123,255,0.25); border-radius: 6px !important; width: 100%; height: 45px;
    }
    
    /* Kuondoa nafasi kubwa juu ya sidebar na kuficha usafiri wa kawaida */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Mtindo wa herufi na muundo wa Mika Chat Bot Sidebar */
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
    .user-bubble { background-color: #e2f0d9; padding: 12px; border-radius: 8px; margin-bottom: 8px; color: #1e3d14; font-family: sans-serif; }
    .mika-bubble { background-color: #f1f1f1; padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #28a745; color: #222222; font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

# 2. REAL CORPORATE DATA MATRIX POOLS
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

# Initialize Memory Buffer globally kwa ajili ya historia halisi
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "user", "text": "how to use postman tool on my local pc"},
        {"role": "user", "text": "can you outline the differences between GET and POST"},
        {"role": "user", "text": "what's up i'm not getting any feedback"}
    ]

# Localized app dictionary strings
text_dict = {
    "English": {
        "title": "🖥️ MIKA Global Enterprise Sales Command Dashboard",
        "desc": "Automated system processing transactional revenue logs and official target metrics independently.",
        "m1": "📦 Total Verified Revenue",
        "m2": "📈 Official Source Target",
        "risk_banner": "⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack identified stockist data.",
        "chat_title": "Recent Chats"
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata mapato ya miamala na vyanzo rasmi vya malengo kando.",
        "m1": "📦 Jumla ya Mapato Yaliyothibitishwa",
        "m2": "📈 Lengo Rasmi la Mauzo",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za wauzaji maalum.",
        "chat_title": "Ya hivi majuzi"
    }
}

# 3. GOOGLE-STYLE SIDEBAR INTEGRATION
with st.sidebar:
    # Nembo kuu uliyoiomba iandikwe "Mika Chat Bot"
    st.markdown('<div class="sidebar-title">🤖 Mika Chat Bot</div>', unsafe_allow_html=True)
    
    # Lugha / Language controller
    lang = st.radio("🌐 Lugha / Language:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    # Vitufe vikuu vya uendeshaji
    if st.button("➕ Mazungumzo mapya" if lang == "Kiswahili" else "➕ New Conversation", use_container_width=True):
        st.session_state["chat_history"] = []
        st.rerun()
        
    if st.button("🔍 Tafuta mazungumzo" if lang == "Kiswahili" else "🔍 Search Chats", use_container_width=True):
        st.toast("Sehemu ya utafutaji inakuja hivi karibuni!")
    
    st.write("---")
    
    # Kuchagua Ukurasa/Mtazamo wa Dashboard
    page = st.radio(
        "Select Dashboard View:" if lang == "English" else "Chagua Mtazamo:",
        ["📈 Executive Overview & Pipeline", "🧠 Simulated n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"]
    )
    
    st.write("---")
    
    # ⏳ DYNAMIC SIDEBAR HISTORY ENGINE (Inafanana kabisa na muundo wa Google uliochagua!)
    st.markdown(f'<div class="sidebar-section-title">{text_dict[lang]["chat_title"]}</div>', unsafe_allow_html=True)
    
    if not st.session_state["chat_history"]:
        st.caption("No recent conversations." if lang == "English" else "Hakuna mazungumzo ya hivi karibuni.")
    else:
        # Inasoma historia yako halisi na kuionyesha kama list nadhifu ya kubofya
        for idx, chat in enumerate(st.session_state["chat_history"]):
            short_text = chat["text"][:28] + "..." if len(chat["text"]) > 28 else chat["text"]
            if st.button(f"💬 {short_text}", key=f"hist_{idx}", use_container_width=True):
                st.toast(f"Ulichagua: {chat['text']}")
                
    st.write("---")
    # Kitufe cha kufuta kumbukumbu chini kabisa ya list
    if st.button("🗑️ Clear History" if lang == "English" else "🗑️ Safisha Kumbukumbu", key="clear_history_btn"):
        st.session_state["chat_history"] = []
        st.rerun()

# 4. MAIN BODY DASHBOARD PANEL
st.title(text_dict[lang]["title"])
st.caption(text_dict[lang]["desc"])
st.warning(text_dict[lang]["risk_banner"])

# Onyesha Dataframe bila Indentation Error ya mwanzo
if 'df_region' in locals():
    st.subheader("📊 Regional Performance Overview")
    st.dataframe(df_region, use_container_width=True, hide_index=True)
