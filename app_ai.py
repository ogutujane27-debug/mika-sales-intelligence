import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import io

# 1. ENTERPRISE SUITE INITIALIZATION
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

# Premium CSS with safe Python percentage parsing for fluid animations
st.markdown("""
    <style>
    @keyframes slideUp { 
        0%% { opacity: 0; transform: translateY(15px); } 
        100%% { opacity: 1; transform: translateY(0); } 
    }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stMetric, .element-container { animation: slideUp 0.5s ease-out forwards; }
    .stButton>button { 
        background-color: #28a745 !important; color: white !important; font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(40,167,69,0.25); border-radius: 6px !important; width: 100%; height: 45px;
        font-size: 16px !important;
    }
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

# 3. SIDEBAR MULTI-PAGE ENGINE
with st.sidebar:
    st.header("⚡ Command Center")
    lang = st.radio("🌐 Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    page = st.radio(
        "Select Dashboard View:" if lang == "English" else "Chagua Mtazamo:",
        ["📈 Executive Overview & Pipeline", "🧠 Simulated n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"]
    )
    st.write("---")
    st.caption("MIKA Automation Infrastructure Layer Active.")

# Localized app dictionary strings (CLEANED FROM PHASE 16/18 LABELS)
text = {
    "English": {
        "title": "🖥️ MIKA Global Enterprise Sales Command Dashboard",
        "desc": "Automated system processing transactional revenue logs and official target metrics independently.",
        "m1": "📦 Total Verified Revenue",
        "m2": "📈 Official Source Target",
        "risk_banner": "⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of sales lack stockist parameters. This is a tracking concern, not an immediate financial loss.",
        "chart1": "🌍 Regional Market Share & Contribution",
        "chart2": "💳 Credit Terms & Liquidity Exposure Pipeline",
        "ai_header": "🧠 Simulated n8n Automation & Audit Engine",
        "ai_prompt": "Activate the simulated backend node pipeline to clean raw records and stream insights.",
        "ai_btn": "🚀 Trigger Local n8n Orchestration Pipeline",
        "ai_idle": "💡 Local n8n Simulator Core: Idle. Pipeline waiting for execution command.",
        "chat_header": "💬 Ask MIKA — Limitless Market Intelligence Chatbot",
        "chat_desc": "Ask any business, competitor (Samsung, LG, Ramtons, Hisense, Alyassin), supply chain, stockout, or market query related to Kenya.",
        "chat_ph": "Type your query here in any language..."
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata mapato ya miamala na vyanzo rasmi vya malengo kando.",
        "m1": "📦 Jumla ya Mapato Yaliyothibitishwa",
        "m2": "📈 Lengo Rasmi la Mauzo",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za stockist. Hili ni tatizo la ufuatiliaji wa data.",
        "ch1": "🌍 Mgawo wa Soko na Mchango wa Mikoa",
        "ch2": "💳 Mzunguko wa Mikopo na Vihatarishi vya Ukwasi",
        "ai_header": "🧠 Mfumo wa Kiotomatiki wa n8n Simulator & Ukaguzi",
        "ai_prompt": "Washa mtiririko wa kiotomatiki wa ndani ili kusafisha kumbukumbu na kumwaga ripoti rasmi.",
        "ai_btn": "🚀 Trigger Local n8n Orchestration Pipeline",
        "ai_idle": "💡 Seva ya n8n Simulator iko tayari. Bonyeza kitufe ili AI isome mifumo ya data.",
        "chat_header": "💬 Uliza MIKA — Chatbot Huru ya Akili ya Soko",
        "chat_desc": "Uliza swali lolote la kibiashara, washindani (Samsung, LG, Ramtons, Hisense), stoo kupungua, au mwenendo wa soko la Kenya.",
        "chat_ph": "Andika swali lako hapa kwa lugha yoyote..."
    }
}

st.title(text[lang]["title"])
st.write(text[lang]["desc"])
st.write("---")

# HIGH-LEVEL EXECUTIVE KPI METRICS
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label=text[lang]["m1"], value="KSh 2.89B", delta="Verified Analytics Active")
with col_m2:
    st.metric(label=text[lang]["m2"], value="KSh 1.68B", delta="Source Target Confirmed")
with col_m3:
    st.metric(label="Stock Tracing Risk" if lang == "English" else "Riski ya Ufuatiliaji", value="89.87%", delta="Data Traceability Gap", delta_color="inverse")
st.write("---")


# ==========================================
# PAGE VIEW 1: EXECUTIVE OVERVIEW & PIPELINE
# ==========================================
if page == "📈 Executive Overview & Pipeline":
    st.warning(text[lang]["risk_banner"])
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader(text[lang]["chart1"])
        fig1 = px.pie(df_region, names="Region Name", values="Total_Sales", hole=0.5,
                      color_discrete_sequence=px.colors.qualitative.Plotly)
        fig1.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_g2:
        st.subheader(text[lang]["chart2"])
        fig2 = px.bar(df_payment, x="Payment Terms", y="Value Exc. VAT", text_auto='.2s',
                      color="Value Exc. VAT", color_continuous_scale="Cividis")
        fig2.update_layout(height=380, showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.write("---")
    st.subheader("📁 Verified Master Region Data Register")
    st.dataframe(df_region, use_container_width=True, hide_index=True)


# ==========================================
# PAGE VIEW 2: FULL-SCREEN SIMULATED n8n ORCHESTRATION PIPELINE
# ==========================================
elif page == "🧠 Simulated n8n Orchestration Core":
    st.subheader(text[lang]["ai_header"])
    st.write(text[lang]["ai_prompt"])
    
    if st.button(text[lang]["ai_btn"]):
        # SIMULATING THE n8n STEP-BY-STEP WORKFLOW STEPS VISUALLY
        status_box = st.empty()
        status_box.info("🔗 [n8n Node 1/4] Triggered: Fetching new raw sales data sheet from system logs...")
        import time
        time.sleep(1)
        
        status_box.info("⚙️ [n8n Node 2/4] Processing: Python engine executing calculations and regional groupings...")
        time.sleep(1)
        
        status_box.info("🧠 [n8n Node 3/4] Groq Core Ingestion: Sending clean parameters to LLM for world-wide business parsing...")
        
        try:
            client = Groq()
            region_summary = df_region.to_string(index=False)
            
            prompt_instructions = f"""
            Perform an executive-level audit business analysis on this corporate dataset for MIKA sales managers.
            Dataset Parameters:
            - Transaction Analysis Total: KSh 2,888,966,390.88 across 266 data rows.
            - Official Target Total: KSh 1,684,717,184.70.
            - Traceability Risk: 89.87% (KSh 2.60B) of entries lack stockist tracking metrics.
            - Regional Log: {region_summary}
            
            Do NOT mention 'Phase 16' or 'Phase 18' in your text! Keep it professional for corporate board.
            Your output must be written completely in {lang}. Use strong, executive formatting.
            Format your presentation into three distinct bold markdown headers:
            1. MANAGEMENT THE WHYS (Operational logic for Nairobi market concentration).
            2. WHAT-IF RISK MITIGATION (Financial liquidity lift in KSh if stockist tracing maps Nairobi's pool).
            3. STRATEGIC AUDIT ACTIONS (3 immediate corporate mandates for the executive board).
            """
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt_instructions}]
            )
            
            status_box.success("✅ [n8n Node 4/4] Success: Board delivery report successfully compiled!")
            st.write("---")
            
            # THE EXECUTIVE READY REPORT (CLEANED)
            ai_report = completion.choices[0].message.content
            st.markdown(ai_report)
            
            # CLEAN EXECUTIVE NOTIFICATION TEXT AREA FOR RECRUITERS / MANAGEMENT
            st.write("---")
            st.subheader("📱 Automated Management Broadcast Alert Payload")
            
            board_alert = (
                "📢 *MIKA AUTOMATED SALES ALERT*\n\n"
                "Dear Directors,\n"
                f"The weekly sales data audit has been compiled successfully via automation.\n\n"
                "💰 *Key Portfolio Performance:*\n"
                "- Total Verified Revenue: KSh 2.89 Billion.\n"
                "- Nairobi Hub Market Share: 49.46% (Dominant Sub-Region).\n\n"
                "⚠️ *Critical Data Tracking Alert:*\n"
                "- 89.87% (KSh 2.60B) of transaction lines currently lack identified stockist data. This requires immediate automation logic mitigation to secure tracing controls.\n\n"
                "🌐 Deployed Control Center: https://streamlit.app"
            )
            
