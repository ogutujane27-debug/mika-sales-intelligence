import streamlit as st
import pandas as pd
import io

# =====================================================================
# 1. CORE SYSTEM SETUP (Must be at the very top, exactly once)
# =====================================================================
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

# Premium CSS for fluid animations and a clean Google-Style Sidebar layout
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
    
    /* Hides the default Streamlit navigation to create a custom feel */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Premium typography styling for your brand-new sidebar layout */
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
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. BUSINESS DATA REPOSITORIES
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

# Initialize Memory Tracking for user histories
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"text": "how to use postman tool on my l..."},
        {"text": "can you outline the differences b..."},
        {"text": "what's up i'm not getting any fee..."}
    ]

# Multi-lingual Dictionary configuration 
text_dict = {
    "English": {
        "title": "🖥️ MIKA Global Enterprise Sales Command Dashboard",
        "desc": "Automated system processing transactional revenue logs and official target metrics independently.",
        "risk_banner": "⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack identified stockist data. This is a tracking concern, not an immediate financial loss.",
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
# 3. GOOGLE-STYLE CUSTOM SIDEBAR
# =====================================================================
with st.sidebar:
    # Google Layout Brand Replacement
    st.markdown('<div class="sidebar-title">🤖 Mika Chat Bot</div>', unsafe_allow_html=True)
    
    # Simple Language Controller Switch
    lang = st.radio("🌐 Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    # Modern Action Operations Buttons
    if st.button("➕ Mazungumzo mapya" if lang == "Kiswahili" else "➕ New Conversation", use_container_width=True):
        st.session_state["chat_history"] = []
        st.rerun()
        
    if st.button("🔍 Tafuta mazungumzo" if lang == "Kiswahili" else "🔍 Search Chats", use_container_width=True):
        st.toast("Sehemu ya utafutaji inakuja hivi karibuni!")
    
    st.write("---")
    
    # Active View Configurations Selector
    page = st.radio(
        "Select Dashboard View:" if lang == "English" else "Chagua Mtazamo:",
        ["📈 Executive Overview & Pipeline", "🧠 Simulated n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"]
    )
    st.write("---")
    
    # ⏳ GOOGLE BROWSING HISTORY LOGS ARCHIVE
    st.markdown(f'<div class="sidebar-section-title">{text_dict[lang]["chat_title"]}</div>', unsafe_allow_html=True)
    
    if not st.session_state["chat_history"]:
        st.caption("No recent conversations." if lang == "English" else "Hakuna mazungumzo ya hivi karibuni.")
    else:
        # Loop through log items neatly without loading yellow paper indicators
        for idx, chat in enumerate(st.session_state["chat_history"]):
            if st.button(f"💬 {chat['text']}", key=f"nav_log_{idx}", use_container_width=True):
                st.toast(f"Selected: {chat['text']}")
                
    st.write("---")
    if st.button("🗑️ Clear History" if lang == "English" else "🗑️ Safisha Kumbukumbu", key="clear_logs_action"):
        st.session_state["chat_history"] = []
        st.rerun()

# =====================================================================
# 4. PRIMARY MAIN DISPLAY PANEL CONTENT
# =====================================================================
st.title(text_dict[lang]["title"])
st.caption(text_dict[lang]["desc"])
st.warning(text_dict[lang]["risk_banner"])

# Secure isolated dataset output frame rendering
st.subheader("📊 Regional Market Share & Contribution")
st.dataframe(df_region, use_container_width=True, hide_index=True)
