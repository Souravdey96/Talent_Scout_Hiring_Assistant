"""
llm.py
------
Hybrid rule-based technical question generator for TalentScout.
Returns a LIST of questions to be asked one at a time.
"""

def generate_technical_questions(desired_role, experience, tech_stack):
    """
    Generate 3–5 technical interview questions based on tech stack.
    """

    tech_stack = tech_stack.lower()

    QUESTION_BANK = {
        "mern": [
            "Explain the role of MongoDB in the MERN stack.",
            "How does React manage state and component lifecycle?",
            "What is middleware in Express.js and why is it important?",
            "How does Node.js handle asynchronous operations?",
            "How do REST APIs work in a MERN application?"
        ],
        "python": [
            "What are Python decorators?",
            "Explain list comprehensions with an example.",
            "What is the Global Interpreter Lock (GIL)?",
            "How does Python manage memory?",
            "What are generators in Python?"
        ],
        "sql": [
            "What is the difference between INNER JOIN and LEFT JOIN?",
            "Explain normalization in databases.",
            "What are indexes and why are they used?",
            "Explain ACID properties.",
            "What are window functions?"
        ]
    }

    questions = []

    for key in QUESTION_BANK:
        if key in tech_stack:
            questions.extend(QUESTION_BANK[key])

    # Fallback questions
    if not questions:
        questions = [
            "Explain a challenging technical problem you have solved.",
            "How do you ensure code quality in your projects?",
            "Describe your experience with system design."
        ]

    return questions[:5]   
