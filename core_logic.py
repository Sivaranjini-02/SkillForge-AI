"""
SkillForge AI Core Logic Module
================================
Provides core business logic, accessibility-safe HTML sanitization, 
dynamic Career Time-Traveler calculations, validation, and Markdown report synthesis.
"""

from typing import Dict, List, Any, Optional, Tuple
import html
import re
from datetime import datetime


def sanitize_html(text: Any) -> str:
    """
    Sanitize text against Cross-Site Scripting (XSS) before embedding into HTML.
    
    Args:
        text: Any object or string to be escaped.
        
    Returns:
        HTML-escaped string safe for DOM interpolation.
    """
    if text is None:
        return ""
    return html.escape(str(text), quote=True)


def compute_time_traveler_eta(readiness_score: int, study_hours_per_week: int) -> Tuple[int, int]:
    """
    Dynamically recalculate estimated weeks to career readiness based on study velocity.
    
    Formula:
        Total hours to close gap = max(35, int((92 - readiness_score) * 3.6))
        Estimated weeks = max(2, round(total_gap_hours / study_hours_per_week))
        
    Args:
        readiness_score: Candidate readiness percentage (0-100).
        study_hours_per_week: Weekly study commitment (5-40).
        
    Returns:
        Tuple of (estimated_weeks, total_gap_hours).
    """
    safe_score = max(0, min(100, int(readiness_score)))
    safe_hours = max(1, int(study_hours_per_week))
    total_gap_hours = max(35, int((92 - safe_score) * 3.6))
    estimated_weeks = max(2, round(total_gap_hours / safe_hours))
    return estimated_weeks, total_gap_hours


def compute_progress_percentage(completed_count: int, total_count: int) -> int:
    """
    Calculate progress percentage between 0 and 100.
    
    Args:
        completed_count: Number of completed items.
        total_count: Total items.
        
    Returns:
        Integer percentage (0-100).
    """
    if total_count <= 0:
        return 0
    return max(0, min(100, int((completed_count / total_count) * 100)))


def validate_profile_inputs(
    name: str,
    skills: str,
    certs: str,
    hours: int,
) -> Tuple[bool, Optional[str]]:
    """
    Validate learner profile fields against length bounds and sanity checks.
    
    Args:
        name: Learner full name.
        skills: Current skills string.
        certs: Certifications/projects string.
        hours: Weekly hours (5-40).
        
    Returns:
        Tuple of (is_valid: bool, error_message: Optional[str]).
    """
    if not name or not name.strip():
        return False, "Candidate name cannot be empty."
    if len(name) > 100:
        return False, "Candidate name exceeds maximum allowed length of 100 characters."
    if len(skills) > 1000:
        return False, "Skills field exceeds maximum allowed length of 1000 characters."
    if len(certs) > 1000:
        return False, "Certifications field exceeds maximum allowed length of 1000 characters."
    if hours < 5 or hours > 40:
        return False, "Weekly study hours must be between 5 and 40."
    return True, None


def evaluate_diagnostic_answer(
    selected_idx: int,
    correct_idx: int,
    skill_tested: str,
) -> Tuple[bool, Optional[Dict[str, str]]]:
    """
    Evaluate a candidate's diagnostic quiz selection and generate a micro-patch if incorrect.
    
    Args:
        selected_idx: Index of chosen option.
        correct_idx: Index of ground truth answer.
        skill_tested: Topic or skill tested.
        
    Returns:
        Tuple of (is_correct, patch_module_dict_or_None).
    """
    is_correct = selected_idx == correct_idx
    if is_correct:
        return True, None
    
    patch = {
        "topic": f"2-Day Micro-Patch: {skill_tested}",
        "reason": f"Misconception identified during assessment of {skill_tested}.",
        "action": f"Dedicate 48 hours to reviewing fundamentals of {skill_tested} before tackling production-scale features.",
    }
    return False, patch


def parse_hireability_score(eval_text: str) -> str:
    """
    Extract a percentage hireability score from hiring manager evaluation markdown.
    
    Args:
        eval_text: Raw markdown evaluation output.
        
    Returns:
        String percentage score (e.g. '85%').
    """
    if not eval_text:
        return "85%"
    match = re.search(r"(\d{1,3})%", eval_text)
    if match:
        score_int = int(match.group(1))
        if 0 <= score_int <= 100:
            return f"{score_int}%"
    return "85%"


def get_default_consensus_data(role: str, hours: int, name: str) -> Dict[str, Any]:
    """
    Generate calibrated default consensus dataset adhering strictly to multi-agent schema.
    
    Args:
        role: Target career role.
        hours: Weekly study hours.
        name: Candidate name.
        
    Returns:
        Dictionary with readiness_score, strengths, missing_skills, skill_radar,
        debate_transcript, roadmap, and diagnostic_quiz.
    """
    clean_name = sanitize_html(name)
    clean_role = sanitize_html(role)
    
    return {
        "readiness_score": 45,
        "strengths": [
            "Python Programming & Automation",
            "Relational Database Design (SQL)",
            "Semantic HTML & Basic Web Structure",
        ],
        "missing_skills": [
            "JavaScript (ES6+)",
            "React Component Architecture",
            "Node.js & Express REST APIs",
            "Full-Stack State Management",
            "Containerization & Docker",
        ],
        "skill_radar": {
            "Frontend (React & JS)": {"current": 25, "required": 85},
            "Backend (Node & Python APIs)": {"current": 55, "required": 85},
            "Database & SQL Architecture": {"current": 70, "required": 80},
            "System & API Design": {"current": 30, "required": 75},
            "DevOps, Git & Deployment": {"current": 35, "required": 70},
        },
        "debate_transcript": [
            {
                "agent": "🔍 Skill-Analyzer Agent",
                "role": "Skill Gap Diagnostic",
                "message": f"Audited {clean_name}'s profile against {clean_role} industry standards. Found solid Python and SQL fundamentals, but identified critical missing skills: JavaScript, React, and Node.js are essential for full-stack competency.",
            },
            {
                "agent": "📚 Curriculum-Architect Agent",
                "role": "Syllabus Architect",
                "message": "Proposed an intensive 4-week full-stack acceleration curriculum covering Modern JavaScript, React 19 architecture, Node/Express microservices, and end-to-end cloud deployment. Initial workload estimate: 25 hrs/week.",
            },
            {
                "agent": "⚖️ Pacing-Guardian Agent",
                "role": "Workload & Pacing Auditor",
                "message": f"Workload conflict detected! Learner committed to {hours} hours/week. A 25-hour schedule risks severe burnout and drop-off. Negotiating down: pruning GraphQL and complex microservices, streamlining projects into focused {hours}-hour high-impact deliverables.",
            },
            {
                "agent": "🧠 Assessment-Agent",
                "role": "Validation & Diagnostic Lead",
                "message": "Consensus ratified with adjusted pacing. I have structured a diagnostic skill check targeting the #1 critical gap (JavaScript Async Event Loop & Promises) to benchmark foundational readiness before Week 1.",
            },
        ],
        "roadmap": [
            {
                "week": 1,
                "focus_skill": "Modern JavaScript (ES6+) & DOM",
                "topic": "Async/Await, Promises, Closures, Fetch API & Modern Web Fundamentals",
                "course_tutorial": "MDN JavaScript Learning Path & FullStackOpen Part 1",
                "hands_on_project": "Build an asynchronous crypto/currency tracker with live data feeds",
            },
            {
                "week": 2,
                "focus_skill": "React Component Architecture",
                "topic": "React 19 Hooks (useState, useEffect, useMemo), Props & Dynamic Component Trees",
                "course_tutorial": "Official React Documentation (react.dev) & Epic React Core",
                "hands_on_project": "Develop a responsive Kanban task board with interactive drag-and-drop state",
            },
            {
                "week": 3,
                "focus_skill": "Node.js & Express REST APIs",
                "topic": "Express Middleware, Routing Architecture, JWT Authentication & PostgreSQL ORM",
                "course_tutorial": "The Odin Project NodeJS Course & Express.js Production Guide",
                "hands_on_project": "Architect a secure multi-tenant Task Management REST API with token auth",
            },
            {
                "week": 4,
                "focus_skill": "Full-Stack Integration & Deployment",
                "topic": "Connecting React with Express API, CORS, Environment Security & Containerization",
                "course_tutorial": "FullStackOpen Part 3 & Docker Getting Started Guide",
                "hands_on_project": "Containerize and deploy an integrated full-stack app on Cloud Run or Render",
            },
        ],
        "diagnostic_quiz": {
            "skill_tested": "JavaScript Async Event Loop & Promises",
            "question": "In JavaScript, if a Promise resolves and a setTimeout with 0ms delay are both queued, which executes first and why?",
            "options": [
                "setTimeout executes first because timers take precedence in the execution stack",
                "Promise callback executes first because the microtask queue is prioritized before the macrotask queue",
                "They execute in nondeterministic order depending on browser CPU load",
                "Both execute simultaneously across separate parallel worker threads",
            ],
            "correct_answer": 1,
            "explanation": "Promises schedule callbacks in the microtask queue, which is completely emptied before the event loop picks up macrotasks (such as setTimeout timers).",
        },
    }


def generate_career_blueprint_md(
    name: str,
    role: str,
    hours: int,
    skills: str,
    certs_str: str,
    roadmap_data: Dict[str, Any],
    completed_weeks: List[int],
    patch_module: Optional[Dict[str, str]],
    interview_q: Optional[str],
    interview_eval: Optional[str],
    interview_score: Optional[str],
) -> str:
    """
    Compile candidate metrics, roadmap, patches, and interview results into a Markdown report.
    """
    readiness = roadmap_data.get("readiness_score", 45)
    missing = roadmap_data.get("missing_skills", [])
    strengths = roadmap_data.get("strengths", [])
    roadmap = roadmap_data.get("roadmap", [])
    eta_weeks, total_gap_hours = compute_time_traveler_eta(readiness, hours)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = [
        f"# 🚀 SkillForge AI — Personalized Career Blueprint",
        f"*Generated on {now_str} | Candidate: **{name}***\n",
        f"---\n",
        f"## 👤 1. Learner Profile & Career Target",
        f"- **Candidate Name:** {name}",
        f"- **Target Role:** {role}",
        f"- **Weekly Study Commitment:** {hours} Hours / Week",
        f"- **Current Skill Assets:** {skills}",
        f"- **Credentials & Portfolio:** {certs_str}\n",
        f"## 📊 2. Benchmarking & Readiness Metrics",
        f"- **Role Match Readiness:** {readiness}% (Target Industry Benchmark: 85%+)",
        f"- **Missing Core Competencies:** {len(missing)} Critical Gaps",
        f"- **Career Time-Traveler ETA:** ~{eta_weeks} Weeks (@ {hours} hrs/wk, ~{total_gap_hours}h total study)",
        f"- **Course Progress:** {len(completed_weeks)} / {len(roadmap)} Weeks Completed\n",
        f"### ✅ Verified Strengths",
    ]
    for s in strengths:
        md.append(f"- {s}")
    md.append("")

    md.append(f"### ⚠️ Identified Skill Gaps (High Priority)")
    for m in missing:
        md.append(f"- {m}")
    md.append("")

    md.append(f"## 🗺️ 3. 4-Week Actionable Learning Roadmap")
    for w in roadmap:
        w_num = w.get("week", 1)
        is_done = " [COMPLETED]" if w_num in completed_weeks else " [IN PROGRESS]"
        md.append(f"### Week {w_num}: {w.get('focus_skill', 'Core Skill')}{is_done}")
        md.append(f"- **Core Topic:** {w.get('topic', '')}")
        md.append(f"- **Recommended Course / Tutorial:** {w.get('course_tutorial', '')}")
        md.append(f"- **Hands-On Practical Milestone:** {w.get('hands_on_project', '')}")
        md.append("")

    md.append(f"## 🔧 4. Adaptive 2-Day Micro-Patches (Remediation)")
    if patch_module:
        md.append(f"- **Triggered Patch Topic:** {patch_module.get('topic', 'Diagnostic Remediation')}")
        md.append(f"- **Diagnosis:** {patch_module.get('reason', '')}")
        md.append(f"- **Prescribed 2-Day Action:** {patch_module.get('action', '')}\n")
    else:
        md.append(f"*✅ No active micro-patches required — foundational diagnostic checks validated.*\n")

    md.append(f"## 🎤 5. AI Mock Interview & Hireability Gauntlet")
    if interview_q:
        md.append(f"### Scenario Challenge Question:")
        md.append(f"> {interview_q}\n")
        if interview_eval:
            if interview_score:
                md.append(f"**Hireability Score:** {interview_score}\n")
            md.append(f"### Evaluation & Hiring Panel Rubric:")
            md.append(f"{interview_eval}\n")
        else:
            md.append(f"*Candidate response pending evaluation.*\n")
    else:
        md.append(f"*No scenario interview has been initiated yet.*\n")

    md.append(f"---\n")
    md.append(f"*Exported by SkillForge AI • Multi-Agent Autonomous Career Navigator*")

    return "\n".join(md)
