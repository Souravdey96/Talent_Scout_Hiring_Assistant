# Talent_Scout_Hiring_Assistant
🤖 TalentScout Hiring Assistant

An intelligent, Streamlit-powered recruitment assistant designed to automate the initial screening of technical candidates. The system gathers candidate profiles and generates tailored technical interview questions based on their specific tech stack.
📖 Project Overview

The TalentScout Hiring Assistant streamlines the top-of-funnel recruitment process for technical roles. It interacts with candidates via a high-end, responsive chat interface to collect essential professional data and conducts a preliminary technical assessment.
🚀 Installation & Setup

    Clone the Repository
    Bash

git clone https://github.com/Souravdey96/Talent_Scout_Hiring_Assistant.git
cd Talent_Scout_Hiring_Assistant

Install Dependencies
Bash

pip install -r requirements.txt

Configure Environment Variables Create a .env file and add your Hugging Face API credentials:
Bash

HF_API_KEY=your_key_here

Launch the Application
Bash

    streamlit run app.py

🏗️ Technical Architecture

The project follows a Decoupled Cloud-Native Design to ensure scalability and stay within hosting resource limits.

    app.py: Core Streamlit interface managing session state and custom CSS.

    llm.py: Hybrid question generation engine utilizing the Hugging Face Inference API.

    utils.py: Centralized validation logic (Regex/Digit checks) and field configurations.

🎯 Prompt Design

    Persona-Based Prompting: Assigned the LLM the role of a "Senior Technical Interviewer" to ensure professional, high-quality output.

    Few-Shot Strategy: Included example formatting within the system prompt to minimize hallucinations.

🛠️ Challenges & Solutions
Challenge	Technical Solution
1GB RAM Baseline Limit	Pivoted to a Cloud-Native Inference strategy using the Hugging Face API to offload model computation, keeping local memory usage under 250MB.
GitHub 100MB File Limit	Integrated Git LFS (Large File Storage) to version control the 990MB model weights while keeping the repository lightweight.
Divergent Git History	Resolved complex merge conflicts and "non-fast-forward" errors during deployment using git rebase and stash workflows.
Strict Data Validation	Implemented Python-based logic to enforce exactly 10-digit phone inputs, preventing malformed data from reaching the LLM.
Theme-Responsive UI	Created specialized CSS that switches text/caret colors dynamically to ensure visibility in both light and dark backgrounds.
🛡️ Data Privacy & Best Practices

    Secret Management: Sensitive API keys are managed through Streamlit Secrets and .env files.

    Session Management: UI elements (chat input/icons) are dynamically cleared upon interview completion or exit to ensure a clean user experience.

📄 License

This project is licensed under the MIT License.
