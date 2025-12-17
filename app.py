"""
TalentScout Hiring Assistant
----------------------------
Streamlit-based chatbot that performs initial candidate screening
by collecting candidate details in a structured conversational flow.
"""

import streamlit as st
from utils import CANDIDATE_FIELDS, FIELD_QUESTIONS

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
if "messages" not in st.session_state:
    st.session_state.messages = []

if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}

if "current_field_index" not in st.session_state:
    st.session_state.current_field_index = 0

if "greeted" not in st.session_state:
    st.session_state.greeted = False

if "candidate_collection_complete" not in st.session_state:
    st.session_state.candidate_collection_complete = False

if "technical_questions_generated" not in st.session_state:
    st.session_state.technical_questions_generated = False

if "technical_questions" not in st.session_state:
    st.session_state.technical_questions = ""


# --------------------------------------------------
# Greeting (shown once)
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
# Ask FIRST / NEXT Question (BEFORE user input)
# --------------------------------------------------
if (
    not st.session_state.candidate_collection_complete
    and st.session_state.current_field_index < len(CANDIDATE_FIELDS)
):
    field = CANDIDATE_FIELDS[st.session_state.current_field_index]
    question = FIELD_QUESTIONS[field]

    if not any(msg["content"] == question for msg in st.session_state.messages):
        st.session_state.messages.append({
            "role": "assistant",
            "content": question
        })

# --------------------------------------------------
# Display Chat History
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

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    if user_text in EXIT_KEYWORDS:
        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "Thank you for your time! 🙏\n\n"
                "Our recruitment team will review your information "
                "and reach out with next steps."
            )
        })
        st.stop()

    if (
        not st.session_state.candidate_collection_complete
        and st.session_state.current_field_index < len(CANDIDATE_FIELDS)
    ):
        field_name = CANDIDATE_FIELDS[st.session_state.current_field_index]
        st.session_state.candidate_data[field_name] = user_input
        st.session_state.current_field_index += 1

        if st.session_state.current_field_index == len(CANDIDATE_FIELDS):
            st.session_state.candidate_collection_complete = True

    st.rerun()

# --------------------------------------------------
# Completion Message (shown once after tech stack)
# --------------------------------------------------
if st.session_state.candidate_collection_complete:
    completion_message = (
        "Thank you for sharing your details! ✅\n\n"
        "I will now ask you a few technical questions "
        "based on your declared tech stack."
    )

    if not any(
        msg["content"] == completion_message
        for msg in st.session_state.messages
    ):
        st.session_state.messages.append({
            "role": "assistant",
            "content": completion_message
        })
        st.rerun()

# --------------------------------------------------
# Generate Technical Questions using LLM (once)
# --------------------------------------------------
if (
    st.session_state.candidate_collection_complete
    and not st.session_state.technical_questions_generated
):
    from llm import generate_technical_questions

    try:
        tech_questions = generate_technical_questions(
            desired_role=st.session_state.candidate_data.get("desired_role", ""),
            experience=st.session_state.candidate_data.get("experience", ""),
            tech_stack=st.session_state.candidate_data.get("tech_stack", "")
        )

        st.session_state.technical_questions = tech_questions
        st.session_state.technical_questions_generated = True

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Here are your technical questions:\n\n{tech_questions}"
        })

    except Exception as e:
        st.session_state.messages.append({
        "role": "assistant",
        "content": f"⚠️ Error while generating questions: {str(e)}"
    })

    st.rerun()

