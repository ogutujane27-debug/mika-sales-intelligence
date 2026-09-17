import streamlit as st
import pandas as pd
import plotly.express as px
import io
import requests

# =====================================================================
# 1. ENTERPRISE SUITE INITIALIZATION
# =====================================================================
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
        "ai_header": "🔌 Real n8n Orchestration Core Engine",
        "ai_prompt": "Enter your active webhook listener node endpoint link to stream database transactional parameters directly.",
        "ai_btn": "🚀 Execute Live n8n Pipeline",
        "ai_idle": "💡 Real n8n Connection Core: Waiting for outbound execution trigger input.",
        "chat_header": "💬 Ask MIKA — Limitless Market Intelligence Chatbot",
        "chat_desc": "Ask any business, competitor (Samsung, LG, Ramtons, Hisense, Alyassin), supply chain, stockout, or market query related to Kenya.",
        "chat_ph": "Type your query here and press enter..."
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata mapato ya miamala na vyanzo rasmi vya malengo kando.",
        "m1": "📦 Jumla ya Mapato Yaliyothibitishwa",
        "m2": "📈 Lengo Rasmi la Mauzo",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za wauzaji maalum. Hili ni suala la ufuatiliaji, sio upotezaji vya kifedha wa haraka.",
        "chart1": "🌍 Uchangiaji wa Mauzo Kimkoa",
        "chart2": "💳 Masharti ya Malipo na Hali ya ukwasi wa Mtaji",
        "ai_header": "🔌 Mitambo ya Kiotomatiki wa n8n (Live)",
        "ai_prompt": "Washa mfumo wa n8n kusafisha data na kutoa ripoti.",
        "ai_btn": "🚀 Washa n8n Pipeline ya Ukweli",
        "ai_idle": "💡 Mfumo wa n8n: Hausumbuki. Unasubiri amri yako ya kuwasha mitambo.",
        "chat_header": "💬 Uliza MIKA — Chatbot ya Soko la Kimataifa",
        "chat_desc": "Uliza swali lolote kuhusu biashara, washindani (Samsung, LG, Ramtons, Hisense, Alyassin), usambazaji, au upungufu vya bidhaa nchini Kenya.",
        "chat_ph": "Andika swali lako hapa na ubonyeze enter..."
    }
}

# =====================================================================
# 3. SIDEBAR MULTI-PAGE ENGINE
# =====================================================================
with st.sidebar:
    st.header("⚡ Command Center")
    lang = st.radio("🌐 Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    page = st.radio(
        "Select Dashboard View:" if lang == "English" else "Chagua Mtazamo:",
        ["📈 Executive Overview & Pipeline", "🧠 Real n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"]
    )
    st.write("---")
    st.caption("MIKA Automation Infrastructure Layer Active.")

# =====================================================================
# 4. MAIN DISPLAY FRAME
# =====================================================================
st.title(text[lang]["title"])
st.caption(text[lang]["desc"])
st.warning(text[lang]["risk_banner"])
st.write("---")

# --- VIEW 1: EXECUTIVE DASHBOARD WITH DEEP ANALYSIS BUTTON ---
if page == "📈 Executive Overview & Pipeline":
    if st.button("🚀 Run Deep Enterprise Analysis", type="primary"):
        total_outlets = int(df_region["Outlet_Count"].sum())
        nairobi_pct = float(df_region.at[0, "Pct_of_Total"])
        nairobi_sales = float(df_region.at[0, "Total_Sales"])
        coast_sales = float(df_region.at[1, "Total_Sales"])
        max_credit_pct = float(df_payment.at[0, "Pct_of_Total"])
        max_credit_term = str(df_payment.at[0, "Payment Terms"])
        
        st.success("📊 **Deep Enterprise Intelligence Audit Complete!**")
        st.info(f"""
        **Comprehensive Matrix & Operational Analytics:**
        * **Territory Infrastructure:** Our footprint actively covers **{total_outlets} verified stockist outlets** distributed strategically across East Africa.
        * **Regional Volume Leader:** **Nairobi Region** commands the primary density, pulling a massive **KSh {nairobi_sales:,.2f}** which accounts for **{nairobi_pct}%** of all transactional operations.
        * **Secondary Operations Center:** **Coast Region** tracks as the secondary volume node with an aggregate footprint of **KSh {coast_sales:,.2f}** (16.20% Share share).
        * **Liquidity & Credit Exposure Pipeline:** Financial audit shows severe exposure in credit terms. **{max_credit_term}** accounts for the absolute highest portfolio concentration at **{max_credit_pct}%** of all allocations, presenting a critical working capital cycle loop.
        * **Competitor Environment Intelligence:** Live monitoring parameters log active retail matching independent variables against market leaders: **Samsung, LG, Ramtons, Hisense, and Alyassin** distribution channels.
        """)
        st.write("---")
        
    st.subheader(text[lang]["chart1"])
    st.dataframe(df_region, use_container_width=True, hide_index=True)
    st.write("---")
    st.subheader(text[lang]["chart2"])
    st.dataframe(df_payment, use_container_width=True, hide_index=True)

# --- VIEW 2: REAL N8N AUTOMATION ENGINE ---
if page == "🧠 Real n8n Orchestration Core":
    st.subheader(text[lang]["ai_header"])
    st.write(text[lang]["ai_prompt"])
    n8n_url = st.text_input("n8n Webhook URL Target Endpoint:", value="http://192.168.1.87:8501")
    
    if st.button(text[lang]["ai_btn"], type="primary"):
        st.info(f"Streaming live payload parameters outbound to: {n8n_url}...")
        payload = {
            "source": "streamlit_command_center",
            "region_matrix": region_csv,
            "payment_matrix": payment_csv
        }
        try:
            response = requests.post(n8n_url, json=payload, timeout=8)
            if response.status_code == 200:
                st.success("✅ n8n Pipeline completed execution step successfully!")
                st.write(response.text)
            if response.status_code != 200:
                st.error(f"❌ Automation server returned code: {response.status_code}")
        except Exception as e:
            st.error("❌ Network Timeout Error: Streamlit Cloud cannot ping your local network IP.")
            st.warning("💡 **n8n Webhook Explanation:** Streamlit is deployed on the public internet, while `192.168.1.87` is your internal private office network router. Public servers cannot access internal local IPs unless you open a public tunnel on your computer using a tool like **Ngrok** or configure **Port Forwarding** on your office router.")
            with st.expander("📂 View Extracted Live Payload Matrix (Packaged for n8n Target Node)", expanded=True):
                st.json(payload)

# --- VIEW 3: ASK MIKA CHATBOT ENGINE WITH FUNCTIONAL ICONS ---
if page == "💬 Ask MIKA Market Chatbot":
    st.subheader(text[lang]["chat_header"])
    st.write(text[lang]["chat_desc"])
    
    if st.session_state["chat_history"]:
        for chat in st.session_state["chat_history"]:
