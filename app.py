"""
TalentScout Hiring Assistant
----------------------------
Streamlit-based chatbot that performs initial candidate screening
and asks technical questions one at a time.
"""

import streamlit as st
import re
from utils import CANDIDATE_FIELDS, FIELD_QUESTIONS
from llm import generate_technical_questions

# --------------------------------------------------
# Validation Helpers
# --------------------------------------------------
def validate_input(field, value):
    value = value.strip()

    # ---------- FULL NAME ----------
    if field == "full_name":
        parts = value.split()
        if len(parts) < 2:
            return False, "Please enter your full name (first name and last name)."
        if any(len(p) < 2 for p in parts):
            return False, "Each part of your name must have at least 2 characters."

    # ---------- EMAIL ----------
    elif field == "email":
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            return False, "Please enter a valid email address."

    # ---------- PHONE ----------
    elif field == "phone":
        if not value.isdigit() or not (10 <= len(value) <= 15):
            return False, "Phone number must contain 10–15 digits only."

    # ---------- EXPERIENCE ----------
    elif field == "experience":
        if not value.isdigit() or not (0 <= int(value) <= 50):
            return False, "Experience must be a number between 0 and 50."

    # ---------- DESIRED ROLE ----------
    elif field == "desired_role":
        if len(value) < 5:
            return False, "Please enter the full role name (e.g., Data Analyst)."

        if value.isupper() and len(value) <= 4:
            return False, "Please avoid abbreviations. Enter the full role name."

    # ---------- LOCATION ----------
    elif field == "location":
        if len(value) < 4:
            return False, "Please enter a valid city name (e.g., Kolkata)."
        if not re.match(r"^[A-Za-z ]+$", value):
            return False, "Location should contain only letters."

    # ---------- TECH STACK ----------
    elif field == "tech_stack":
        if len(value.split(",")) < 1:
            return False, "Please list at least one technology."

    return True, ""



# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 TalentScout Hiring Assistant")
st.write(
    "Welcome! This assistant will help with the initial screening process "
    "by collecting your details and asking relevant technical questions."
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
    "exited": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# Stop app permanently if exited
# --------------------------------------------------
if st.session_state.exited:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    st.stop()

# --------------------------------------------------
# Greeting (once)
# --------------------------------------------------
if not st.session_state.greeted:
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "Hello! 👋 I'm **TalentScout**, your hiring assistant.\n\n"
            "I will collect your basic details and then ask technical questions "
            "based on your tech stack.\n\n"
            "You can type **exit** anytime to end the conversation."
        )
    })
    st.session_state.greeted = True

# --------------------------------------------------
# Ask candidate detail question
# --------------------------------------------------
if (
    not st.session_state.candidate_collection_complete
    and st.session_state.current_field_index < len(CANDIDATE_FIELDS)
):
    field = CANDIDATE_FIELDS[st.session_state.current_field_index]
    question = FIELD_QUESTIONS[field]

    if not any(m["content"] == question for m in st.session_state.messages):
        st.session_state.messages.append({
            "role": "assistant",
            "content": question
        })

# --------------------------------------------------
# Generate technical questions (ONCE)
# --------------------------------------------------
if (
    st.session_state.candidate_collection_complete
    and not st.session_state.technical_questions_generated
):
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "Thank you for sharing your details! ✅\n\n"
            "Let's begin with the technical questions."
        )
    })

    st.session_state.technical_questions = generate_technical_questions(
        desired_role=st.session_state.candidate_data.get("desired_role", ""),
        experience=st.session_state.candidate_data.get("experience", ""),
        tech_stack=st.session_state.candidate_data.get("tech_stack", "")
    )

    st.session_state.technical_questions_generated = True

# --------------------------------------------------
# Ask ONE technical question
# --------------------------------------------------
if (
    st.session_state.technical_questions_generated
    and st.session_state.current_tech_question_index < len(st.session_state.technical_questions)
):
    question = st.session_state.technical_questions[
        st.session_state.current_tech_question_index
    ]

    if not any(m["content"] == question for m in st.session_state.messages):
        st.session_state.messages.append({
            "role": "assistant",
            "content": question
        })

# --------------------------------------------------
# Display chat history
# --------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --------------------------------------------------
# User Input
# --------------------------------------------------
EXIT_KEYWORDS = {"exit", "quit", "bye", "stop", "end"}
user_input = st.chat_input("Type your response here...")

if user_input:
    user_text = user_input.strip().lower()

    # ---------------- EXIT ----------------
    if user_text in EXIT_KEYWORDS:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "Thank you for your time! 🙏\n\n"
                "Our recruitment team will review your information "
                "and reach out with next steps."
            )
        })
        st.session_state.exited = True
        st.rerun()

    # Normal user input
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # -------- Candidate phase (with validation) --------
    if not st.session_state.candidate_collection_complete:
        field = CANDIDATE_FIELDS[st.session_state.current_field_index]
        is_valid, error_msg = validate_input(field, user_input)

        if not is_valid:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ {error_msg}"
            })
            st.rerun()

        st.session_state.candidate_data[field] = user_input
        st.session_state.current_field_index += 1

        if st.session_state.current_field_index == len(CANDIDATE_FIELDS):
            st.session_state.candidate_collection_complete = True

        st.rerun()

    # -------- Technical phase --------
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
