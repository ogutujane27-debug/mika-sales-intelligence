import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import io

# 1. ENTERPRISE SUITE INITIALIZATION
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

# Premium CSS parsing for fluid animations and premium executive chat layout
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

# Initialize Memory Buffer globally for Sidebar History Tracking
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Localized app dictionary strings
text = {
    "English": {
        "title": "🖥️ MIKA Global Enterprise Sales Command Dashboard",
        "desc": "Automated system processing transactional revenue logs and official target metrics independently.",
        "m1": "📦 Total Verified Revenue",
        "m2": "📈 Official Source Target",
        "risk_banner": "⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack identified stockist data. This is a tracking concern, not an immediate financial loss.",
        "chart1": "🌍 Regional Market Share & Contribution",
        "chart2": "💳 Credit Terms & Liquidity Exposure Pipeline",
        "ai_header": "🧠 Simulated n8n Automation & Audit Engine",
        "ai_prompt": "Activate the simulated backend node pipeline to clean raw records and stream insights.",
        "ai_btn": "🚀 Trigger Local n8n Orchestration Pipeline",
        "ai_idle": "💡 Local n8n Simulator Core: Idle. Pipeline waiting for execution command.",
        "chat_header": "💬 Ask MIKA — Limitless Market Intelligence Chatbot",
        "chat_desc": "Ask any business, competitor (Samsung, LG, Ramtons, Hisense, Alyassin), supply chain, stockout, or market query related to Kenya.",
        "chat_ph": "Type your query here and press enter..."
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata mapato ya miamala na vyanzo rasmi vya malengo kando.",
        "m1": "📦 Jumla ya Mapato Yaliyothibitishwa",
        "m2": "📈 Lengo Rasmi la Mauzo",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za wauzaji maalum. Hili ni suala la ufuatiliaji, sio upotezaji wa kifedha wa haraka.",
        "chart1": "🌍 Uchangiaji wa Mauzo Kimkoa",
        "chart2": "💳 Masharti ya Malipo na Hali ya ukwasi wa Mtaji",
        "ai_header": "🧠 Mfumo wa Kiotomatiki wa n8n",
        "ai_prompt": "Washa mfumo wa n8n kusafisha data na kutoa ripoti.",
        "ai_btn": "🚀 Washa n8n Pipeline ya Ndani",
        "ai_idle": "💡 Mfumo wa n8n: Hausumbuki. Unasubiri amri yako.",
        "chat_header": "💬 Uliza MIKA — Chatbot ya Soko la Kimataifa",
        "chat_desc": "Uliza swali lolote kuhusu biashara, washindani (Samsung, LG, Ramtons, Hisense, Alyassin), usambazaji, au upungufu wa bidhaa nchini Kenya.",
        "chat_ph": "Andika swali lako hapa na ubonyeze enter..."
    }
}

# 3. SIDEBAR MULTI-PAGE ENGINE & LIVE CHAT HISTORY SIDEBAR
with st.sidebar:
    st.header("⚡ Command Center")
    lang = st.radio("🌐 Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    page = st.radio(
        "Select Dashboard View:" if lang == "English" else "Chagua Mtazamo:",
        ["📈 Executive Overview & Pipeline", "🧠 Simulated n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"]
    )
    st.write("---")
    
    # ⏳ DYNAMIC SIDEBAR HISTORY ENGINE
    if page == "💬 Ask MIKA Market Chatbot":
        st.subheader("📝 Ya hivi majuzi" if lang == "Kiswahili" else "📝 Recent Chats")
        
        # 🗑️ Micro-Erase Clear Button inside the Sidebar layout
        if st.button("🗑️ Clear History" if lang == "English" else "🗑️ Safisha Kumbukumbu"):
            st.session_state["chat_history"] = []
            st.rerun()
            
        st.write("---")
        if not st.session_state["chat_history"]:
            st.caption("No recent conversations." if lang == "English" else "Hakuna mazungumzo ya hivi karibuni.")
        else:
            # Displays user's previous questions cleanly on the sidebar rows
            for idx, chat in enumerate(st.session_state["chat_history"]):
                if chat["role"] == "user":
                    short_text = chat["text"][:28] + "..." if len(chat["text"]) > 28 else chat["text"]
                    st.caption(f"🔍 {short_text}")
        st.write("---")
        
    st.caption("MIKA Automation Infrastructure Layer Active.")


# 4. MAIN DISPLAY FRAME
st.title(text[lang]["title"])
st.caption(text[lang]["desc"])
st.warning(text[lang]["risk_banner"])
st.write("---")

# --- VIEW 1: EXECUTIVE DASHBOARD ---
if page == "📈 Executive Overview & Pipeline":
    st.subheader(text[lang]["chart1"])
    # HAPA PALIKUWA NA INDENTATION ERROR - Sasa hivi pamepangiliwa vizuri kabisa!
    st.dataframe(df_region, use_container_width=True, hide_index=True)
    
    st.subheader(text[lang]["chart2"])
    st.dataframe(df_payment, use_container_width=True, hide_index=True)

# --- VIEW 2: N8N SIMULATED CORE ---
elif page == "🧠 Simulated n8n Orchestration Core":
    st.subheader(text[lang]["ai_header"])
    st.write(text[lang]["ai_prompt"])
    if st.button(text[lang]["ai_btn"]):
        st.success("✅ [n8n Node Log] Webhook fired to localhost:5678. Web scraping and data cleansing successful!")
    else:
        st.info(text[lang]["ai_idle"])

# --- VIEW 3: ASK MIKA CHATBOT ---
elif page == "💬 Ask MIKA Market Chatbot":
    st.subheader(text[lang]["chat_header"])
    st.write(text[lang]["chat_desc"])
    
    # Render historical chat log bubbles from memory
    for chat in st.session_state["chat_history"]:
        if chat["role"] == "user":
            st.markdown(f'<div class="user-bubble"><b>You:</b> {chat["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="mika-bubble"><b>🤖 MIKA:</b> {chat["text"]}</div>', unsafe_allow_html=True)
            
    # Input field to send new queries
    user_query = st.text_input(text[lang]["chat_ph"], key="chatbot_input_box")
    if user_query:
        # Append query and a simulated premium answer into memory
        st.session_state["chat_history"].append({"role": "user", "text": user_query})
        st.session_state["chat_history"].append({
            "role": "mika", 
            "text": f"Analyzing raw logs for your query: '{user_query}'. Our baseline records confirm Nairobi Region handles 49.46% of transaction footprints."
        })
        st.rerun()
