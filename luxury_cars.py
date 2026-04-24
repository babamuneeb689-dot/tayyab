import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load local environment variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(page_title="Luxury Car Selector", page_icon="🏎️", layout="wide")

# Custom Styling
st.markdown("""
    <style>
        .block-container { padding-bottom: 100px; }
        div[data-testid="stChatInput"] { position: fixed; bottom: 20px; z-index: 99; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State (Stored in temporary RAM only)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- LUXURY SELECTOR SYSTEM INSTRUCTIONS ---
system_instruction = """
You are an Elite Automobile Consultant. You must follow this EXACT 7-step sequence:

1. CAR COMPANIES: Start by enlisting top luxury brands (e.g., Mercedes-Benz, BMW, Audi, Tesla, Porsche, Range Rover) and ask the user to pick one.
2. BUDGET: Ask for their budget range (e.g., in Millions PKR or USD).
3. RADAR: Ask if they require "Radar/Adaptive Cruise Control" and "Autonomous Driving" features.
4. ENGINE: Ask for their preferred engine capacity (e.g., 1.5L, 2.0L Turbo, 3.0L V6, etc.).
5. MILEAGE: Ask for their minimum required fuel average/mileage (km/l).
6. EV or PETROL: Ask if they want an "Electric Vehicle (EV)" or a "Petrol/Hybrid" car.
7. SUGGEST: Based on ALL previous answers, suggest a list of 3 specific luxury cars with their key features and estimated price.

STRICT RULES:
- Do not ask all questions at once. Ask one, wait for the reply, then ask the next.
- Maintain a highly professional and premium tone.
- If a user's requirements are impossible, explain why and offer the best alternative.
"""

# --- Sidebar ---
with st.sidebar:
    st.title("📂 Consultation")
    st.write("Find your next masterpiece of engineering.")
    if st.button("🗑️ Clear Current Selection", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main UI ---
st.title("🏎️ Luxury Car Selector")
st.markdown("#### *Find your next masterpiece of engineering*")

# Display current chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Text Input
prompt = st.chat_input("Enter your preference...")

# API Key Retrieval
api_key = os.getenv("groq_api") or st.secrets.get("groq_api")

if prompt:
    if not api_key:
        st.error("API Key missing! Please check your Streamlit Secrets.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": system_instruction}] + st.session_state.messages,
                model="llama-3.1-8b-instant"
            )
            reply = response.choices[0].message.content
            
            with st.chat_message("assistant"):
                st.markdown(reply)
                
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
        except Exception as e:
            st.error(f"Error: {e}")