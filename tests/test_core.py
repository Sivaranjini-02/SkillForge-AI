"""
SkillForge AI Test Suite
=========================
Comprehensive automated tests covering:
- Career Time-Traveler ETA recalculation
- HTML sanitization / XSS mitigation
- Profile validation bounds
- Default consensus schema integrity (4-agent war room)
- Diagnostic evaluation and 2-day micro-patch generation
- Hireability score parsing
- Career Blueprint Markdown export
- Progress calculations and edge cases
"""

import pytest
from core_logic import (
    sanitize_html,
    compute_time_traveler_eta,
    compute_progress_percentage,
    validate_profile_inputs,
    evaluate_diagnostic_answer,
    parse_hireability_score,
    get_default_consensus_data,
    generate_career_blueprint_md,
)


class TestSecurityAndSanitization:
    """Tests for input sanitization and XSS prevention."""

    def test_sanitize_html_escapes_script_tags(self):
        malicious = "<script>alert('xss')</script>"
        sanitized = sanitize_html(malicious)
        assert "<script>" not in sanitized
        assert "&lt;script&gt;" in sanitized

    def test_sanitize_html_escapes_quotes_and_attributes(self):
        payload = '"><img src=x onerror=alert(1)>'
        sanitized = sanitize_html(payload)
        assert "<img" not in sanitized
        assert "&quot;&gt;&lt;img" in sanitized

    def test_sanitize_html_handles_none_and_integers(self):
        assert sanitize_html(None) == ""
        assert sanitize_html(42) == "42"
        assert sanitize_html("") == ""

    def test_sanitize_html_handles_ampersands(self):
        assert "&amp;" in sanitize_html("A & B")


class TestValidation:
    """Tests for profile bounds and sanity checks."""

    def test_valid_profile_inputs(self):
        is_valid, err = validate_profile_inputs(
            name="Alex Rivera",
            skills="Python, SQL, HTML",
            certs="AWS Certified",
            hours=15,
        )
        assert is_valid is True
        assert err is None

    def test_empty_name_fails(self):
        is_valid, err = validate_profile_inputs(
            name="   ",
            skills="Python",
            certs="None",
            hours=15,
        )
        assert is_valid is False
        assert "name cannot be empty" in err.lower()

    def test_excessive_name_length(self):
        is_valid, err = validate_profile_inputs(
            name="A" * 105,
            skills="Python",
            certs="None",
            hours=15,
        )
        assert is_valid is False
        assert "exceeds maximum allowed length" in err.lower()

    def test_excessive_skills_length(self):
        is_valid, err = validate_profile_inputs(
            name="Alex",
            skills="S" * 1050,
            certs="None",
            hours=15,
        )
        assert is_valid is False
        assert "skills" in err.lower()

    def test_invalid_hours_out_of_bounds(self):
        is_valid, err = validate_profile_inputs("Alex", "Python", "Cert", 2)
        assert is_valid is False
        is_valid, err = validate_profile_inputs("Alex", "Python", "Cert", 50)
        assert is_valid is False


class TestCareerTimeTravelerAndProgress:
    """Tests for Career Time-Traveler formulas and progress tracking."""

    def test_time_traveler_eta_scaling(self):
        # High hours per week should result in fewer weeks
        weeks_fast, total_h1 = compute_time_traveler_eta(readiness_score=45, study_hours_per_week=30)
        weeks_slow, total_h2 = compute_time_traveler_eta(readiness_score=45, study_hours_per_week=10)
        assert total_h1 == total_h2
        assert weeks_fast < weeks_slow
        assert weeks_fast >= 2

    def test_time_traveler_eta_minimum_floor(self):
        weeks, _ = compute_time_traveler_eta(readiness_score=95, study_hours_per_week=40)
        assert weeks >= 2

    def test_time_traveler_eta_boundary_scores(self):
        weeks_0, h_0 = compute_time_traveler_eta(readiness_score=0, study_hours_per_week=15)
        weeks_100, h_100 = compute_time_traveler_eta(readiness_score=100, study_hours_per_week=15)
        assert weeks_0 > weeks_100
        assert h_0 > h_100

    def test_compute_progress_percentage(self):
        assert compute_progress_percentage(0, 4) == 0
        assert compute_progress_percentage(2, 4) == 50
        assert compute_progress_percentage(4, 4) == 100
        assert compute_progress_percentage(1, 0) == 0
        assert compute_progress_percentage(-1, 4) == 0
        assert compute_progress_percentage(5, 4) == 100


class TestDiagnosticQuizAndMicroPatch:
    """Tests for adaptive skill check and 2-day micro-patch generation."""

    def test_correct_answer_no_patch(self):
        is_correct, patch = evaluate_diagnostic_answer(
            selected_idx=1,
            correct_idx=1,
            skill_tested="React State Management",
        )
        assert is_correct is True
        assert patch is None

    def test_incorrect_answer_generates_2day_patch(self):
        is_correct, patch = evaluate_diagnostic_answer(
            selected_idx=0,
            correct_idx=1,
            skill_tested="JavaScript Async Event Loop",
        )
        assert is_correct is False
        assert patch is not None
        assert "2-Day Micro-Patch: JavaScript Async Event Loop" in patch["topic"]
        assert "48 hours" in patch["action"]


class TestHireabilityScoreParser:
    """Tests for score extraction from LLM evaluations."""

    def test_extract_hireability_score_standard(self):
        eval_md = "Great candidate! **Hireability Score: 88%**."
        assert parse_hireability_score(eval_md) == "88%"

    def test_extract_hireability_score_with_text_around(self):
        eval_md = "Rubric Result: 94% hire readiness achieved."
        assert parse_hireability_score(eval_md) == "94%"

    def test_fallback_when_no_score_found(self):
        eval_md = "Evaluated response thoroughly without numeric match."
        assert parse_hireability_score(eval_md) == "85%"

    def test_empty_string_fallback(self):
        assert parse_hireability_score("") == "85%"


class TestConsensusDataAndBlueprint:
    """Tests for multi-agent consensus data and Markdown blueprint export."""

    def test_consensus_data_structure(self):
        data = get_default_consensus_data(
            role="Full Stack Developer",
            hours=15,
            name="Alex Rivera",
        )
        assert "readiness_score" in data
        assert "strengths" in data
        assert "missing_skills" in data
        assert "skill_radar" in data
        assert "debate_transcript" in data
        assert "roadmap" in data
        assert "diagnostic_quiz" in data

        # Ensure Full Stack Developer role contains JavaScript, React, Node.js
        missing_str = " ".join(data["missing_skills"])
        assert "JavaScript" in missing_str
        assert "React" in missing_str
        assert "Node.js" in missing_str

        # Ensure 4-agent war room debate transcript has all 4 agents
        agents = [d["agent"] for d in data["debate_transcript"]]
        assert any("Skill-Analyzer" in a for a in agents)
        assert any("Curriculum-Architect" in a for a in agents)
        assert any("Pacing-Guardian" in a for a in agents)
        assert any("Assessment-Agent" in a for a in agents)

    def test_generate_career_blueprint_md(self):
        data = get_default_consensus_data("Full Stack Developer", 15, "Alex Rivera")
        patch = {
            "topic": "2-Day Micro-Patch: Async Event Loop",
            "reason": "Test diagnosis",
            "action": "48 hour review",
        }
        md = generate_career_blueprint_md(
            name="Alex Rivera",
            role="Full Stack Developer",
            hours=15,
            skills="Python, SQL",
            certs_str="SQL Cert",
            roadmap_data=data,
            completed_weeks=[1, 2],
            patch_module=patch,
            interview_q="Explain event loop in Node.js",
            interview_eval="Detailed rubric score 85%",
            interview_score="85%",
        )
        assert "# 🚀 SkillForge AI — Personalized Career Blueprint" in md
        assert "Alex Rivera" in md
        assert "Full Stack Developer" in md
        assert "Week 1" in md
        assert "[COMPLETED]" in md
        assert "2-Day Micro-Patch: Async Event Loop" in md
        assert "Explain event loop in Node.js" in md
        assert "85%" in md

    def test_generate_blueprint_without_patches_or_interviews(self):
        data = get_default_consensus_data("Data Scientist", 20, "Jordan Lee")
        md = generate_career_blueprint_md(
            name="Jordan Lee",
            role="Data Scientist",
            hours=20,
            skills="Python, Pandas",
            certs_str="DataCamp Cert",
            roadmap_data=data,
            completed_weeks=[],
            patch_module=None,
            interview_q=None,
            interview_eval=None,
            interview_score=None,
        )
        assert "Jordan Lee" in md
        assert "Data Scientist" in md
        assert "No active micro-patches required" in md
        assert "No scenario interview has been initiated" in md
