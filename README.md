# Talent_Scout_Hiring_Assistant
🤖 TalentScout Hiring Assistant

An intelligent, Streamlit-powered recruitment assistant designed to automate the initial screening of technical candidates. The system gathers candidate profiles and generates tailored technical interview questions based on their specific tech stack.
📖 Project Overview

The TalentScout Hiring Assistant streamlines the top-of-funnel recruitment process for technical roles. It interacts with candidates via a high-end, responsive chat interface to collect essential professional data and conducts a preliminary technical assessment.
Key Features

    Modular Architecture: Separate logic for UI, LLM question generation, and utility constants.

    Dynamic Information Gathering: Sequentially collects name, contact info, experience, role, and tech stack.

    Intelligent Technical Assessment: Generates 3-5 custom questions tailored to the candidate's proficiency in specific technologies (e.g., Python, MERN, SQL).

    Theme-Responsive UI: Supports both Light and Dark modes with specialized CSS for improved visibility.

    Graceful Session Management: UI elements like the chat input and assistant icons dynamically disappear upon interview completion or exit.

🚀 Installation & Setup
1. Clone the Repository
Bash

git clone <your-repository-url>
cd Hiring_Assistant_Chatbot

2. Install Dependencies
Bash

pip install -r requirements.txt

3. Configure Environment Variables

Copy the .env.example file to create a local .env and add your API credentials.
Bash

cp .env.example .env

Note: Ensure .env is listed in your .gitignore to protect sensitive data.

4. Initialize the Model

Run the model creation script once to generate the local .pkl weights.
Bash

python flan_t5_model_pkl.py

5. Launch the Application
Bash

streamlit run app.py

🏗️ Technical Details
Architecture

The project follows a modular design pattern to ensure scalability and maintainability:

    app.py: The core Streamlit interface managing session state, conversation flow, and custom styling.

    llm.py: Contains the hybrid question generation engine utilizing a pre-defined bank for common stacks and a fallback for diverse technologies.

    prompts.py: Houses specialized prompt templates designed for technical interviewing.

    utils.py: Centralized configuration for candidate fields and standard validation logic.

Model Details

    Model: Google's Flan-T5-Base.

    Type: Text-to-Text generation model.

    Role: Used for technical question generation when the keyword-based question bank does not cover a specific candidate tech stack.

🎯 Prompt Design

The prompts used in this assistant are crafted based on professional Prompt Engineering principles:

    Persona-Based Prompting: We assigned the LLM the role of a "Senior Technical Interviewer" in prompts.py to ensure high-quality, professional, and strictly technical outputs.

    Instructional Constraints: The prompt explicitly forbids HR-style or personal questions, keeping the focus entirely on technical assessment.

    Few-Shot Strategy: The prompt includes specific formatting instructions and an example format to minimize non-deterministic behavior and hallucinations.

🛡️ Data Privacy & Best Practices

In compliance with GDPR and the assignment's privacy criteria, the system implements several protection layers:

    Secret Management: Sensitive API keys are managed through .env files and Streamlit Secrets, ensuring they are never exposed in public repositories.

    Anonymized Backend Processing: Personal information is handled programmatically and is not stored in public logs.

    Data Retention: Candidates are informed of how their data will be reviewed, and session state is cleared upon exit.

🛠️ Challenges & Solutions
Challenge	Solution
"Jump-to-Top" Robot Icon	Implemented conditional CSS logic that hides chat avatars globally once the exited state is triggered.
Typing Visibility	Created theme-responsive CSS that switches text and caret colors to ensure visibility in both light and dark backgrounds.
Clean Exit UI	Designed an if show_input check that physically removes the st.chat_input widget when the screening is completed.

📄 License

This project is licensed under the MIT License.
