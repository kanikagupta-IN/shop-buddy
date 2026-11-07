# app/ui.py
import streamlit as st
from app.database.vector_store import VectorDB
from app.ai.agent import EcommerceMCPAgent
from app.utils.i18n import TRANSLATIONS
from app.utils.feedback_store import LocalFeedbackStore

# Application Configuration Frame
st.set_page_config(page_title="Bilingual MCP Agent Shop", layout="wide")

# Persistent State Management Engine
if "db" not in st.session_state:
    st.session_state.db = VectorDB()
if "agent" not in st.session_state:
    st.session_state.agent = EcommerceMCPAgent(st.session_state.db)
if "feedback_store" not in st.session_state:
    st.session_state.feedback_store = LocalFeedbackStore()
if "cart" not in st.session_state:
    st.session_state.cart = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "checkout_active" not in st.session_state:
    st.session_state.checkout_active = False

# Sidebar Language Selection Menu 
with st.sidebar:
    st.header("Language Settings / भाषा सेटिंग्स")
    lang_choice = st.selectbox(
        "Choose Interface Language / भाषा चुनें",
        options=["English", "हिंदी (Hindi)"],
        index=0
    )
    # Map selected display string down to system keys
    lang_key = "en" if lang_choice == "English" else "hi"

    # Seed default welcome message if the timeline is empty
    t = TRANSLATIONS[lang_key]
    
    st.divider()
    
    # NEW: Customer Experience Feedback Collection Hub
    st.subheader(t["feedback_title"])
    with st.form(key="customer_feedback_form", clear_on_submit=True):
        stars = st.slider(t["feedback_rating"], min_value=1, max_value=5, value=5)
        notes = st.text_area(t["feedback_text"], max_chars=150)
        submit_feedback = st.form_submit_button(t["feedback_submit"], use_container_width=True)
        
        if submit_feedback:
            st.session_state.feedback_store.save_review(stars, notes)
            st.success(t["feedback_success"])
            
    # Display running live metrics aggregate panel
    metrics = st.session_state.feedback_store.get_summary_metrics()
    st.markdown(f"#### {t['feedback_metrics_title']}")
    col_m1, col_m2 = st.columns(2)
    col_m1.metric(t["feedback_avg"], f"⭐ {metrics['avg_rating']}/5")
    col_m2.metric(t["feedback_total"], f"👥 {metrics['total_count']}")
    
# MAIN APPLICATION PRESENTATION
if not st.session_state.chat_history:
    st.session_state.chat_history.append({"role": "assistant", "content": t["system_ready"]})

# Presentation Layout Structure 
st.title(t["title"])
st.caption(t["subtitle"])

col_chat, col_cart = st.columns([1.2, 0.8], gap="large")

with col_chat:
    st.subheader(t["chat_header"])
    
    # Display translation matched chat records
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if user_input := st.chat_input(t["chat_placeholder"]):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Route query through the language-aware MCP agent
        agent_result = st.session_state.agent.process_message(user_input, lang_key)
        
        if agent_result["action"] == "ADD_TO_CART":
            st.session_state.cart.append(agent_result["item"])
            
        st.session_state.chat_history.append({"role": "assistant", "content": agent_result["content"]})
        st.rerun()

with col_cart:
    st.subheader(t["cart_header"])
    if not st.session_state.cart:
        st.info(t["cart_empty"])
    else:
        cart_total = 0.0
        for item in st.session_state.cart:
            st.write(f" **{item['name']}** — `${item['price']:.2f}`")
            cart_total += item["price"]
        
        st.markdown(f"### **{t['total_balance']}: \\${cart_total:.2f}**")
        st.divider()
        
        st.session_state.checkout_active = st.checkbox(t["toggle_checkout"], value=st.session_state.checkout_active)
        
        if st.session_state.checkout_active:
            st.info(t["stripe_info"])
            st.text_input(t["dummy_card"], value="4242 •••• •••• 4242", disabled=True)
            paid_tier_required = st.checkbox(t["production_mode"])
            
            if st.button(t["pay_button"], type="primary", use_container_width=True):
                if paid_tier_required:
                    # Renders language-appropriate payment gateway warning block
                    st.error(f"{t['paid_error_title']}\n\n{t['paid_error_desc']}")
                else:
                    st.success(t["success_msg"])
                    st.session_state.cart = []
                    st.session_state.checkout_active = False
                    st.rerun()
