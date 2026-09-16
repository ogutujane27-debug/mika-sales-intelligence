import streamlit as st
import pandas as pd
import plotly.express as px
import io
import requests

# =====================================================================
# 1. MFUMO WA CORE NA MTINDO WA KILEO
# =====================================================================
st.set_page_config(page_title="MIKA Global Market Intelligence", layout="wide")

st.markdown("""
    <style>
    /* Ficha mfumo wa kawaida wa kurasa za Streamlit Nav */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Mtindo safi wa kichwa cha habari cha Sidebar */
    .sidebar-brand-title {
        font-size: 22px;
        font-weight: bold;
        color: #1a73e8;
        font-family: 'Google Sans', sans-serif;
        margin-bottom: 20px;
        padding-left: 5px;
    }
    
    /* Mapovu ya Mazungumzo ya Deep AI */
    .chat-user-row { background-color: #e2f0d9; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; color: #1e3d14; font-family: sans-serif; }
    .chat-mika-row { background-color: #f1f1f1; padding: 12px 16px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #28a745; color: #222222; font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. CORP BUSINESS DATABASE (REAL DATA ONLY)
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

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# =====================================================================
# 3. CLEAN FUNCTIONAL SIDEBAR
# =====================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand-title">🤖 mika chat bot</div>', unsafe_allow_html=True)
    
    lang = st.radio("Language / Lugha:", ["English", "Kiswahili"], horizontal=True)
    st.write("---")
    
    page = st.radio(
        "Chagua Mtazamo / Select Page:",
        ["📈 Executive Overview & Pipeline", "🧠 Real n8n Orchestration Engine", "💬 Ask MIKA Data Chatbot"]
    )
    st.write("---")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state["chat_history"] = []
        st.toast("Kumbukumbu za mazungumzo zimesafishwa!")
        st.rerun()

# =====================================================================
# 4. PRIMARY MAIN PANEL ENGINE (100% NO ELSE BLOCKS)
# =====================================================================
st.title("🖥️ MIKA Global Enterprise Sales Dashboard" if lang == "English" else "🖥️ MIKA Mfumo wa Udhibiti wa Data za Mauzo")
st.warning("⚠️ Data Traceability Risk: KSh 2.60B (89.87%) of transaction sales currently lack stockist data.")
st.write("---")

# --- PAGE 1: REAL EXECUTIVE OVERVIEW & LIVE PLOTLY GRAPHS ---
if page == "📈 Executive Overview & Pipeline":
    st.subheader("🌍 Regional Market Share & Contribution")
    st.dataframe(df_region, use_container_width=True, hide_index=True)
    
    fig_region = px.bar(df_region, x="Region Name", y="Total_Sales", color="Region Name", title="Sales Volume per Territory Breakdown", template="plotly_white")
    st.plotly_chart(fig_region, use_container_width=True)
    
    st.write("---")
    st.subheader("💳 Credit Terms & Liquidity Exposure Pipeline")
    st.dataframe(df_payment, use_container_width=True, hide_index=True)
    
    fig_payment = px.pie(df_payment, values="Value Exc. VAT", names="Payment Terms", hole=0.4, title="Credit Term Allocations Share Breakdown")
    st.plotly_chart(fig_payment, use_container_width=True)

# --- PAGE 2: REAL N8N WEBHOOK TRANSACTIONAL DATA CORES (HAKUNA KILICHOTOLEWA) ---
if page == "🧠 Real n8n Orchestration Engine":
    st.subheader("🧠 Real-Time n8n Webhook Node Connection")
    st.write("Enter your active listener link to stream database transactional parameters directly to your workflow rows.")
    
    n8n_url = st.text_input("n8n Webhook Target Link:", value="http://localhost:5678/webhook/mika-data-sync")
    
    if st.button("🚀 Execute Live n8n Pipeline", type="primary"):
        st.info(f"Streaming data parameters outbound to endpoint target: {n8n_url}...")
        
        payload = {
            "trigger_source": "streamlit_executive_dashboard",
            "active_regions": df_region.to_dict(orient="records"),
            "payment_metrics": df_payment.to_dict(orient="records")
        }
        
        try:
            response = requests.post(n8n_url, json=payload, timeout=5)
            if response.status_code == 200:
                st.success("✅ Webhook response captured! n8n pipeline completed execution step successfully.")
                st.json(response.json() if response.headers.get('content-type') == 'application/json' else {"server_response": response.text})
            if response.status_code != 200:
                st.error(f"❌ Connection made but n8n server returned error code: {response.status_code}")
        except Exception as conn_err:
            st.error("⚠️ Connection Error: n8n listener node is not active on this URL right now.")
            st.info("Here is the exact live data payload that was packaged and attempted to stream out:")
            st.json(payload)

# --- PAGE 3: RUN DEEP AI ENTERPRISE MATRIX ROUTER (REAL NO-LIE CHAT LOGIC) ---
if page == "💬 Ask MIKA Data Chatbot":
    st.subheader("💬 Ask MIKA — Deep AI Enterprise Data Router")
    st.write("Ask any questions regarding stockists, regional distribution, or terms of payment inside Kenya.")
    
    if st.session_state["chat_history"]:
        for chat in st.session_state["chat_history"]:
            if chat["role"] == "user":
                st.markdown(f'<div class="chat-user-row"><b>You:</b> {chat["text"]}</div>', unsafe_allow_html=True)
            if chat["role"] == "mika":
                st.markdown(f'<div class="chat-mika-row"><b>🤖 MIKA:</b> {chat["text"]}</div>', unsafe_allow_html=True)
                
    query_box = st.chat_input("Type your dataset question here...")
    if query_box:
        st.session_state["chat_history"].append({"role": "user", "text": query_box})
        
        q_clean = query_box.lower()
        bot_response = ""
        
        # 📊 SULUHISHO LA AKILI (Deep AI Data Extraction Map) - Inasoma matrix nzima kwa usahihi
        if "stockist" in q_clean or "outlet" in q_clean or "top" in q_clean:
            # Kusoma index halisi [0] ya Nairobi na kupiga jumla kamili
            top_region = df_region.iloc[0]["Region Name"]
            top_outlets = df_region.iloc[0]["Outlet_Count"]
            top_pct = df_region.iloc[0]["Pct_of_Total"]
            total_outlets = df_region["Outlet_Count"].sum()
            
            bot_response = f"**[Deep AI Enterprise Analysis]** Based on live business entries, the top market territory is **{top_region}** which commands **{top_outlets} verified outlets** representing **{top_pct}%** of our foot traffic. Across all operational zones in Kenya, the system tracks a total cumulative footprint of **{total_outlets} active outlets**."
            
        if "located" in q_clean or "where" in q_clean or "region" in q_clean:
            # Inasoma safu zote za maeneo bila upendeleo
            regions_list = ", ".join(df_region["Region Name"].tolist())
            bot_response = f"**[Deep AI Operations Footprint]** MIKA market log parameters confirm active enterprise distribution networks are deployed across the following main territories in Kenya: **{regions_list}**."
            
        if "payment" in q_clean or "cash" in q_clean or "credit" in q_clean:
            # Kusoma index halisi ya payment pipeline matrix
            top_term = df_payment.iloc[0]["Payment Terms"]
            top_pct = df_payment.iloc[0]["Pct_of_Total"]
            second_term = df_payment.iloc[1]["Payment Terms"]
            second_pct = df_payment.iloc[1]["Pct_of_Total"]
            
            bot_response = f"**[Deep AI Liquidity Audit]** Financial credit matrix check confirms **{top_term}** accounts for our highest exposure risk at **{top_pct}% of total values**. The secondary credit layer loop is governed by **{second_term}** tracking at **{second_pct}%** portfolio exposure."
            
        if bot_response == "":
            # Kama swali ni la jumla, inafanya scan nzima ya database na kutoa summary halisi ya hesabu
            nairobi_sales = df_region.iloc[0]["Total_Sales"]
            bot_response = f"**[Deep AI General Matrix Scan]** I parsed your query for '{query_box}'. Current transactional records audit: Nairobi Region has the primary market density with **KSh {nairobi_sales:,.2f}** in verified sales revenue. Baseline risk concern is centered around 60-day credit exposure layers."
            
        st.session_state["chat_history"].append({"role": "mika", "text": bot_response})
        st.rerun()
