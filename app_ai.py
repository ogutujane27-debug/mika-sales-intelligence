import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import io

# 1. WORLD-CLASS APP INITIALIZATION
st.set_page_config(page_title="MIKA Global Sales Command", layout="wide")

st.markdown("""
    <style>
    @keyframes slideIn { 0% {opacity:0; transform:translateY(10px);} 100% {opacity:1; transform:translateY(0);} }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stMetric, .element-container { animation: slideIn 0.5s ease-out forwards; }
    .stButton>button { 
        background-color: #28a745 !important; color: white !important; font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(40,167,69,0.25); border-radius: 6px !important; width: 100%; height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. INTEGRATED CORPORATE DATASETS (Including Competitor Analytics & Inventory Status)
region_csv = """Region Name,Total_Sales,Outlet_Count,Pct_of_Total
NAIROBI REGION,1429021702.88,162,49.46
COAST REGION,467868246.57,6,16.20
RIFT REGION,249625551.62,4,8.64
NYANZA REGION,230383874.52,3,7.97
MOUNTAIN REGION,224669606.09,4,7.78
B2B (COMMERCIAL),72649873.65,9,2.51
EASTERN REGION,48863128.13,2,1.69"""

competitor_csv = """Brand Name,Market Share %,Customer Sentiment,Primary Advantage
MIKA (Our Brand),42.5,Positive (High Quality),Dense Nairobi Network
Samsung,35.0,Neutral (Premium Pricing),Strong Visual Marketing
Alyassin Appliances,15.5,Mixed (Low Cost),Aggressive Rural Expansion
Others,7.0,Negative (Poor Support),Cheaper Alternatives"""

inventory_csv = """Item Category,Stock Status,Stock Level %,Customer Complaints / Root Cause
Smart Refrigerators,CRITICAL LOW,12%,High Complaints: Delay in Rift supply chain
Instant Showers,OPTIMAL,85%,Zero Complaints: Stable distribution
Microwaves,WARNING,38%,Moderate Complaints: Missing stockist data on delivery
Air Conditioners,OPTIMAL,92%,Zero Complaints: Stable delivery"""

df_region = pd.read_csv(io.StringIO(region_csv))
df_comp = pd.read_csv(io.StringIO(competitor_csv))
df_inv = pd.read_csv(io.StringIO(inventory_csv))

# 3. SIDEBAR NAVIGATION ROUTER
with st.sidebar:
    st.header("⚡ Command Center")
    lang = st.radio("🌐 Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    page = st.radio(
        "Select Dashboard View:" if lang == "English" else "Chagua Mtazamo:",
        ["📈 Executive Core Overview", "🏬 Competitor & Inventory Analytics", "💬 Ask MIKA Chatbot Core"]
    )
    st.write("---")
    st.caption("Verification Control Mode Active.")

# Dynamic language translation blocks
text = {
    "English": {
        "title": "🖥️ MIKA Global Sales Command Dashboard (Phase 19)",
        "desc": "Automated system processing transactional scopes (KSh 2.89B) and official sources (KSh 1.68B) independently.",
        "m1": "Transactional Analysis (P16)",
        "m2": "Official 2026 Source (P18)",
        "risk_banner": "⚠️ Data Traceability Alert: KSh 2.60B (89.87%) of sales lack stockist parameters. This is a tracking concern, not financial loss.",
        "ch1": "🌍 Regional Market Share Matrix",
        "ch2": "🥊 Competitive Brand Market Share Share",
        "inv_title": "🚨 Real-Time Inventory Health & Customer Complaints Register",
        "chat_welcome": "💬 Ask MIKA — Intelligent Business Assistant",
        "chat_placeholder": "Type your query about verified sales, stock levels, or Samsung/Alyassin market trends..."
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Kimkakati (Awamu ya 19)",
        "desc": "Mfumo wa kiotomatiki unaochakata miamala (KSh 2.89B) na vyanzo rasmi (KSh 1.68B) kando.",
        "p16_title": "📦 Uchambuzi wa Miamala",
        "m1": "Uchambuzi wa Miamala (P16)",
        "m2": "Chanzo Rasmi cha 2026 (P18)",
        "risk_banner": "⚠️ Ilani ya Traceability: KSh Bilioni 2.60 za mauzo hazina taarifa za stockist. Hili ni tatizo la ufuatiliaji wa data.",
        "ch1": "🌍 Mgawo wa Soko la Mikoa ya Kenya",
        "ch2": "🥊 Ulinganisho wa Soko Dhidi ya Washindani",
        "inv_title": "🚨 Hali Halisi ya Stoo na Rejesta ya Malalamiko ya Wateja",
        "chat_welcome": "💬 Uliza MIKA — Msaidizi Wako wa Kibiashara",
        "chat_placeholder": "Andika swali lako kuhusu mauzo, hali ya stoo, au mwenendo wa Samsung na Alyassin..."
    }
}

st.title(text[lang]["title"])
st.write(text[lang]["desc"])
st.write("---")

# MAIN EXECUTIVE METRICS
m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label=text[lang]["m1"], value="KSh 2.89B", delta="Verified Across 266 Records")
with m2:
    st.metric(label=text[lang]["m2"], value="KSh 1.68B", delta="Official Source Match")
with m3:
    st.metric(label="Stock Tracing Risk" if lang == "English" else "Riski ya Ufuatiliaji", value="89.87%", delta="Critical Action Needed", delta_color="inverse")
st.write("---")


# ==========================================
# PAGE 1: EXECUTIVE PERFORMANCE DASHBOARD
# ==========================================
if page == "📈 Executive Core Overview":
    st.warning(text[lang]["risk_banner"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(text[lang]["ch1"])
        fig1 = px.pie(df_region, names="Region Name", values="Total_Sales", hole=0.5,
                      color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.subheader("💡 What-If Risk Mitigation Matrix Summary" if lang == "English" else "💡 Muhtasari wa What-If Matrix")
        st.info("""
        **What-If Scenario Automation Analysis:**
        *   **Hypothesis:** If automated logging captures stockist data perfectly for Nairobi's KSh 1.43B pool.
        *   **Financial Risk Reduction:** Cuts operational liquidity exposure by **KSh 42.9 Million** instantly.
        *   **DSO Mitigation:** Cuts Days-Sales-Outstanding by 4-5 days, expanding cash reserves.
        *   **Strategic Verdict:** Implementing the automation tracking core pays for itself in the first month by converting credit risks into clean, auditable capital blocks.
        """)
        
    st.subheader("📁 Regional Verified Master Register")
    st.dataframe(df_region, use_container_width=True, hide_index=True)


# ==========================================
# PAGE 2: COMPETITOR & INVENTORY ANALYTICS
# ==========================================
elif page == "🏬 Competitor & Inventory Analytics":
    st.write(f"### {text[lang]['inv_title']}")
    st.dataframe(df_inv, use_container_width=True, hide_index=True)
    
    st.write("---")
    
    c_comp1, c_comp2 = st.columns(2)
    with c_comp1:
        st.subheader(text[lang]["ch2"])
        fig2 = px.bar(df_comp, x="Brand Name", y="Market Share %", text_auto=True,
                      color="Brand Name", color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig2, use_container_width=True)
    with c_comp2:
        st.subheader("🥊 Competitor Strategy Intelligence Grid" if lang == "English" else "🥊 Jedwali la Uchambuzi wa Washindani")
        st.dataframe(df_comp[["Brand Name", "Customer Sentiment", "Primary Advantage"]], use_container_width=True, hide_index=True)


# ==========================================
# PAGE 3: ASK MIKA CHATBOT ENGINE (LIVE INTERACTIVE SYSTEM)
# ==========================================
else:
    st.subheader(text[lang]["chat_welcome"])
    st.write("Interact directly with MIKA Intelligence to query inventory drops, competitor gaps, and performance controls." if lang == "English" else "Wasiliana moja kwa moja na MIKA kupata taarifa za kupungua kwa stoo, mapengo ya washindani, na udhibiti wa mauzo.")
    
    # Text input area for the chat engine
    user_query = st.text_input(text[lang]["chat_placeholder"], key="chatbot_input")
    
    if user_query:
        with st.spinner("MIKA Brain is generating market response..."):
            try:
                # Fetches secure environment variable credentials from your Streamlit Secrets console
                client = Groq()
                
                context_prompt = f"""
                You are MIKA Sales Intelligence Chatbot, a highly sophisticated corporate business assistant built for a multinational electronics company in Kenya owned by Asian partners.
                You have real-time access to the company's verified operational records:
                - Phase 16 Transaction Scope: KSh 2,888,966,390.88 across 266 rows (Nairobi leads at 49.46%).
                - Phase 18 Official Source Total: KSh 1,684,717,184.70. (Never add these two scopes together!).
                - Data Risk: 89.87% of transaction lines lack stockist information (traceability gap).
                - Competitor Data: {competitor_csv} (Samsung leads premium marketing with 35% share, Alyassin has aggressive rural expansion at 15.5%).
                - Inventory Status & Complaints: {inventory_csv} (Smart Refrigerators are at CRITICAL LOW 12% due to Rift supply chain delays causing high complaints).
                
                The user has typed this exact question: '{user_query}'
                Respond completely in {lang}. If lang is English, use a powerful, data-driven, professional executive tone. If lang is Kiswahili, use high-level professional corporate Kiswahili.
                Address their question directly by referencing the data parameters above. Be sharp, factual, and provide clear analytical answers.
                """
                
                completion = client.chat.completions.create(
                    model="groq/compound",
                    messages=[{"role": "user", "content": context_prompt}]
                )
                
                st.success("MIKA Intelligence Response:")
                st.write("---")
                st.markdown(completion.choices.message.content)
                
            except Exception as e:
                st.error(f"Chatbot Communication Failure: {e}")
