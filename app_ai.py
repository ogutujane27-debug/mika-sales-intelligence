import streamlit as st
import pandas as pd
import io

# =====================================================================
# 1. SYSTEM SETUP
# =====================================================================
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

# Premium CSS for Google-style layout and buttons
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
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
    /* Green Run/Execute button theme */
    .stButton>button { 
        background-color: #28a745 !important; color: white !important; font-weight: bold !important;
        border-radius: 6px !important; width: 100%; height: 45px;
    }
    .user-bubble { background-color: #e2f0d9; padding: 12px; border-radius: 8px; margin-bottom: 8px; color: #1e3d14; }
    .mika-bubble { background-color: #f1f1f1; padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #28a745; color: #222222; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. BUSINESS DATA
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
    st.session_state["chat_history"] = [
        {"text": "how to use postman tool on my local pc"},
        {"text": "can you outline the differences between GET and POST"},
        {"text": "what's up i'm not getting any feedback"}
    ]

# Lugha / Translations
text_dict = {
    "English": {
        "title": "🖥️ MIKA Global Enterprise Sales Command Dashboard",
        "desc": "Automated system processing transactional revenue logs and official target metrics independently.",
        "risk_banner": "⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack identified stockist data.",
        "chat_title": "Recent Chats"
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata mapato ya miamala na vyanzo rasmi vya malengo kando.",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za wauzaji maalum.",
        "chat_title": "Ya hivi majuzi"
    }
}

# =====================================================================
# 3. GOOGLE-STYLE SIDEBAR
# =====================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 Mika Chat Bot</div>', unsafe_allow_html=True)
    
    lang = st.radio("🌐 Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    if st.button("➕ Mazungumzo mapya" if lang == "Kiswahili" else "➕ New Conversation", use_container_width=True):
        st.session_state["chat_history"] = []
        st.rerun()
        
    if st.button("🔍 Tafuta mazungumzo" if lang == "Kiswahili" else "🔍 Search Chats", use_container_width=True):
        st.toast("Utafutaji unakuja hivi karibuni!")
    
    st.write("---")
    
    page = st.radio(
        "Select Dashboard View:" if lang == "English" else "Chagua Mtazamo:",
        ["📈 Executive Overview & Pipeline", "🧠 Simulated n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"]
    )
    st.write("---")
    
    st.markdown(f'<div class="sidebar-section-title">{text_dict[lang]["chat_title"]}</div>', unsafe_allow_html=True)
    
    for idx, chat in enumerate(st.session_state["chat_history"]):
        short_text = chat["text"][:28] + "..." if len(chat["text"]) > 28 else chat["text"]
        if st.button(f"💬 {short_text}", key=f"nav_log_{idx}", use_container_width=True):
            st.toast(f"Ulichagua: {chat['text']}")
                
    st.write("---")
    if st.button("🗑️ Clear History" if lang == "English" else "🗑️ Safisha Kumbukumbu", key="clear_logs_action"):
        st.session_state["chat_history"] = []
        st.rerun()

# =====================================================================
# 4. MAIN BODY DISPLAY SWITCHING
# =====================================================================
st.title(text_dict[lang]["title"])
st.caption(text_dict[lang]["desc"])
st.warning(text_dict[lang]["risk_banner"])
st.write("---")

# --- PAGE 1: EXECUTIVE OVERVIEW ---
if page == "📈 Executive Overview & Pipeline":
    st.subheader("📊 Regional Market Share & Contribution")
    st.dataframe(df_region, use_container_width=True, hide_index=True)
    
    st.subheader("💳 Credit Terms & Liquidity Exposure Pipeline")
    st.dataframe(df_payment, use_container_width=True, hide_index=True)

# --- PAGE 2: N8N CORE AUTOMATION ---
elif page == "🧠 Simulated n8n Orchestration Core":
    st.subheader("🧠 n8n Automation Engine Pipeline")
    st.write("Welcome to the automation layer. Here you can execute backend workflows.")
    
    if st.button("🚀 Trigger Local n8n Orchestration Pipeline"):
        st.success("✅ n8n Pipeline executed successfully! Data cleaned and loaded into memory.")
        st.info("Webhook captured on localhost:5678. Status: 200 OK")
    else:
        st.info("💡 Local n8n Simulator Core: Idle. Waiting for trigger instruction.")

# --- PAGE 3: ASK MIKA CHATBOT ---
elif page == "💬 Ask MIKA Market Chatbot":
    st.subheader("💬 Ask MIKA — Market Intelligence Chatbot")
    st.write("Ask any business or market query related to Kenya.")
    
    user_query = st.text_input("Type your question here / Andika swali lako hapa:", key="user_question_input")
    
    if user_query:
        # Save to sidebar history dynamically
        st.session_state["chat_history"].insert(0, {"text": user_query})
        
        # Display response bubbles
        st.markdown(f'<div class="user-bubble"><b>You:</b> {user_query}</div>', unsafe_allow_html=True)
        
        # Simple local AI logic for presentation
        response = f"Hello! I am MIKA. I processed your request regarding '{user_query}'. Our top market is NAIROBI REGION with 49.46% of total sales."
        st.markdown(f'<div class="mika-bubble"><b>🤖 MIKA:</b> {response}</div>', unsafe_allow_html=True)
