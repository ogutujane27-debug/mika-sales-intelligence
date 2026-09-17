import streamlit as st
import pandas as pd
import plotly.express as px
import io
import requests

# =====================================================================
# 1. ENTERPRISE SUITE INITIALIZATION & PREMIUM CSS STYLING
# =====================================================================
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

st.markdown("""
    <style>
    @keyframes slideUp { 
        0% { opacity: 0; transform: translateY(15px); } 
        100% { opacity: 1; transform: translateY(0); } 
    }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    [data-testid="stSidebarNav"] {display: none;}
    
    .stButton>button { 
        background-color: #28a745 !important; color: white !important; font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(40,167,69,0.25); border-radius: 6px !important; width: 100%; height: 45px;
    }
    .user-bubble { background-color: #e2f0d9; padding: 12px; border-radius: 8px; margin-bottom: 8px; color: #1e3d14; font-family: sans-serif; }
    .mika-bubble { background-color: #f1f1f1; padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #28a745; color: #222222; font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

```python
# ================================================================
# VIEW 2: REAL N8N ORCHESTRATION CORE
# ================================================================
if page == "🧠 Real n8n Orchestration Core":

    st.subheader(text[lang]["ai_header"])

    st.write(text[lang]["ai_prompt"])

    st.info(
        "Webhook flow: MIKA → HTTP POST → n8n Webhook → Workflow → "
        "Respond to Webhook → MIKA"
    )

    # ------------------------------------------------------------
    # N8N WEBHOOK CONFIGURATION
    # ------------------------------------------------------------
    n8n_url = st.text_input(
        "n8n Webhook URL Target Endpoint:",
        value="http://192.168.1.87:5678/webhook/mika",
        help=(
            "Use the actual n8n Webhook URL. "
            "Do NOT use the Streamlit port 8501."
        )
    )

    # Optional test URL
    st.caption(
        "Example: http://192.168.1.87:5678/webhook/mika "
        "or during development: /webhook-test/mika"
    )

    st.write("---")

    # ------------------------------------------------------------
    # EXECUTE LIVE N8N PIPELINE
    # ------------------------------------------------------------
    if st.button(
        text[lang]["ai_btn"],
        type="primary",
        key="execute_live_n8n"
    ):

        if not n8n_url.strip():
            st.error("❌ Please enter the n8n Webhook URL.")
        else:

            # Payload sent to n8n
            payload = {
                "trigger_source": "MIKA Streamlit",
                "pipeline": "Global Market Intelligence",
                "request_type": "enterprise_analysis",

                "language": lang,

                "region_data": df_region.to_dict(
                    orient="records"
                ),

                "payment_data": df_payment.to_dict(
                    orient="records"
                ),

                "total_verified_revenue": float(
                    df_region["Total_Sales"].sum()
                ),

                "outlet_count": int(
                    df_region["Outlet_Count"].sum()
                )
            }

            st.info(
                f"🔌 Sending live payload to n8n:\n\n"
                f"`{n8n_url}`"
            )

            try:

                response = requests.post(
                    n8n_url.strip(),
                    json=payload,
                    timeout=30
                )

                # ------------------------------------------------
                # HTTP SUCCESS
                # ------------------------------------------------
                if response.ok:

                    st.success(
                        f"✅ n8n workflow responded successfully "
                        f"(HTTP {response.status_code})"
                    )

                    # Try to interpret n8n response as JSON
                    try:
                        result = response.json()

                        st.subheader(
                            "📡 n8n Pipeline Response"
                        )

                        st.json(result)

                        # Try common response fields
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

                        # n8n may return plain text
                        response_text = response.text.strip()

                        st.subheader(
                            "📡 n8n Pipeline Response"
                        )

                        if response_text:
                            st.success(response_text)
                        else:
                            st.warning(
                                "⚠️ n8n returned an empty response."
                            )

                # ------------------------------------------------
                # HTTP ERROR
                # ------------------------------------------------
                else:

                    st.error(
                        f"❌ n8n returned HTTP "
                        f"{response.status_code}"
                    )

                    if response.text:
                        st.code(
                            response.text,
                            language="text"
                        )

            # ----------------------------------------------------
            # CONNECTION ERROR
            # ----------------------------------------------------
            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to n8n."
                )

                st.warning(
                    "Check that:\n"
                    "1. n8n is running.\n"
                    "2. The IP address is correct.\n"
                    "3. Port 5678 is reachable.\n"
                    "4. The Webhook node is active."
                )

            # ----------------------------------------------------
            # TIMEOUT
            # ----------------------------------------------------
            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ n8n did not respond within 30 seconds."
                )

                st.warning(
                    "The workflow may still be processing, "
                    "or the webhook/workflow is not responding."
                )

            # ----------------------------------------------------
            # OTHER REQUEST ERROR
            # ----------------------------------------------------
            except requests.exceptions.RequestException as e:

                st.error(
                    f"❌ n8n request failed: {e}"
                )

            # ----------------------------------------------------
            # UNEXPECTED ERROR
            # ----------------------------------------------------
            except Exception as e:

                st.error(
                    f"❌ Unexpected pipeline error: {e}"
                )


# ================================================================
# VIEW 3: ASK MIKA MARKET CHATBOT
# ================================================================
if page == "💬 Ask MIKA Market Chatbot":

    st.subheader(text[lang]["chat_header"])

    st.write(text[lang]["chat_desc"])

    # ------------------------------------------------------------
    # CHAT CONTROL BAR
    # ------------------------------------------------------------
    col_search, col_refresh = st.columns([4, 1])

    with col_search:

        search_query = st.text_input(
            "🔍 Search MIKA:",
            placeholder=text[lang]["chat_ph"],
            key="mika_search_input"
        )

    with col_refresh:

        st.write("")

        if st.button(
            "🔄 Refresh",
            key="mika_refresh"
        ):

            st.session_state["chat_history"] = []

            # Clear current input on next rerun
            st.rerun()

    # ------------------------------------------------------------
    # SEND BUTTON
    # ------------------------------------------------------------
    send_query = st.button(
        "🔍 Search / Ask MIKA",
        type="primary",
        key="mika_send"
    )

    # ------------------------------------------------------------
    # CHAT DISPLAY
    # ------------------------------------------------------------
    st.write("---")

    if not st.session_state["chat_history"]:

        st.info(
            "💡 Ask MIKA a business question to begin."
        )

    else:

        for message in st.session_state["chat_history"]:

            if message["role"] == "user":

                st.markdown(
                    f"""
                    <div class="user-bubble">
                        <strong>👤 You</strong><br>
                        {message["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="mika-bubble">
                        <strong>🤖 MIKA</strong><br>
                        {message["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ------------------------------------------------------------
    # ASK MIKA
    # ------------------------------------------------------------
    if send_query:

        question = search_query.strip()

        if not question:

            st.warning(
                "⚠️ Please enter a question before searching."
            )

        else:

            # Add user message immediately
            st.session_state["chat_history"].append(
                {
                    "role": "user",
                    "content": question
                }
            )

            # ----------------------------------------------------
            # CHATBOT WEBHOOK
            # ----------------------------------------------------
            # IMPORTANT:
            # Change this to your actual n8n CHAT webhook.
            #
            # Example:
            # http://192.168.1.87:5678/webhook/mika-chat
            # ----------------------------------------------------
            chatbot_url = st.session_state.get(
                "mika_chat_webhook",
                "http://192.168.1.87:5678/webhook/mika-chat"
            )

            chat_payload = {

                "trigger_source": "MIKA Chatbot",

                "request_type": "market_intelligence_question",

                "language": lang,

                "question": question,

                "conversation": st.session_state[
                    "chat_history"
                ],

                "regional_data": df_region.to_dict(
                    orient="records"
                ),

                "payment_data": df_payment.to_dict(
                    orient="records"
                )
            }

            with st.spinner("🤖 MIKA is analysing your question..."):

                try:

                    response = requests.post(
                        chatbot_url,
                        json=chat_payload,
                        timeout=45
                    )

                    # ------------------------------------------------
                    # SUCCESS
                    # ------------------------------------------------
                    if response.ok:

                        try:

                            result = response.json()

                            answer = (
                                result.get("response")
                                or result.get("answer")
                                or result.get("output")
                                or result.get("message")
                            )

                            # If n8n returns an unexpected JSON structure
                            if not answer:

                                answer = str(result)

                        except ValueError:

                            answer = response.text.strip()

                        if not answer:

                            answer = (
                                "MIKA received an empty response "
                                "from the automation workflow."
                            )

                        st.session_state[
                            "chat_history"
                        ].append(
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        )

                    # ------------------------------------------------
                    # HTTP FAILURE
                    # ------------------------------------------------
                    else:

                        error_message = (
                            f"n8n chatbot returned HTTP "
                            f"{response.status_code}."
                        )

                        if response.text:
                            error_message += (
                                f"\n\n{response.text}"
                            )

                        st.session_state[
                            "chat_history"
                        ].append(
                            {
                                "role": "assistant",
                                "content": (
                                    "❌ " + error_message
                                )
                            }
                        )

                # ----------------------------------------------------
                # CONNECTION ERROR
                # ----------------------------------------------------
                except requests.exceptions.ConnectionError:

                    st.session_state[
                        "chat_history"
                    ].append(
                        {
                            "role": "assistant",
                            "content": (
                                "❌ I cannot connect to the MIKA "
                                "n8n chatbot right now. "
                                "Please check that n8n is running "
                                "and that the webhook URL is correct."
                            )
                        }
                    )

                # ----------------------------------------------------
                # TIMEOUT
                # ----------------------------------------------------
                except requests.exceptions.Timeout:

                    st.session_state[
                        "chat_history"
                    ].append(
                        {
                            "role": "assistant",
                            "content": (
                                "⏱️ The MIKA workflow took too long "
                                "to respond. Check the n8n execution."
                            )
                        }
                    )

                # ----------------------------------------------------
                # OTHER ERROR
                # ----------------------------------------------------
                except requests.exceptions.RequestException as e:

                    st.session_state[
                        "chat_history"
                    ].append(
                        {
                            "role": "assistant",
                            "content": (
                                f"❌ MIKA connection error: {e}"
                            )
                        }
                    )

                # ----------------------------------------------------
                # UNEXPECTED ERROR
                # ----------------------------------------------------
                except Exception as e:

                    st.session_state[
                        "chat_history"
                    ].append(
                        {
                            "role": "assistant",
                            "content": (
                                f"❌ Unexpected MIKA error: {e}"
                            )
                        }
                    )

            # Refresh screen to show new response
            st.rerun()
```
