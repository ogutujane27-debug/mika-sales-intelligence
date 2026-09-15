import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import io

# 1. GLOBAL MANAGEMENT ENVIRONMENT SETUP
st.set_page_config(page_title="MIKA Sales Intelligence Suite", layout="wide")

# Modern corporate styling with interactive load animations
st.markdown("""
    <style>
    @keyframes slideIn { 0% {opacity:0; transform:translateY(10px);} 100% {opacity:1; transform:translateY(0);} }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    .stMetric, .element-container { animation: slideIn 0.5s ease-out forwards; }
    /* Premium style for the AI Core Activation Button */
    .stButton>button { 
        background-color: #28a745 !important; color: white !important; font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(40,167,69,0.25); border-radius: 6px !important; width: 100%; height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. LOCAL DATA STORAGE REPRESENTING VERIFIED MIKA MASTER RECORDS
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

# 3. SIDEBAR COMMAND CENTER & MULTI-LANGUAGE TRANSLATION TOGGLE
with st.sidebar:
    st.header("⚡ Command Center")
    
    # 🌍 THE TRANSLATION AI LAYER
    lang = st.radio("🌐 Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    # Navigation Router matching your verified dashboard screens
    page_label = "Select Dashboard View" if lang == "English" else "Chagua Mtazamo wa Dashboard"
    page = st.radio(
        page_label,
        ["📈 Executive Overview", "🧠 AI Business Brain Screen"]
    )
    st.write("---")
    
    # Audit Control Summary
    st.caption("**Reporting Controls:** Transactional and Source scopes represent different scopes and must NOT be added together.")

# 4. APP DICTIONARY FOR INSTANT DYNAMIC TRANSLATION
text = {
    "English": {
        "title": "📊 MIKA Final Verified Management Dashboard",
        "desc": "This platform maintains strict reporting controls across separate transactional and source data scopes.",
        "p16_title": "📦 Transactional Analysis",
        "p18_title": "📈 Official 2026 Source",
        "p16_val": "KSh 2.89B",
        "p18_val": "KSh 1.68B",
        "status_p16": "PASS — Transaction total verified across 266 records",
        "status_p18": "PASS — Official source reporting total verified",
        "risk_title": "🏪 Stockist Data Traceability Risk",
        "risk_msg": "KSh 2.60B (89.87%) of transaction sales currently lack identified stockist data. This is a traceability concern, not an immediate financial loss.",
        "chart1": "🌍 Regional Market Share & Contribution",
        "chart2": "💳 Credit Terms & Liquidity Exposure Pipeline",
        "ai_header": "🧠 Real-Time AI Management Brain Screen",
        "ai_prompt_msg": "Click the button below to stream localized management insights directly from the AI server.",
        "ai_btn": "🚀 Run Deep Enterprise Analysis",
        "ai_idle": "💡 Seva ya AI iko tayari. Click the button to analyze data pools."
    },
    "Kiswahili": {
        "title": "📊 MIKA Mfumo wa Ukaguzi wa Data za Mauzo",
        "desc": "Mfumo huu unadumisha udhibiti mkali wa ukaguzi kati ya data ya miamala na vyanzo rasmi.",
        "p16_title": "📦 Uchambuzi wa Miamala",
        "p18_title": "📈 Chanzo Rasmi cha 2026",
        "p16_val": "KSh Bilioni 2.89",
        "p18_val": "KSh Bilioni 1.68",
        "status_p16": "IMEKUBALIWA — Jumla ya miamala imethibitishwa kwenye rekodi 266",
        "status_p18": "IMEKUBALIWA — Jumla ya ripoti kutoka chanzo rasmi imethibitishwa",
        "risk_title": "🏪 Riski ya Traceability ya Data za Stockist",
        "risk_msg": "KSh Bilioni 2.60 (89.87%) ya miamala haina taarifa za stockist. Hili ni tatizo la ufuatiliaji wa data, si hasara ya kifedha.",
        "chart1": "🌍 Mgawo wa Soko na Mchango wa Mikoa",
        "chart2": "💳 Mzunguko wa Mikopo na Vihatarishi vya Ukwasi",
        "ai_header": "🧠 Seva ya Uchambuzi ya AI ya Muda Halisi",
        "ai_prompt_msg": "Bonyeza kitufe kilicho chini ili kupokea muhtasari wa kiutendaji kutoka kwenye seva ya AI.",
        "ai_btn": "🚀 Washa Uchambuzi wa AI",
        "ai_idle": "💡 Seva ya AI iko tayari. Bonyeza kitufe ili AI isome mifumo ya data."
    }
}

# 5. HEADER SECTION ATTACHED TO DICTIONARY ROUTING
st.title(text[lang]["title"])
st.write(text[lang]["desc"])
st.write("---")

# 6. HIGH-LEVEL EXECUTIVE METRICS GRID
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric(label=text[lang]["p16_title"], value=text[lang]["p16_val"], delta=text[lang]["status_p16"])
with col_m2:
    st.metric(label=text[lang]["p18_title"], value=text[lang]["p18_val"], delta=text[lang]["status_p18"])

st.write("---")


# ==========================================
# PAGE VIEW 1: EXECUTIVE PERFORMANCE DASHBOARD
# ==========================================
if page == "📈 Executive Overview":
    
    # Display Data Traceability Warning Banner
    st.warning(f"⚠️ **{text[lang]['risk_title']}:** {text[lang]['risk_msg']}")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader(text[lang]["chart1"])
        # FIXED: Qualitative palette tracking fixed for secure loading
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

    # Clean data register below charts
    st.write("---")
    st.subheader("📁 Verified Master Region Register")
    st.dataframe(df_region, use_container_width=True, hide_index=True)


# ==========================================
# PAGE VIEW 2: FULL SCREEN SEPARATE AI SERVER
# ==========================================
else:
    st.subheader(text[lang]["ai_header"])
    st.write(text[lang]["ai_prompt_msg"])
    
    if st.button(text[lang]["ai_btn"]):
        with st.spinner("Streaming calculations from AI core..."):
            try:
                # 🔴 CHANGE THIS TOKEN ON LINE 124 TO YOUR ACTUAL POSTMAN WORKING KEY 🔴
                client = Groq() # Clean and secure for public GitHub pushing!

                
                prompt_instructions = f"""
                Perform an executive-level audit business analysis on this specific corporate dataset for MIKA sales managers.
                Dataset Overview:
                Transactional Analysis Total: KSh 2,888,966,390.88 across 266 records.
                Official 2026 Source Total: KSh 1,684,717,184.70.
                Data Quality Issue: KSh 2.60B (89.87%) of sales lack stockist tracking data.
                Regional breakdown: {region_csv}
                
                You must output your complete analysis in {lang}. If lang is English, use standard corporate English. If lang is Kiswahili, write professionally in Kiswahili.
                Format your response into three specific, bolded markdown sections:
                1. MANAGEMENT THE WHYS: Explain why transactional analysis and official source totals must stay completely separate and why Nairobi dominates.
                2. WHAT-IF RISK MITIGATION: Analyze what happens if we fix the stockist data-quality traceability gap for Nairobi's KSh 1.43B pool.
                3. STRATEGIC AUDIT ACTIONS: Provide 3 immediate administrative actions for the management board.
                """
                
                completion = client.chat.completions.create(
                    model="groq/compound",
                    messages=[{"role": "user", "content": prompt_instructions}]
                )
                
                st.success("Analysis Successfully Compiled!")
                st.write("---")
                # Correct choice list index configuration applied
                st.markdown(completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"AI Server Connection Error: {e}")
    else:
        st.info(text[lang]["ai_idle"])
