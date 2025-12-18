"""
TalentScout Hiring Assistant
----------------------------
Streamlit-based chatbot with centered intro and theme-responsive UI.
"""

import streamlit as st
import re
from utils import CANDIDATE_FIELDS, FIELD_QUESTIONS
from llm import generate_technical_questions

# --------------------------------------------------
# Page configuration (MUST BE FIRST)
# --------------------------------------------------
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
defaults = {
    "messages": [],
    "candidate_data": {},
    "current_field_index": 0,
    "greeted": False,
    "candidate_collection_complete": False,
    "technical_questions_generated": False,
    "technical_questions": [],
    "current_tech_question_index": 0,
    "technical_answers": [],
    "exited": False,
    "theme": "light"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# Theme Toggle Logic
# --------------------------------------------------
def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

is_dark = st.session_state.theme == "dark"

# --------------------------------------------------
# Frontend UI & CSS (Root Cause Fixes)
# --------------------------------------------------
st.markdown(
    f"""
    <style>
        header {{ visibility: hidden; height: 0px; }}
        
        .stApp {{
            background-color: {"#020617" if is_dark else "#ffffff"} !important;
        }}

        /* --- CONDITIONAL EXIT FIX --- */
        /* This rule only exists when the user has typed exit */
        { '[data-testid="stChatMessageAvatarAssistant"] { display: none !important; }' if st.session_state.exited else "" }
        /* ---------------------------- */

        /* Fix for Bottom Bar Background */
        .st-emotion-cache-128upt6, [data-testid="stBottomBlockContainer"] {{
            background-color: {"#020617" if is_dark else "#ffffff"} !important;
            border: none !important;
            box-shadow: none !important;
        }}

        /* Chat Input Wrapper Styling */
        .st-emotion-cache-k7rogd {{
            background-color: {"#02080c" if is_dark else "#ffffff"} !important;
            border: 1px solid {"#334155" if is_dark else "#e2e8f0"} !important;
            border-radius: 1.25rem !important;
        }}

        /* Textarea Styling & Typing Color Fix */
        textarea[data-testid="stChatInputTextArea"] {{
            background-color: transparent !important;
            color: {"#000000" if is_dark else "#1f2937"} !important;
            caret-color: {"#000000" if is_dark else "#1f2937"} !important;
        }}
        
        textarea[data-testid="stChatInputTextArea"]::placeholder {{
            color: #64748b !important;
        }}

        /* Chat Message Visibility */
        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span {{
            color: {"#ffffff" if is_dark else "#1f2937"} !important;
        }}

        /* Centered Welcome Screen Logic */
        .welcome-screen {{
            text-align: center;
            color: {"#ffffff" if is_dark else "#1f2937"} !important;
            padding: 20px;
        }}
        .large-robot {{ font-size: 80px; margin-bottom: 10px; }}
        .welcome-title {{ font-size: 28px; font-weight: 700; margin-bottom: 15px; }}
        .welcome-desc {{ font-size: 16px; line-height: 1.6; }}

        /* Header & Theme Button */
        .ts-header-bg {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 60px;
            background-color: #000; z-index: 1000;
        }}
        .ts-logo-container {{
            position: fixed; top: 18px; left: 32px; z-index: 1001;
            color: white !important; font-size: 20px; font-weight: 600;
        }}
        div[data-testid="stButton"] {{
            position: fixed; top: 12px; right: 32px; z-index: 1002;
            width: auto !important;
        }}

        /* Fixed Footer */
        .ts-footer {{
            position: fixed; bottom: 0; left: 0; width: 100%;
            background-color: {"#020617" if is_dark else "#ffffff"};
            text-align: center; font-size: 11px; color: #9ca3af;
            padding: 10px 0; z-index: 999;
            border-top: 1px solid {"#1e293b" if is_dark else "#f1f5f9"};
        }}

        .main-content-spacer {{ margin-top: 80px; }}
        .block-container {{ padding-top: 0rem !important; padding-bottom: 7rem !important; }}
    </style>

    <div class="ts-header-bg"></div>
    <div class="ts-logo-container">TalentScout</div>
    <div class="main-content-spacer"></div>
    """,
    unsafe_allow_html=True
)

st.button("☀️ Light" if is_dark else "🌙 Dark", on_click=toggle_theme, key="theme_toggle")

# --------------------------------------------------
# App Logic & Chat Flow
# --------------------------------------------------
if st.session_state.exited:
    for msg in st.session_state.messages:
        if "welcome-screen" in msg["content"]:
            st.markdown(msg["content"], unsafe_allow_html=True)
        else:
            with st.chat_message(msg["role"]): 
                st.markdown(msg["content"], unsafe_allow_html=True)
    st.stop()

# 1. Start conversation: Add persistent Greeting UI to chat history
if not st.session_state.greeted:
    welcome_html = f"""
    <div class="welcome-screen">
        <div class="large-robot">🤖</div>
        <div class="welcome-title">TalentScout Hiring Assistant</div>
        <div class="welcome-desc">
            Hello! 👋 I'm <strong>TalentScout</strong>, your hiring assistant.<br><br>
            I will collect your basic details and then ask technical questions<br>
            based on your tech stack.<br><br>
            You can type <strong>exit</strong> anytime to end the conversation.
        </div>
    </div>
    """
    st.session_state.messages.append({"role": "assistant", "content": welcome_html})
    st.session_state.greeted = True

# 2. Add first question if not already there
if not st.session_state.candidate_collection_complete and st.session_state.current_field_index < len(CANDIDATE_FIELDS):
    field = CANDIDATE_FIELDS[st.session_state.current_field_index]
    question = FIELD_QUESTIONS[field]
    if not any(question in m["content"] for m in st.session_state.messages):
        st.session_state.messages.append({"role": "assistant", "content": question})

# 3. Handle technical question generation
if st.session_state.candidate_collection_complete and not st.session_state.technical_questions_generated:
    st.session_state.messages.append({"role": "assistant", "content": "Thank you for sharing your details! ✅\n\nLet's begin the technical screening."})
    st.session_state.technical_questions = generate_technical_questions(
        st.session_state.candidate_data.get("desired_role", ""),
        st.session_state.candidate_data.get("experience", ""),
        st.session_state.candidate_data.get("tech_stack", "")
    )
    st.session_state.technical_questions_generated = True

# 4. Handle technical question flow
if st.session_state.technical_questions_generated and st.session_state.current_tech_question_index < len(st.session_state.technical_questions):
    question = st.session_state.technical_questions[st.session_state.current_tech_question_index]
    if not any(question in m["content"] for m in st.session_state.messages):
        st.session_state.messages.append({"role": "assistant", "content": question})

# Display Chat History
for msg in st.session_state.messages:
    if "welcome-screen" in msg["content"]:
        st.markdown(msg["content"], unsafe_allow_html=True)
    else:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --------------------------------------------------
# User Input & Exit Handling Logic
# --------------------------------------------------

# Check if we should still show the input box
# It disappears if:
# 1. User typed 'exit' (exited is True)
# 2. All technical questions are answered (index reached total questions)
show_input = not st.session_state.exited and (
    not st.session_state.technical_questions_generated or 
    st.session_state.current_tech_question_index < len(st.session_state.technical_questions)
)

if show_input:
    user_input = st.chat_input("Type your response here...")
else:
    user_input = None

st.markdown('<div class="ts-footer">Powered by TalentScout Hiring Assistant</div>', unsafe_allow_html=True)

def validate_input(field, value):
    value = value.strip()
    if field == "full_name":
        parts = value.split()
        if len(parts) < 2: return False, "Please enter your full name (first and last)."
    elif field == "email":
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value): return False, "Invalid email address."
    elif field == "phone":
        if not value.isdigit() or not (10 <= len(value) <= 15): return False, "Enter 10–15 digits only."
    elif field == "experience":
        if not value.isdigit() or not (0 <= int(value) <= 50): return False, "Experience must be 0–50."
    elif field == "desired_role":
        if len(value) < 5: return False, "Enter full role name."
    elif field == "location":
        if len(value) < 4: return False, "Enter valid city."
    elif field == "tech_stack":
        if len(value.split(",")) < 1: return False, "List at least one technology."
    return True, ""

if user_input:
    user_text = user_input.lower().strip()
    if user_text in {"exit", "quit", "stop", "bye", "end"}:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({
            "role": "assistant", 
            "content": (
                "Thank you for your time! 🙏\n\n"
                "Our recruitment team will review your information \n"
                "and reach out with next steps."
            )
        })
        st.session_state.exited = True
        st.rerun()

    st.session_state.messages.append({"role": "user", "content": user_input})
    
    if not st.session_state.candidate_collection_complete:
        field = CANDIDATE_FIELDS[st.session_state.current_field_index]
        ok, err = validate_input(field, user_input)
        if not ok:
            st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {err}"})
        else:
            st.session_state.candidate_data[field] = user_input
            st.session_state.current_field_index += 1
            if st.session_state.current_field_index == len(CANDIDATE_FIELDS):
                st.session_state.candidate_collection_complete = True
        st.rerun()
    elif st.session_state.technical_questions_generated:
        st.session_state.technical_answers.append(user_input)
        st.session_state.current_tech_question_index += 1
        if st.session_state.current_tech_question_index == len(st.session_state.technical_questions):
            st.session_state.messages.append({
                "role": "assistant", 
                "content": (
                    "✅ **Technical screening completed.**\n\n"
                    "Thank you for answering the technical questions.\n"
                    "Our recruitment team will review your responses and "
                    "contact you if your profile matches the requirements.\n\n"
                    "Have a great day! 🙌"
                )
            })
        st.rerun()