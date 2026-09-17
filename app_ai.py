import streamlit as st
import pandas as pd
import plotly.express as px
import io
import requests

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

# =====================================================================
# 3. SESSION STATE
# =====================================================================
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "enterprise_analysis_run" not in st.session_state:
    st.session_state["enterprise_analysis_run"] = False

# =====================================================================
# 4. LANGUAGE DICTIONARY
# =====================================================================
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
        "ai_prompt": "Enter your active n8n webhook endpoint to send the enterprise intelligence payload into your workflow.",
        "ai_btn": "🚀 Execute Live n8n Pipeline",
        "ai_idle": "💡 Real n8n Connection Core: Waiting for outbound execution trigger input.",
        "chat_header": "💬 Ask MIKA — Limitless Market Intelligence Chatbot",
        "chat_desc": "Ask any business, competitor (Samsung, LG, Ramtons, Hisense, Alyassin), supply chain, stockout, or market query related to Kenya.",
        "chat_ph": "Type your query here and press enter...",
    },
    "Kiswahili": {
        "title": "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo",
        "desc": "Mfumo wa kiotomatiki unaochakata mapato ya miamala na vyanzo rasmi vya malengo kando.",
        "m1": "📦 Jumla ya Mapato Yaliyothibitishwa",
        "m2": "📈 Lengo Rasmi la Mauzo",
        "risk_banner": "⚠️ Riski ya Traceability: KSh Bilioni 2.60 za miamala hazina taarifa za wauzaji maalum. Hili ni suala la ufuatiliaji, sio upotezaji wa kifedha wa haraka.",
        "chart1": "🌍 Uchangiaji wa Mauzo Kimkoa",
        "chart2": "💳 Masharti ya Malipo na Hali ya Ukwasi",
        "ai_header": "🔌 Mitambo ya Kiotomatiki wa n8n (Live)",
        "ai_prompt": "Weka anwani halisi ya webhook ya n8n ili kutuma data ya biashara kwenye workflow yako.",
        "ai_btn": "🚀 Washa n8n Pipeline ya Ukweli",
        "ai_idle": "💡 Mfumo wa n8n: Unasubiri amri yako ya kuwasha workflow.",
        "chat_header": "💬 Uliza MIKA — Chatbot ya Ujasusi wa Soko",
        "chat_desc": "Uliza kuhusu biashara, washindani, usambazaji, stockout, au soko la Kenya.",
        "chat_ph": "Andika swali lako hapa na ubonyeze enter...",
    },
}

# =====================================================================
# 5. SIDEBAR MULTI-PAGE ENGINE
# =====================================================================
with st.sidebar:
    st.header("⚡ Command Center")

    lang = st.radio(
        "🌐 Language / Lugha:",
        ["English", "Kiswahili"],
        horizontal=True,
    )

    st.write("---")

    page = st.radio(
        "Select Dashboard View:" if lang == "English" else "Chagua Mtazamo:",
        [
            "📈 Executive Overview & Pipeline",
            "🧠 Real n8n Orchestration Core",
            "💬 Ask MIKA Market Chatbot",
        ],
    )

    st.write("---")
    st.caption("MIKA Automation Infrastructure Layer Active.")

# =====================================================================
# 6. MAIN DISPLAY FRAME
# =====================================================================
st.title(text[lang]["title"])
st.caption(text[lang]["desc"])
st.warning(text[lang]["risk_banner"])
st.write("---")

# =====================================================================
# VIEW 1: EXECUTIVE OVERVIEW & PIPELINE
# =====================================================================
if page == "📈 Executive Overview & Pipeline":

    if st.button(
        "🚀 Run Deep Enterprise Analysis",
        type="primary",
        key="deep_enterprise_analysis",
    ):
        total_outlets = int(df_region["Outlet_Count"].sum())
        nairobi_pct = float(df_region.at[0, "Pct_of_Total"])
        max_credit_pct = float(df_payment.at[0, "Pct_of_Total"])
        max_credit_term = str(df_payment.at[0, "Payment Terms"])

        st.session_state["enterprise_analysis_run"] = True

        st.success("📊 Enterprise Intelligence Audit Complete!")

        st.info(
            f"""
**Matrix Operational Highlights:**

* Cumulative distribution infrastructure spans **{total_outlets} verified stockist outlets** inside Kenya.
* Primary regional market density is dominated by **Nairobi Region** accounting for **{nairobi_pct}%** of market share traffic.
* Financial exposure audit indicates **{max_credit_term}** accounts for the highest liquidity concentration at **{max_credit_pct}%** of the payment-terms matrix.
* Competitor logging active against baseline records: Samsung, LG, Ramtons, Hisense, Alyassin ecosystem.
"""
        )

    st.write("---")
    st.subheader(text[lang]["chart1"])

    st.dataframe(
        df_region,
        use_container_width=True,
        hide_index=True,
    )

    st.write("---")
    st.subheader(text[lang]["chart2"])

    st.dataframe(
        df_payment,
        use_container_width=True,
        hide_index=True,
    )

# =====================================================================
# VIEW 2: REAL N8N ORCHESTRATION CORE
# =====================================================================
elif page == "🧠 Real n8n Orchestration Core":

    st.subheader(text[lang]["ai_header"])
    st.write(text[lang]["ai_prompt"])

    st.info(
        "Webhook flow: MIKA → HTTP POST → n8n Webhook → Workflow → "
        "Respond to Webhook → MIKA"
    )

    n8n_url = st.text_input(
        "n8n Webhook URL Target Endpoint:",
        value="",
        placeholder="http://192.168.1.87:5678/webhook/mika",
        help="Use the actual Webhook URL copied from your n8n Webhook node. Do not use the Streamlit port 8501.",
        key="n8n_webhook_url",
    )

    st.caption(
        "Production webhook normally uses /webhook/... . "
        "During testing, n8n may provide /webhook-test/... ."
    )

    st.write("---")

    if st.button(
        text[lang]["ai_btn"],
        type="primary",
        key="execute_live_n8n",
    ):

        if not n8n_url.strip():
            st.error(
                "❌ Enter the actual n8n Webhook URL first. "
                "Example: http://192.168.1.87:5678/webhook/mika"
            )
        elif not (
            n8n_url.strip().startswith("http://")
            or n8n_url.strip().startswith("https://")
        ):
            st.error("❌ The webhook URL must start with http:// or https://")
        else:

            payload = {
                "trigger_source": "MIKA Streamlit",
                "pipeline": "Global Market Intelligence",
                "request_type": "enterprise_analysis",
                "language": lang,
                "region_data": df_region.to_dict(orient="records"),
                "payment_data": df_payment.to_dict(orient="records"),
                "total_verified_revenue": float(
                    df_region["Total_Sales"].sum()
                ),
                "outlet_count": int(
                    df_region["Outlet_Count"].sum()
                ),
            }

            st.info(
                f"🔌 Sending live payload to n8n:\n\n`{n8n_url.strip()}`"
            )

            try:
                response = requests.post(
                    n8n_url.strip(),
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                )

                if response.ok:
                    st.success(
                        f"✅ n8n workflow responded successfully "
                        f"(HTTP {response.status_code})"
                    )

                    if response.text.strip():
                        try:
                            result = response.json()
                            st.subheader("📡 n8n Pipeline Response")
                            st.json(result)

                            if isinstance(result, dict):
                                mika_response = (
                                    result.get("response")
                                    or result.get("message")
                                    or result.get("output")
                                    or result.get("answer")
                                )
                                if mika_response:
                                    st.success(
                                        f"🤖 n8n Result:\n\n{mika_response}"
                                    )
                        except ValueError:
                            st.subheader("📡 n8n Pipeline Response")
                            st.success(response.text.strip())
                    else:
                        st.warning(
                            "⚠️ n8n accepted the request but returned an empty response. "
                            "If you expect a response, add/configure a Respond to Webhook node."
                        )
                else:
                    st.error(
                        f"❌ n8n returned HTTP {response.status_code}"
                    )
                    if response.text.strip():
                        st.code(response.text.strip(), language="text")

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the n8n server.")
                st.warning(
                    "Check that n8n is running, the server IP is correct, "
                    "port 5678 is reachable, and the webhook URL is active."
                )

            except requests.exceptions.Timeout:
                st.error("⏱️ n8n did not respond within 30 seconds.")
                st.warning(
                    "Check the n8n execution panel. The workflow may be "
                    "processing, waiting for another node, or not returning a response."
                )

            except requests.exceptions.RequestException as exc:
                st.error(f"❌ n8n request failed: {exc}")

            except Exception as exc:
                st.error(f"❌ Unexpected pipeline error: {exc}")

# =====================================================================
# VIEW 3: ASK MIKA MARKET CHATBOT
# =====================================================================
elif page == "💬 Ask MIKA Market Chatbot":

    st.subheader(text[lang]["chat_header"])
    st.write(text[lang]["chat_desc"])

    # ---------------------------------------------------------------
    # CHATBOT WEBHOOK
    # ---------------------------------------------------------------
    chatbot_url = st.text_input(
        "MIKA Chatbot n8n Webhook:",
        value="",
        placeholder="http://192.168.1.87:5678/webhook/mika-chat",
        help="Paste the webhook URL of the n8n workflow that handles MIKA chat.",
        key="mika_chat_webhook",
    )

    # ---------------------------------------------------------------
    # CLEAR SEARCH / REFRESH
    # ---------------------------------------------------------------
    search_col, refresh_col = st.columns([5, 1])

    with search_col:
        question = st.text_input(
            "🔍 Search / Ask MIKA",
            placeholder=text[lang]["chat_ph"],
            key="mika_search_input",
            label_visibility="visible",
        )

    with refresh_col:
        st.write("")
        if st.button(
            "🔄 Refresh",
            key="mika_refresh",
            help="Clear the current MIKA conversation",
        ):
            st.session_state["chat_history"] = []
            st.rerun()

    ask_col, clear_col = st.columns([5, 1])

    with ask_col:
        send_query = st.button(
            "🔍 Search / Ask MIKA",
            type="primary",
            key="mika_send",
        )

    with clear_col:
        if st.button(
            "🗑️ Clear",
            key="mika_clear",
        ):
            st.session_state["chat_history"] = []
            st.rerun()

    st.write("---")

    # ---------------------------------------------------------------
    # CHAT HISTORY
    # ---------------------------------------------------------------
    if not st.session_state["chat_history"]:
        st.info("💡 Ask MIKA a business question to begin.")
    else:
        for message in st.session_state["chat_history"]:
            content = str(message.get("content", ""))

            if message.get("role") == "user":
                st.markdown(
                    f"""
                    <div class="user-bubble">
                        <strong>👤 You</strong><br>
                        {content}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="mika-bubble">
                        <strong>🤖 MIKA</strong><br>
                        {content}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ---------------------------------------------------------------
    # SEND QUESTION TO N8N
    # ---------------------------------------------------------------
    if send_query:

        clean_question = question.strip()

        if not clean_question:
            st.warning("⚠️ Enter a question before searching.")

        elif not chatbot_url.strip():
            st.error(
                "❌ Enter the actual MIKA chatbot n8n Webhook URL first."
            )

        elif not (
            chatbot_url.strip().startswith("http://")
            or chatbot_url.strip().startswith("https://")
        ):
            st.error(
                "❌ The chatbot webhook URL must start with http:// or https://"
            )

        else:

            st.session_state["chat_history"].append(
                {
                    "role": "user",
                    "content": clean_question,
                }
            )

            chat_payload = {
                "trigger_source": "MIKA Chatbot",
                "request_type": "market_intelligence_question",
                "language": lang,
                "question": clean_question,
                "conversation": st.session_state["chat_history"],
                "regional_data": df_region.to_dict(orient="records"),
                "payment_data": df_payment.to_dict(orient="records"),
            }

            with st.spinner("🤖 MIKA is analysing your question..."):

                try:
                    response = requests.post(
                        chatbot_url.strip(),
                        json=chat_payload,
                        headers={"Content-Type": "application/json"},
                        timeout=45,
                    )

                    if response.ok:

                        answer = ""

                        if response.text.strip():
                            try:
                                result = response.json()

                                if isinstance(result, dict):
                                    answer = (
                                        result.get("response")
                                        or result.get("answer")
                                        or result.get("output")
                                        or result.get("message")
                                        or ""
                                    )

                                    if not answer:
                                        answer = str(result)
                                else:
                                    answer = str(result)

                            except ValueError:
                                answer = response.text.strip()

                        if not answer:
                            answer = (
                                "MIKA received the request, but the n8n "
                                "workflow returned no answer."
                            )

                        st.session_state["chat_history"].append(
                            {
                                "role": "assistant",
                                "content": answer,
                            }
                        )

                    else:

                        error_message = (
                            f"n8n chatbot returned HTTP "
                            f"{response.status_code}."
                        )

                        if response.text.strip():
                            error_message += (
                                f"\n\n{response.text.strip()}"
                            )

                        st.session_state["chat_history"].append(
                            {
                                "role": "assistant",
                                "content": "❌ " + error_message,
                            }
                        )

                except requests.exceptions.ConnectionError:
                    st.session_state["chat_history"].append(
                        {
                            "role": "assistant",
                            "content": (
                                "❌ MIKA cannot connect to the n8n chatbot. "
                                "Check that n8n is running and that the "
                                "webhook URL is reachable from this Streamlit app."
                            ),
                        }
                    )

                except requests.exceptions.Timeout:
                    st.session_state["chat_history"].append(
                        {
                            "role": "assistant",
                            "content": (
                                "⏱️ The MIKA workflow did not respond within "
                                "45 seconds. Check the n8n execution."
                            ),
                        }
                    )

                except requests.exceptions.RequestException as exc:
                    st.session_state["chat_history"].append(
                        {
                            "role": "assistant",
                            "content": f"❌ MIKA connection error: {exc}",
                        }
                    )

                except Exception as exc:
                    st.session_state["chat_history"].append(
                        {
                            "role": "assistant",
                            "content": f"❌ Unexpected MIKA error: {exc}",
                        }
                    )

            st.rerun()
