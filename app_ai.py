import streamlit as st
import pandas as pd
import plotly.express as px
import io

# =====================================================================
# 1. CORE ENTERPRISE INITIALIZATION & GOOGLE SIDEBAR CSS STYLING
# =====================================================================
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

st.markdown("""
    <style>
    /* Ficha muundo wa kawaida wa kurasa za Streamlit */
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

# Initialize session arrays safely
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "search_logs" not in st.session_state:
    st.session_state["search_logs"] = [
        "i want to start a new project as i l...",
        "what's up i'm not getting any fee...",
        "how to use postman tool on my l...",
        "can you outline the differences b..."
    ]

# Multi-lingual Dictionary configuration 
text_dict = {
    "English": {
        "title": "🖥️ MIKA Global Enterprise Sales Command Dashboard",
        "desc": "Automated system processing transactional revenue logs and official target metrics independently.",
        "risk_banner": "⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack identified stockist data. This is a tracking concern, not an immediate financial loss.",
        "chat_title": "Ya hivi majuzi"
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata mapato ya miamala na vyanzo rasmi vya malengo kando.",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za wauzaji maalum.",
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
    
    st.markdown('<div class="google-menu-item">📝 Mazungumzo mapya</div>', unsafe_allow_html=True)
    st.markdown('<div class="google-menu-item">🔍 Tafuta mazungumzo</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="google-section-title">Kompyuta ndogo</div>', unsafe_allow_html=True)
    st.markdown('<div class="google-menu-item">➕ Weka daftari</div>', unsafe_allow_html=True)
    st.markdown('<div class="google-menu-item">📁 poe business project</div>', unsafe_allow_html=True)
    
    st.write("---")
    
    st.markdown('<div class="google-section-title">Chagua Ukurasa / Views</div>', unsafe_allow_html=True)
    page = st.selectbox(
        "Chagua Mtazamo:",
        ["📈 Executive Overview & Pipeline", "🧠 Simulated n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"],
        label_visibility="collapsed"
    )
    
    st.write("---")
    
    st.markdown(f'<div class="google-section-title">{text_dict[lang]["chat_title"]}</div>', unsafe_allow_html=True)
    
    if not st.session_state["search_logs"]:
        st.caption("Hakuna rekodi.")
    else:
        for idx, log in enumerate(st.session_state["search_logs"]):
            st.markdown(f'<div class="google-history-item">💬 {log}</div>', unsafe_allow_html=True)
            
    st.write("---")
    
    st.markdown('<div class="google-section-title">⚙️ Mipangilio / Settings</div>', unsafe_allow_html=True)
    clear_action = st.checkbox("🗑️ Clear History & Logs")
    if clear_action:
        st.session_state["chat_history"] = []
        st.session_state["search_logs"] = []
        st.toast("Kumbukumbu zote zimefutwa!")
        st.rerun()

# =====================================================================
# 4. PRIMARY MAIN PANEL CONTROLLER
# =====================================================================
st.title(text_dict[lang]["title"])
st.caption(text_dict[lang]["desc"])
st.warning(text_dict[lang]["risk_banner"])
st.write("---")

# --- VIEW 1: EXECUTIVE OVERVIEW ---
if page == "📈 Executive Overview & Pipeline":
    st.header("🌍 Regional Market Share & Contribution")
    st.dataframe(df_region, use_container_width=True, hide_index=True)
    
    fig_region = px.bar(
        df_region, 
        x="Region Name", 
        y="Total_Sales", 
        color="Region Name", 
        title="Visual representation of Sales Volume per Territory",
        template="plotly_white"
    )
    st.plotly_chart(fig_region, use_container_width=True)
    
    st.write("---")
    st.header("💳 Credit Terms & Liquidity Exposure Pipeline")
    st.dataframe(df_payment, use_container_width=True, hide_index=True)
    
    fig_payment = px.pie(
        df_payment, 
        values="Value Exc. VAT", 
        names="Payment Terms", 
        hole=0.4, 
        title="Credit Term Allocations Share Breakdown"
    )
    st.plotly_chart(fig_payment, use_container_width=True)

# --- VIEW 2: N8N CORE AUTOMATION ---
elif page == "🧠 Simulated n8n Orchestration Core":
    st.subheader("🧠 Simulated n8n Webhook Node Engine Integration")
    st.write("Press the core activation node pipeline to parse database transactional strings.")
    
    if st.button("🚀 Trigger Local n8n Orchestration Pipeline", type="primary"):
        st.success("✅ [Status 200 OK] Live Pipeline Webhook Response Stream Complete!")
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

# --- VIEW 3: ASK MIKA CHATBOT ENGINE ---
elif page == "💬 Ask MIKA Market Chatbot":
    st.subheader("💬 Ask MIKA — Limitless Market Intelligence Chatbot")
    
    for chat in st.session_state["chat_history"]:
        if chat["role"] == "user":
            st.markdown(f'<div class="chat-user-row"><b>You:</b> {chat["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-mika-row"><b>🤖 MIKA:</b> {chat["text"]}</div>', unsafe_allow_html=True)
            
        query_box = st.chat_input("Ask any business or competitor query here...")
    if query_box:
        if query_box not in st.session_state["search_logs"]:
            st.session_state["search_logs"].insert(0, query_box[:28] + "...")
            
        st.session_state["chat_history"].append({"role": "user", "text": query_box})
        
        bot_response = f"Analyzing raw logs for your query: '{query_box}'. Our baseline records confirm Nairobi Region handles 49.46% of transaction footprints."
        st.session_state["chat_history"].append({"role": "mika", "text": bot_response})
        st.rerun()
        
        query_box = st.chat_input("Ask any business or competitor query here...")
    if query_box:
        if query_box not in st.session_state["search_logs"]:
            st.session_state["search_logs"].insert(0, query_box[:28] + "...")
            
        st.session_state["chat_history"].append({"role": "user", "text": query_box})
        
        bot_response = f"Analyzing raw logs for your query: '{query_box}'. Our baseline records confirm Nairobi Region handles 49.46% of transaction footprints."
        st.session_state["chat_history"].append({"role": "mika", "text": bot_response})
        st.rerun()


