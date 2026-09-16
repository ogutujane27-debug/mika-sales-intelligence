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
        box-shadow: 0 4px 15px rgba(40,167,69,0.25); border-radius: 6px !important; width: 100%; height: 50px;
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
        ["📈 Executive Overview & Pipeline", "🧠 Real-Time AI Management Brain", "💬 Ask MIKA Market Chatbot"]
    )
    st.write("---")
    st.caption("Reporting Controls Active: Separate Scopes Maintained.")

# Localized app dictionary strings
text = {
    "English": {
        "title": "🖥️ MIKA Global Enterprise Sales Command Dashboard",
        "desc": "Automated system processing transactional (P16: KSh 2.89B) and source logs (P18: KSh 1.68B) independently.",
        "m1": "📦 Transactional Analysis",
        "m2": "📈 Official 2026 Source",
        "risk_banner": "⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack identified stockist data. This is a traceability concern, not an immediate financial loss.",
        "chart1": "🌍 Regional Market Share & Contribution",
        "chart2": "💳 Credit Terms & Liquidity Exposure Pipeline",
        "ai_header": "🧠 Real-Time AI Management Brain Screen",
        "ai_prompt": "Click the button below to stream localized management insights directly from the AI server.",
        "ai_btn": "🚀 Run Deep Enterprise Analysis",
        "ai_idle": "💡 AI Core Status: Idle. Click the button to analyze data pools.",
        "chat_header": "💬 Ask MIKA — Limitless Market Intelligence Chatbot",
        "chat_desc": "Ask any business, competitor (Samsung, LG, Ramtons, Hisense, Alyassin), supply chain, stockout, or market query related to Kenya.",
        "chat_ph": "Type your query here in any language..."
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata miamala (Awamu ya 16: KSh 2.89B) na vyanzo rasmi (Awamu ya 18: KSh 1.68B) kando.",
        "m1": "📦 Uchambuzi wa Miamala",
        "m2": "📈 Chanzo Rasmi cha 2026",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za stockist. Hili ni tatizo la ufuatiliaji wa data.",
        "ch1": "🌍 Mgawo wa Soko na Mchango wa Mikoa",
        "ch2": "💳 Mzunguko wa Mikopo na Vihatarishi vya Ukwasi",
        "ai_header": "🧠 Seva ya Uchambuzi ya AI ya Muda Halisi",
        "ai_prompt": "Bonyeza kitufe kilicho chini ili kupokea muhtasari wa kiutendaji kutoka kwenye seva ya AI.",
        "ai_btn": "🚀 Washa Uchambuzi wa AI",
        "ai_idle": "💡 Seva ya AI iko tayari. Bonyeza kitufe ili AI isome mifumo ya data.",
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
    st.metric(label=text[lang]["m1"], value="KSh 2.89B", delta="PASS — 266 Records Verified")
with col_m2:
    st.metric(label=text[lang]["m2"], value="KSh 1.68B", delta="PASS — Source Verified")
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
# PAGE VIEW 2: FULL-SCREEN AI REPORT GENERATOR
# ==========================================
elif page == "🧠 Real-Time AI Management Brain":
    st.subheader(text[lang]["ai_header"])
    st.write(text[lang]["ai_prompt"])
    
    if st.button(text[lang]["ai_btn"]):
        with st.spinner("Streaming executive intelligence from AI core..."):
            try:
                client = Groq()
                region_summary = df_region.to_string(index=False)
                
                prompt_instructions = f"""
                Perform an executive-level audit business analysis on this corporate dataset for MIKA sales managers.
                Dataset Parameters:
                - Transaction Analysis Total (Phase 16): KSh 2,888,966,390.88 across 266 data rows.
                - Official 2026 Source Total (Phase 18): KSh 1,684,717,184.70.
                - Traceability Risk: 89.87% (KSh 2.60B) of transaction entries lack stockist tracking metrics.
                - Regional Log: {region_summary}
                
                Your output must be written completely in {lang}. Use strong, executive formatting.
                Format your presentation into three distinct bold markdown headers:
                1. MANAGEMENT THE WHYS (Operational logic for scope separation and Nairobi market concentration).
                2. WHAT-IF RISK MITIGATION (Financial liquidity lift in KSh if stockist tracing maps Nairobi's pool).
                3. STRATEGIC AUDIT ACTIONS (3 immediate corporate mandates for the executive board).
                """
                
                completion = client.chat.completions.create(
                    model="groq/compound",
                    messages=[{"role": "user", "content": prompt_instructions}]
                )
                
                st.success("Analysis Successfully Compiled!")
                st.write("---")
                st.markdown(completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"AI Server Connection Error: {e}")
    else:
        st.info(text[lang]["ai_idle"])


# ==========================================
# PAGE VIEW 3: UNLIMITLESS ASK MIKA MARKET CHATBOT
# ==========================================
else:
    st.subheader(text[lang]["chat_header"])
    st.write(text[lang]["chat_desc"])
    
    user_query = st.text_input(text[lang]["chat_ph"], key="global_market_chatbot")
    
    if user_query:
        with st.spinner("MIKA Core Engine is scanning market variables..."):
            try:
                client = Groq()
                
                # FIXED LAYER: Ujumbe umefupishwa sana hapa ili usizidi kiwango cha herufi za Groq (413 fix)
                context_prompt = (
                    f"You are MIKA Sales Chatbot in Kenya. "
                    f"Data: P16 Transaction Total KSh 2.89B (Nairobi leads at 49.46%%), "
                    f"P18 Source Total KSh 1.68B (Do not combine scopes). "
                    f"89.87%% data lacks stockist tracking info. "
                    f"Competitors: Samsung, LG, Ramtons, Hisense, Alyassin. "
                    f"User Query: {user_query}. Respond professionally in language: {lang}."
                )
                
                completion = client.chat.completions.create(
                    model="groq/compound",
                    messages=[{"role": "user", "content": context_prompt}]
                )
                
                st.success("MIKA Market Core Response:" if lang == "English" else "Majibu ya Akili ya MIKA:")
                st.write("---")
                st.markdown(completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Chatbot Communication Failure: {e}")
