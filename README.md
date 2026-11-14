# 🚀 SkillForge AI: Agentic Learning & Career Navigator

> **Autonomous multi-agent career planning, real-time market alignment, adaptive curriculum generation & AI interview coaching powered by Streamlit and Google Gemini 3.8 Flash.**

---

## 🌟 Key Features

- **🤖 Multi-Agent "Debate & Consensus" War Room (`st.status`):**
  - **🔍 Skill-Analyzer Agent:** Benchmarks learner competencies against industry standards for target career roles.
  - **📚 Curriculum-Architect Agent:** Generates 4-week modular roadmaps with tutorials and milestone projects.
  - **⚖️ Pacing-Guardian Agent:** Audits workload against weekly study commitments to prevent burnout.
  - **🧠 Assessment-Agent:** Formulates diagnostic tests targeting primary critical skill gaps.
- **📊 Top KPI Row & Career Time-Traveler Simulation:**
  - Real-time **Role Match Readiness %**, **Missing Core Skills**, **Course Progress %**, and a live **Career Time-Traveler ETA** that recalculates immediately when weekly study hours change.
- **🎯 Competency Radar Chart (Tab 1):**
  - Dark-themed Plotly `Scatterpolar` radar chart comparing current skills vs target role requirements.
  - Verified Strengths and Identified High-Priority Skill Gaps cards.
- **🗺️ Personalized Learning Roadmap & Progress Tracker (Tab 2):**
  - Week-by-week interactive curriculum cards with checkboxes syncing to the live progress bar.
  - **🏆 Auto-Generated Proof-of-Work Pitch:** Generates copyable LinkedIn achievement posts and GitHub README project bullets based on completed milestones.
  - **📥 One-Click Career Blueprint Exporter:** Compiles complete learner profiles, roadmaps, and interview feedback into `SkillForge_Career_Blueprint.md`.
- **🧪 Adaptive Skill Check & 2-Day Micro-Patches (Tab 3):**
  - Diagnostic assessments targeting the #1 missing skill with automatic injection of 2-day micro-patch remediations upon missed questions.
- **💬 AI Career Mentor (Tab 4):**
  - Interactive chat advisor with suggested prompt pills and career strategy guidance.
- **🎤 AI Mock Interviewer & Hire-Readiness Gauntlet (Tab 5):**
  - High-stakes scenario challenges targeting missing skills.
  - Automated rubric evaluation returning a **Hireability Score (0–100%)**, key strengths, and concrete architectural improvement advice.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **AI & LLM Orchestration:** [Google GenAI SDK](https://github.com/google/generative-ai-python) (`gemini-3.8-flash`)
- **Data & Visualizations:** [Plotly](https://plotly.com/), [Pandas](https://pandas.pydata.org/)
- **Language:** Python 3.12+

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/skillforge-ai.git
cd skillforge-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`.

---

## 🔑 Configuration

Enter your **Google Gemini API Key** in the sidebar authentication input to unlock live Gemini 3.8 Flash synthesis, resume auto-fill, and interview coaching. (A built-in benchmark dataset is included for offline preview).

---

## 📄 License
MIT License. Created with ❤️ for aspiring engineers.
