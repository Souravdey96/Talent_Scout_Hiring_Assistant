"""
utils.py
--------
Utility constants and helper structures for the TalentScout chatbot.
"""

# Ordered list of candidate fields to collect
CANDIDATE_FIELDS = [
    "full_name",
    "email",
    "phone",
    "experience",
    "desired_role",
    "location",
    "tech_stack",
]

# Corresponding questions for each field
FIELD_QUESTIONS = {
    "full_name": "What is your full name?",
    "email": "What is your email address?",
    "phone": "What is your phone number?",
    "experience": "How many years of professional experience do you have?",
    "desired_role": "What position(s) are you applying for?",
    "location": "What is your current location?",
    "tech_stack": (
        "Please list your tech stack (languages, frameworks, databases, tools).\n"
        "Example: Python, Django, PostgreSQL, Docker"
    ),
}
