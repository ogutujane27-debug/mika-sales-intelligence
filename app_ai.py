
App · PY
import streamlit as st
import pandas as pd
import plotly.express as px
import io
import os
import requests
 
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
 
# =====================================================================
# 1. ENTERPRISE SUITE INITIALIZATION & PREMIUM CSS STYLING
# =====================================================================
st.set_page_config(
    page_title="MIKA Global Market Intelligence",
    layout="wide"
)
 
st.markdown("""
<style>
@keyframes slideUp {
    0% { opacity: 0; transform: translateY(15px); }
    100% { opacity: 1; transform: translateY(0); }
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
[data-testid="stSidebarNav"] {
    display: none;
}
.stButton > button {
    background-color: #28a745 !important;
    color: white !important;
    font-weight: bold !important;
    box-shadow: 0 4px 15px rgba(40,167,69,0.25);
    border-radius: 6px !important;
    width: 100%;
    min-height: 45px;
}
.stDownloadButton > button {
    background-color: #007bff !important;
    color: white !important;
    font-weight: bold !important;
    box-shadow: 0 4px 15px rgba(0,123,255,0.25);
    border-radius: 6px !important;
    width: 100%;
    min-height: 45px;
}
.user-bubble {
    background-color: #e2f0d9;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    color: #1e3d14;
    font-family: sans-serif;
}
.mika-bubble {
    background-color: #f1f1f1;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 15px;
    border-left: 5px solid #28a745;
    color: #222222;
    font-family: sans-serif;
}
</style>
""", unsafe_allow_html=True)
 
# =====================================================================
# 2. CORPORATE DATA MATRIX
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
 
# Top-line reporting totals (kept separate on purpose — transactional vs.
# official-source scopes must never be summed together).
TRANSACTIONAL_TOTAL = 2_888_966_390.88
TRANSACTIONAL_RECORDS = 266
OFFICIAL_SOURCE_TOTAL = 1_684_717_184.70
UNTRACKED_STOCKIST_PCT = 89.87
UNTRACKED_STOCKIST_VALUE = 2_600_000_000  # KSh 2.60B, as reported
 
# =====================================================================
# 3. SESSION STATE
# =====================================================================
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
 
if "enterprise_analysis_run" not in st.session_state:
    st.session_state["enterprise_analysis_run"] = False
 
if "n8n_last_response" not in st.session_state:
    st.session_state["n8n_last_response"] = None
 
# =====================================================================
# 4. LANGUAGE DICTIONARY
# =====================================================================
text = {
    "English": {
        "title": "🖥️ MIKA Global Enterprise Sales Command Dashboard",
        "desc": "Automated system processing transactional revenue logs and official target metrics independently.",
        "m1": "📦 Total Transactional Revenue",
        "m2": "📈 Official Source Total",
        "m1_status": f"{TRANSACTIONAL_RECORDS} records verified",
        "m2_status": "Statutory / audited scope",
        "risk_banner": "⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack identified stockist data. This is a tracking concern, not an immediate financial loss.",
        "chart1": "🌍 Regional Market Share & Contribution",
        "chart2": "💳 Credit Terms & Liquidity Exposure Pipeline",
        "nav_label": "Select Dashboard View:",
        "pages": [
            "📈 Executive Overview & Pipeline",
            "🧠 AI Business Brain (Groq)",
            "🔌 Real n8n Orchestration Core",
            "💬 Ask MIKA Market Chatbot",
        ],
        "ai_header": "🧠 Real-Time AI Management Brain Screen",
        "ai_prompt_msg": "Click the button below to stream localized management insights directly from the AI server.",
        "ai_btn": "🚀 Run Deep Enterprise Analysis (AI)",
        "ai_idle": "💡 AI service ready. Click the button to analyze the data pools.",
        "n8n_header": "🔌 Real n8n Orchestration Core Engine",
        "n8n_prompt": "Enter your active n8n webhook endpoint to send the enterprise intelligence payload into your workflow.",
        "n8n_btn": "🚀 Execute Live n8n Pipeline",
        "n8n_idle": "💡 Real n8n Connection Core: Waiting for outbound execution trigger input.",
        "n8n_input_label": "n8n Webhook URL",
        "n8n_sent": "✅ Payload sent successfully.",
        "n8n_error": "❌ Could not reach the n8n webhook.",
        "chat_header": "💬 Ask MIKA — Market Intelligence Chatbot",
        "chat_desc": "Ask any business, competitor (Samsung, LG, Ramtons, Hisense, Alyassin), supply chain, stockout, or market query related to Kenya.",
        "chat_ph": "Type your query here and press enter...",
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata mapato ya miamala na vyanzo rasmi vya malengo kando.",
        "m1": "📦 Jumla ya Mapato ya Miamala",
        "m2": "📈 Jumla ya Chanzo Rasmi",
        "m1_status": f"Rekodi {TRANSACTIONAL_RECORDS} zimethibitishwa",
        "m2_status": "Wigo rasmi / uliokaguliwa",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 (89.87%) za miamala hazina taarifa za wauzaji maalum. Hili ni suala la ufuatiliaji, sio upotezaji wa kifedha wa haraka.",
        "chart1": "🌍 Uchangiaji wa Mauzo Kimkoa",
        "chart2": "💳 Masharti ya Malipo na Hali ya Ukwasi",
        "nav_label": "Chagua Mtazamo wa Dashboard:",
        "pages": [
            "📈 Muhtasari wa Utendaji",
            "🧠 Ubongo wa AI (Groq)",
            "🔌 Mtambo wa n8n (Live)",
            "💬 Uliza MIKA Chatbot",
        ],
        "ai_header": "🧠 Seva ya Uchambuzi ya AI ya Muda Halisi",
        "ai_prompt_msg": "Bonyeza kitufe kilicho chini ili kupokea muhtasari wa kiutendaji kutoka kwenye seva ya AI.",
        "ai_btn": "🚀 Washa Uchambuzi wa AI",
        "ai_idle": "💡 Seva ya AI iko tayari. Bonyeza kitufe ili AI isome mifumo ya data.",
        "n8n_header": "🔌 Mitambo ya Kiotomatiki wa n8n (Live)",
        "n8n_prompt": "Weka anwani halisi ya webhook ya n8n ili kutuma data ya biashara kwenye workflow yako.",
        "n8n_btn": "🚀 Washa n8n Pipeline ya Ukweli",
        "n8n_idle": "💡 Mfumo wa n8n: Unasubiri amri yako ya kuwasha workflow.",
        "n8n_input_label": "Anwani ya Webhook ya n8n",
        "n8n_sent": "✅ Data imetumwa kikamilifu.",
        "n8n_error": "❌ Imeshindikana kufikia webhook ya n8n.",
        "chat_header": "💬 Uliza MIKA — Chatbot ya Ujasusi wa Soko",
        "chat_desc": "Uliza kuhusu biashara, washindani, usambazaji, stockout, au soko la Kenya.",
        "chat_ph": "Andika swali lako hapa na ubonyeze enter...",
    },
}
 
# Use a plain (non-agentic) Groq model everywhere. "groq/compound" runs its
# own hidden web-search/tool-use steps, which can balloon the actual request
# size Groq has to process and trigger a 413 "request_too_large" error even
# for a short question.
GROQ_MODEL = "llama-3.3-70b-versatile"
 
# =====================================================================
# 5. HELPERS
# =====================================================================
def get_groq_api_key():
    """Pull the Groq key from Streamlit secrets first, then env var.
    Never hardcode a real key in source — it ends up in git history
    and any public repo."""
    key = None
    if hasattr(st, "secrets"):
        try:
            key = st.secrets["GROQ_API_KEY"]
        except Exception:
            key = None
    if not key:
        key = os.environ.get("GROQ_API_KEY")
    return key
 
 
def build_dataset_summary():
    """Compute the live figures used across the AI / chatbot prompts,
    so the narrative always matches whatever is in df_region/df_payment."""
    total_outlets = int(df_region["Outlet_Count"].sum())
    nairobi_row = df_region.iloc[0]
    coast_row = df_region.iloc[1]
    max_credit_row = df_payment.loc[df_payment["Value Exc. VAT"].idxmax()]
    return {
        "total_outlets": total_outlets,
        "nairobi_row": nairobi_row,
        "coast_row": coast_row,
        "max_credit_row": max_credit_row,
    }
 
 
# =====================================================================
# 6. SIDEBAR MULTI-PAGE ENGINE
# =====================================================================
with st.sidebar:
    st.header("⚡ Command Center")
 
    lang = st.radio(
        "🌐 Language / Lugha:",
        ["English", "Kiswahili"],
        horizontal=True,
    )
 
    st.write("---")
 
    page = st.radio(text[lang]["nav_label"], text[lang]["pages"])
 
    st.write("---")
    st.caption("MIKA Automation Infrastructure Layer Active.")
 
# =====================================================================
# 7. MAIN DISPLAY FRAME
# =====================================================================
st.title(text[lang]["title"])
st.caption(text[lang]["desc"])
st.warning(text[lang]["risk_banner"])
 
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric(
        label=text[lang]["m1"],
        value=f"KSh {TRANSACTIONAL_TOTAL:,.2f}",
        delta=text[lang]["m1_status"],
    )
with col_m2:
    st.metric(
        label=text[lang]["m2"],
        value=f"KSh {OFFICIAL_SOURCE_TOTAL:,.2f}",
        delta=text[lang]["m2_status"],
    )
 
st.write("---")
 
pages = text[lang]["pages"]
 
# =====================================================================
# VIEW 1: EXECUTIVE OVERVIEW & PIPELINE
# =====================================================================
if page == pages[0]:
 
    if st.button("🚀 Run Deep Enterprise Analysis", type="primary", key="deep_enterprise_analysis"):
        summary = build_dataset_summary()
        nairobi_row = summary["nairobi_row"]
        coast_row = summary["coast_row"]
        max_credit_row = summary["max_credit_row"]
 
        st.session_state["enterprise_analysis_run"] = True
        st.success("📊 Enterprise Intelligence Audit Complete!")
 
        st.info(
            f"""
**Comprehensive Matrix & Operational Analytics:**
 
* **Territory Infrastructure:** Our footprint actively covers **{summary['total_outlets']} verified stockist outlets** distributed strategically across Kenya.
* **Regional Volume Leader:** {nairobi_row['Region Name'].title()} commands the primary density, pulling **KSh {nairobi_row['Total_Sales']:,.2f}**, accounting for **{nairobi_row['Pct_of_Total']}%** of all transactional operations.
* **Secondary Operations Center:** {coast_row['Region Name'].title()} tracks as the secondary volume node with **KSh {coast_row['Total_Sales']:,.2f}** ({coast_row['Pct_of_Total']}% share).
* **Liquidity & Credit Exposure Pipeline:** **{max_credit_row['Payment Terms']}** accounts for the highest portfolio concentration at **{max_credit_row['Pct_of_Total']}%** of all allocations — a critical working-capital cycle to monitor.
* **Competitor Environment:** Positioning is tracked against market leaders Samsung, LG, Ramtons, Hisense, and Alyassin.
"""
        )
 
    st.write("---")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader(text[lang]["chart1"])
        fig1 = px.pie(
            df_region, names="Region Name", values="Total_Sales", hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )
        fig1.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig1, use_container_width=True)
 
    with col_g2:
        st.subheader(text[lang]["chart2"])
        fig2 = px.bar(
            df_payment, x="Payment Terms", y="Value Exc. VAT", text_auto=".2s",
            color="Value Exc. VAT", color_continuous_scale="Cividis",
        )
        fig2.update_layout(height=380, showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig2, use_container_width=True)
 
    st.write("---")
    st.subheader("📁 Verified Master Region Register")
    st.dataframe(df_region, use_container_width=True, hide_index=True)
    st.subheader("📁 Payment Terms Register")
    st.dataframe(df_payment, use_container_width=True, hide_index=True)
 
# =====================================================================
# VIEW 2: AI BUSINESS BRAIN (GROQ)
# =====================================================================
elif page == pages[1]:
    st.subheader(text[lang]["ai_header"])
    st.write(text[lang]["ai_prompt_msg"])
 
    if not GROQ_AVAILABLE:
        st.error("The `groq` package isn't installed. Run: pip install groq")
    elif st.button(text[lang]["ai_btn"]):
        with st.spinner("Streaming calculations from AI core..."):
            try:
                groq_api_key = get_groq_api_key()
                if not groq_api_key:
                    st.error(
                        "No Groq API key found. Add GROQ_API_KEY to "
                        ".streamlit/secrets.toml (locally) or your app's Secrets "
                        "(Streamlit Cloud), or set it as an environment variable."
                    )
                    st.stop()
 
                client = Groq(api_key=groq_api_key)
                summary = build_dataset_summary()
 
                prompt_instructions = f"""
                Perform an executive-level audit business analysis on this specific corporate dataset for MIKA sales managers.
                Dataset Overview:
                Transactional Analysis Total: KSh {TRANSACTIONAL_TOTAL:,.2f} across {TRANSACTIONAL_RECORDS} records.
                Official Source Total: KSh {OFFICIAL_SOURCE_TOTAL:,.2f}.
                Data Quality Issue: KSh {UNTRACKED_STOCKIST_VALUE:,.0f} ({UNTRACKED_STOCKIST_PCT}%) of sales lack stockist tracking data.
                Total verified stockist outlets: {summary['total_outlets']}.
                Regional breakdown: {region_csv}
                Payment terms breakdown: {payment_csv}
 
                You must output your complete analysis in {lang}. If lang is English, use standard corporate English. If lang is Kiswahili, write professionally in Kiswahili.
                Format your response into three specific, bolded markdown sections:
                1. MANAGEMENT THE WHYS: Explain why transactional analysis and official source totals must stay completely separate and why Nairobi dominates.
                2. WHAT-IF RISK MITIGATION: Analyze what happens if we fix the stockist data-quality traceability gap for Nairobi's sales pool.
                3. STRATEGIC AUDIT ACTIONS: Provide 3 immediate administrative actions for the management board.
                """
 
                completion = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt_instructions}],
                )
 
                st.success("Analysis Successfully Compiled!")
                st.write("---")
                st.markdown(completion.choices[0].message.content)
 
            except Exception as e:
                if "request_too_large" in str(e) or "413" in str(e):
                    st.error(
                        "⚠️ That request was too large for the AI service to process. "
                        "Try again — this can happen occasionally with larger prompts."
                    )
                else:
                    st.error(f"AI Server Connection Error: {e}")
    else:
        st.info(text[lang]["ai_idle"])
 
# =====================================================================
# VIEW 3: REAL N8N ORCHESTRATION CORE
# =====================================================================
elif page == pages[2]:
    st.subheader(text[lang]["n8n_header"])
    st.write(text[lang]["n8n_prompt"])
 
    webhook_url = st.text_input(text[lang]["n8n_input_label"], placeholder="https://your-n8n-instance/webhook/...")
 
    if st.button(text[lang]["n8n_btn"]):
        if not webhook_url:
            st.error("Please enter a valid n8n webhook URL first.")
        else:
            summary = build_dataset_summary()
            payload = {
                "transactional_total": TRANSACTIONAL_TOTAL,
                "transactional_records": TRANSACTIONAL_RECORDS,
                "official_source_total": OFFICIAL_SOURCE_TOTAL,
                "untracked_stockist_pct": UNTRACKED_STOCKIST_PCT,
                "total_outlets": summary["total_outlets"],
                "region_breakdown": df_region.to_dict(orient="records"),
                "payment_terms_breakdown": df_payment.to_dict(orient="records"),
                "language": lang,
            }
            with st.spinner("Sending payload to n8n..."):
                try:
                    response = requests.post(webhook_url, json=payload, timeout=15)
                    response.raise_for_status()
                    st.session_state["n8n_last_response"] = response.text
                    st.success(text[lang]["n8n_sent"])
                except requests.exceptions.RequestException as e:
                    st.error(f"{text[lang]['n8n_error']} ({e})")
 
    if st.session_state["n8n_last_response"]:
        st.write("---")
        st.subheader("Last n8n Response")
        st.code(st.session_state["n8n_last_response"])
    elif not webhook_url:
        st.info(text[lang]["n8n_idle"])
 
# =====================================================================
# VIEW 4: ASK MIKA MARKET CHATBOT
# =====================================================================
else:
    st.subheader(text[lang]["chat_header"])
    st.write(text[lang]["chat_desc"])
 
    question = st.text_input(text[lang]["chat_ph"], key="mika_question_input")
 
    search_col, refresh_col, clear_col = st.columns(3)
    with search_col:
        send_query = st.button("🔎 Search", key="mika_search", use_container_width=True)
    with refresh_col:
        if st.button("🔄 Refresh", key="mika_refresh", use_container_width=True):
            st.rerun()
    with clear_col:
        if st.button("🗑️ Clear", key="mika_clear", use_container_width=True):
            st.session_state["chat_history"] = []
            st.rerun()
 
    st.write("---")
 
    if not st.session_state["chat_history"]:
        st.info("💡 Ask MIKA a business question to begin.")
    else:
        for msg in st.session_state["chat_history"]:
            css_class = "user-bubble" if msg["role"] == "user" else "mika-bubble"
            st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)
 
    if send_query:
        user_query = question.strip()
 
        if not user_query:
            st.warning("⚠️ Enter a question before searching.")
            st.stop()
 
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        st.markdown(f'<div class="user-bubble">{user_query}</div>', unsafe_allow_html=True)
 
        if not GROQ_AVAILABLE:
            reply = "The `groq` package isn't installed, so I can't reach the AI backend right now."
        else:
            groq_api_key = get_groq_api_key()
            if not groq_api_key:
                reply = (
                    "No Groq API key found. Add GROQ_API_KEY to your Streamlit secrets "
                    "or environment variables to enable this chatbot."
                )
            else:
                try:
                    client = Groq(api_key=groq_api_key)
                    summary = build_dataset_summary()
                    system_context = f"""
                    You are MIKA's market intelligence assistant for Kenya's appliance retail sector.
                    Known context: transactional total KSh {TRANSACTIONAL_TOTAL:,.2f} across {TRANSACTIONAL_RECORDS} records,
                    official source total KSh {OFFICIAL_SOURCE_TOTAL:,.2f}, {summary['total_outlets']} verified stockist outlets,
                    {UNTRACKED_STOCKIST_PCT}% of transaction sales lack stockist tracking data.
                    Competitors tracked: Samsung, LG, Ramtons, Hisense, Alyassin.
                    Answer in {lang}. Be concise and business-focused. If you don't know something
                    specific (e.g. live competitor pricing), say so rather than inventing numbers.
                    """
                    completion = client.chat.completions.create(
                        model=GROQ_MODEL,
                        messages=[
                            {"role": "system", "content": system_context},
                            {"role": "user", "content": user_query},
                        ],
                    )
                    reply = completion.choices[0].message.content
                except Exception as e:
                    if "request_too_large" in str(e) or "413" in str(e):
                        reply = (
                            "⚠️ That request was too large for the AI service to process. "
                            "Try asking a shorter, more specific question."
                        )
                    else:
                        reply = f"AI Server Connection Error: {e}"
 
        st.session_state["chat_history"].append({"role": "assistant", "content": reply})
        st.markdown(f'<div class="mika-bubble">{reply}</div>', unsafe_allow_html=True)
 
