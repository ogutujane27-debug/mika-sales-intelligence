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
        0%% { opacity: 0; transform: translateY(15px); } 
        100%% { opacity: 1; transform: translateY(0); } 
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

# 3. SIDEBAR MULTI-PAGE ENGINE & LIVE CHAT HISTORY SIDEBAR
with st.sidebar:
    import streamlit as st

# Hakikisha hii ipo juu kabisa ya faili yako
st.set_page_config(layout="wide")

# CSS ya kubadilisha muundo ufanane kabisa na ule wa picha ulizotuma
st.markdown("""
    <style>
        /* Kuondoa nafasi kubwa juu ya sidebar */
        [data-testid="stSidebarNav"] {display: none;}
        
        /* Mtindo wa herufi na rangi za sidebar */
        .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            color: #1a73e8;
            margin-bottom: 25px;
            font-family: 'Google Sans', sans-serif;
        }
        .sidebar-item {
            font-size: 16px;
            padding: 10px 0px;
            color: #3c4043;
            cursor: pointer;
            display: flex;
            align-items: center;
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

# Kujenga Sidebar kama ulivyoomba
with st.sidebar:
    # 1. Jina kuu la mfumo wako
    st.markdown('<div class="sidebar-title">🤖 Mika Chat Bot</div>', unsafe_allow_html=True)
    
    # 2. Vitufe vikuu vya amri (Vinafanana na Google Sidebar)
    if st.button("➕ Mazungumzo mapya", use_container_width=True):
        st.session_state.messages = [] # Inafuta chat ya sasa kuanza mpya
        
    if st.button("🔍 Tafuta mazungumzo", use_container_width=True):
        st.toast("Sehemu ya utafutaji inakuja hivi karibuni!")

    st.markdown('<hr style="margin: 15px 0;">', unsafe_allow_html=True)
    
    # 3. Sehemu ya "Ya hivi majuzi" (Recent History)
    st.markdown('<div class="sidebar-section-title">Ya hivi majuzi</div>', unsafe_allow_html=True)
    
    # Mfano wa list ya historia zako za nyuma (Tengeneza hivi badala ya ile picha ya karatasi)
    recent_chats = [
        "how to use postman tool on my l...",
        "can you outline the differences b...",
        "what's up i'm not getting any fee..."
    ]
    
    for chat in recent_chats:
        if st.button(f"💬 {chat}", key=chat, use_container_width=True):
            st.write(f"Ulichagua: {chat}")

# Sehemu ya data yako (Iliyokuwa na Indentation Error hapo awali)
# Hakikisha mistari hii imekaa bila nafasi za ziada mbele (Perfect Indentation)
st.title("Mika Chat Bot - Dashboard")
if 'df_region' in locals():
    st.dataframe(df_region, use_container_width=True, hide_index=True)

    st.header("⚡ Command Center")
    lang = st.radio("🌐 Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    page = st.radio(
        "Select Dashboard View:" if lang == "English" else "Chagua Mtazamo:",
        ["📈 Executive Overview & Pipeline", "🧠 Simulated n8n Orchestration Core", "💬 Ask MIKA Market Chatbot"]
    )
    st.write("---")
    
    # ⏳ DYNAMIC SIDEBAR HISTORY ENGINE (Looks exactly like Google Browser logs!)
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
                    # Truncate text block to keep it clean and professional
                    short_text = chat["text"][:28] + "..." if len(chat["text"]) > 28 else chat["text"]
                    st.caption(f"🔍 {short_text}")
        st.write("---")
        
    st.caption("MIKA Automation Infrastructure Layer Active.")

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
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za stockist. Hili ni tatizo la ufuatiliaji wa data.",
        "ch1": "🌍 Mgawo wa Soko na Mchango wa Mikoa",
        "ch2": "💳 Mzunguko wa Mikopo na Vihatarishi vya Ukwasi",
        "ai_header": "🧠 Mfumo wa Kiotomatiki wa n8n Simulator & Ukaguzi",
        "ai_prompt": "Washa mtiririko wa kiotomatiki wa ndani ili kusafisha kumbukumbu na kumwaga ripoti rasmi.",
        "ai_btn": "🚀 Trigger Local n8n Orchestration Pipeline",
        "ai_idle": "💡 Seva ya n8n Simulator iko tayari. Bonyeza kitufe ili AI isome mifumo ya data.",
        "chat_header": "💬 Uliza MIKA — Chatbot Huru ya Akili ya Soko",
        "chat_desc": "Uliza swali lolote la kibiashara, washindani (Samsung, LG, Ramtons, Hisense), stoo kupungua, au mwenendo wa soko la Kenya.",
        "chat_ph": "Andika swali lako hapa kisha ubonyeze enter..."
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
    
    st.write("---")
    raw_briefing_text = (
        "MIKA GLOBAL EXECUTIVE SUMMARY\n\n"
        "1. FINANCIAL AUDIT CONTROLS:\n"
        "- Total Verified Operational Revenue Log: KSh 2,888,966,390.88\n"
        "- Official System Sales Target Source: KSh 1,684,717,184.70\n\n"
        "2. RISK EXPOSURE ASSESSMENT:\n"
        "- Market Concentration: Nairobi Region dominates at KSh 1.43B (49.46% of total revenue).\n"
        "- Data Quality Exposure: 89.87% (KSh 2.60B) of transaction lines currently lack stockist data tags."
    )
    
    st.download_button(
        label="📥 Download Executive Briefing" if lang == "English" else "📥 Pakua Muhtasari wa Ripoti",
        data=raw_briefing_text,
        file_name="MIKA_Executive_Management_Briefing.txt",
        mime="text/plain"
    )


# ==========================================
# PAGE VIEW 2: FULL-SCREEN SIMULATED n8n ORCHESTRATION PIPELINE
# ==========================================
elif page == "🧠 Simulated n8n Orchestration Core":
    st.subheader(text[lang]["ai_header"])
    st.write(text[lang]["ai_prompt"])
    
    if st.button(text[lang]["ai_btn"]):
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
            
            prompt_instructions = f"Perform an executive-level audit business analysis on this corporate dataset for MIKA sales managers. Total Revenue: KSh 2.88B. Official Target: KSh 1.68B. Traceability Risk: 89.87%% lack stockist data. Regional Log: {region_summary}. Output must be in {lang}. Format with three headers: 1. MANAGEMENT THE WHYS, 2. WHAT-IF RISK MITIGATION, 3. STRATEGIC AUDIT ACTIONS."
            
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt_instructions}]
            )
            
            status_box.success("✅ [n8n Node 4/4] Success: Board delivery report successfully compiled!")
            st.write("---")
            
            # FILTED: Imeongezewa index ya [0] kuzuia hitilafu ya list object
            ai_report = completion.choices[0].message.content
            st.markdown(ai_report)
            
            st.write("---")
            st.subheader("📱 Automated Management Broadcast Alert Payload")
            
            board_alert = (
                "📢 *MIKA AUTOMATED SALES ALERT*\n\n"
                "Dear Directors,\n"
                "The weekly sales data audit has been compiled successfully via automation.\n\n"
                "💰 *Key Portfolio Performance:*\n"
                "- Total Verified Revenue: KSh 2.89 Billion.\n"
                "- Nairobi Hub Market Share: 49.46%.\n\n"
                "⚠️ *Critical Data Tracking Alert:*\n"
                "- 89.87% lack identified stockist data. Requires immediate automation controls.\n\n"
                "🌐 Deployed Control Center: https://streamlit.app"
            )
            
            st.text_area("📋 Copy-Ready Message Block for WhatsApp / Board Email Broadcast:", value=board_alert, height=210)
            
        except Exception as e:
            st.error(f"AI Server Connection Error: {e}")
    else:
        st.info(text[lang]["ai_idle"])


# ==========================================
# PAGE VIEW 3: DYNAMIC ASK MIKA CHATBOT (CLEAN INTERFACE WITH SIDEBAR HISTORY LOGS)
# ==========================================
else:
    st.subheader(text[lang]["chat_header"])
    st.write(text[lang]["chat_desc"])
    st.write("---")

    # 🛒 PROPER FORM DESIGN WITH INPUT FIELD AND THE '💬 Send Query' BUTTON
    with st.form(key="mika_clean_chat_form", clear_on_submit=True):
        user_input_field = st.text_input(text[lang]["chat_ph"], value="")
        submit_chat_button = st.form_submit_button(
            label="💬 Send Query" if lang == "English" else "💬 Tuma Swali"
        )

    # Core engine triggering on form submission events
    if submit_chat_button and user_input_field:
        with st.spinner("MIKA Core Engine is scanning market variables..."):
            try:
                client = Groq()
                context_prompt = f"You are the MIKA Limitless Corporate Chatbot Core in Kenya. Transaction Revenue KSh 2.89B, Target Total KSh 1.68B. 89.87%% of data lacks stockist info. Competitors in Kenya electronics market: Samsung, LG, Ramtons, Hisense, Alyassin. User query: {user_input_field}. Respond fully and professionally in language: {lang}."
                
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": context_prompt}]
                )
                
                # FILTED: Imeongezewa index ya [0] kuzuia hitilafu ya list object kwenye chatbot pia
                ai_response = completion.choices[0].message.content
                
                # Append exchanges immediately into session arrays so the Sidebar refreshes on the spot!
                st.session_state["chat_history"].append({"role": "user", "text": user_input_field})
                st.session_state["chat_history"].append({"role": "mika", "text": ai_response})
                st.rerun()
                
            except Exception as e:
                st.error(f"Chatbot Communication Failure: {e}")

    # 🌟 RENDER THE CURRENT ACTIVE EXCHANGES DIRECTLY ON THE MAIN VIEW AREA
    if st.session_state["chat_history"]:
        latest_user = st.session_state["chat_history"][-2]["text"]
        latest_mika = st.session_state["chat_history"][-1]["text"]
        
        st.write("---")
        st.markdown(f'<div class="user-bubble"><b>👤 You:</b> {latest_user}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mika-bubble"><b>🤖 MIKA RESPONSE:</b></div>', unsafe_allow_html=True)
        st.markdown(latest_mika)
