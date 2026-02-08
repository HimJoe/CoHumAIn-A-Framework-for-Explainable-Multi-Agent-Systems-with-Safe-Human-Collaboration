"""
Tests for CoHumAIn Framework core functionality
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cohumain.framework import (
    Agent,
    CoHumAInFramework,
    ExplanationLevel,
    AutomationLevel,
    SafetyStatus,
    CoordinationDecision,
    CollectiveExplanation,
    SafetyAssessment,
)


# ---------------------------------------------------------------------------
# Agent tests
# ---------------------------------------------------------------------------

class TestAgent:
    def _make_agent(self, **overrides):
        defaults = dict(
            name="TestAgent",
            role="Tester",
            expertise=0.85,
            confidence_threshold=0.80,
            capabilities=["Testing"],
            constitutional_principles=["Be safe"],
        )
        defaults.update(overrides)
        return Agent(**defaults)

    def test_agent_creation(self):
        agent = self._make_agent()
        assert agent.name == "TestAgent"
        assert agent.role == "Tester"
        assert agent.expertise == 0.85
        assert agent.confidence_threshold == 0.80
        assert "Testing" in agent.capabilities
        assert len(agent.task_history) == 0

    def test_agent_performance_metrics_initialised(self):
        agent = self._make_agent()
        assert agent.performance_metrics["accuracy"] == 0.0
        assert agent.performance_metrics["avg_confidence"] == 0.0
        assert agent.performance_metrics["tasks_completed"] == 0

    def test_generate_reasoning_trace(self):
        agent = self._make_agent()
        trace = agent.generate_reasoning_trace("Do a test", {})
        assert trace["agent"] == "TestAgent"
        assert trace["task"] == "Do a test"
        assert "confidence" in trace
        assert "constitutional_check" in trace
        assert "timestamp" in trace

    def test_reasoning_trace_appended_to_history(self):
        agent = self._make_agent()
        agent.generate_reasoning_trace("task1", {})
        agent.generate_reasoning_trace("task2", {})
        assert len(agent.task_history) == 2

    def test_confidence_reduced_for_high_complexity(self):
        agent = self._make_agent(expertise=0.90)
        trace_normal = agent.generate_reasoning_trace("t", {})
        trace_high = agent.generate_reasoning_trace("t", {"complexity": "high"})
        assert trace_high["confidence"] <= trace_normal["confidence"]

    def test_confidence_capped_at_one(self):
        agent = self._make_agent(expertise=1.0)
        trace = agent.generate_reasoning_trace("t", {})
        assert trace["confidence"] <= 1.0

    def test_check_principles_all_satisfied(self):
        agent = self._make_agent()
        result = agent._check_principles("safe task")
        assert result["all_satisfied"] is True
        assert result["violations"] == []


# ---------------------------------------------------------------------------
# Framework tests
# ---------------------------------------------------------------------------

class TestCoHumAInFramework:
    def _make_framework(self, **overrides):
        defaults = dict(
            domain="general",
            safety_mode="balanced",
        )
        defaults.update(overrides)
        fw = CoHumAInFramework(**defaults)
        return fw

    def _make_team(self):
        fw = self._make_framework()
        fw.add_agents([
            Agent("Alice", "Coder", 0.90, 0.80, ["Code"], ["Be safe"]),
            Agent("Bob", "Reviewer", 0.85, 0.80, ["Review"], ["Be thorough"]),
        ])
        return fw

    # -- agent management --

    def test_add_agent(self):
        fw = self._make_framework()
        a = Agent("A", "R", 0.9, 0.8, [], [])
        fw.add_agent(a)
        assert len(fw.agents) == 1

    def test_add_agents(self):
        fw = self._make_framework()
        fw.add_agents([
            Agent("A", "R", 0.9, 0.8, [], []),
            Agent("B", "R", 0.8, 0.8, [], []),
        ])
        assert len(fw.agents) == 2

    # -- confidence thresholds --

    def test_confidence_threshold_permissive(self):
        fw = self._make_framework(safety_mode="permissive")
        assert fw.confidence_threshold == 0.70

    def test_confidence_threshold_balanced(self):
        fw = self._make_framework(safety_mode="balanced")
        assert fw.confidence_threshold == 0.80

    def test_confidence_threshold_strict(self):
        fw = self._make_framework(safety_mode="strict")
        assert fw.confidence_threshold == 0.90

    def test_confidence_threshold_maximum(self):
        fw = self._make_framework(safety_mode="maximum")
        assert fw.confidence_threshold == 0.95

    def test_confidence_threshold_unknown_defaults(self):
        fw = self._make_framework(safety_mode="unknown")
        assert fw.confidence_threshold == 0.80

    # -- task execution --

    def test_execute_task_returns_all_keys(self):
        fw = self._make_team()
        result = fw.execute_task("Test task")
        expected_keys = {
            "task", "success", "level1_explanations",
            "level2_explanations", "level3_explanation",
            "safety_assessment", "automation_level",
            "requires_human_review", "intervention_reason",
            "execution_time", "timestamp",
        }
        assert expected_keys.issubset(result.keys())

    def test_execute_task_level1_per_agent(self):
        fw = self._make_team()
        result = fw.execute_task("Task")
        assert len(result["level1_explanations"]) == 2

    def test_execute_task_recorded_in_history(self):
        fw = self._make_team()
        fw.execute_task("Task A")
        fw.execute_task("Task B")
        assert len(fw.task_history) == 2

    def test_execute_task_human_in_loop_forces_review(self):
        fw = self._make_team()
        result = fw.execute_task("Task", human_in_loop=True)
        assert result["requires_human_review"] is True

    def test_execute_task_success_when_safe(self):
        fw = self._make_team()
        result = fw.execute_task("Safe task")
        assert result["success"] is True

    # -- coordination --

    def test_delegation_triggered_when_low_confidence(self):
        fw = self._make_framework(safety_mode="maximum")  # threshold 0.95
        fw.add_agents([
            Agent("Low", "R", 0.60, 0.50, [], []),
            Agent("High", "R", 0.99, 0.90, [], []),
        ])
        result = fw.execute_task("task")
        delegation_decisions = [
            c for c in result["level2_explanations"]
            if c.decision_type == "delegation"
        ]
        assert len(delegation_decisions) >= 1

    def test_conflict_resolution_on_variance(self):
        fw = self._make_framework()
        fw.add_agents([
            Agent("Sure", "R", 0.99, 0.80, [], []),
            Agent("Unsure", "R", 0.50, 0.80, [], []),
        ])
        result = fw.execute_task("task")
        conflict_decisions = [
            c for c in result["level2_explanations"]
            if c.decision_type == "conflict_resolution"
        ]
        assert len(conflict_decisions) >= 1

    # -- safety assessment --

    def test_safety_status_safe_when_no_violations(self):
        fw = self._make_team()
        result = fw.execute_task("task")
        assert result["safety_assessment"].status == SafetyStatus.SAFE

    def test_safety_assessment_has_responsible_agents(self):
        fw = self._make_team()
        result = fw.execute_task("task")
        assert "Alice" in result["safety_assessment"].responsible_agents
        assert "Bob" in result["safety_assessment"].responsible_agents

    # -- trust calibration --

    def test_high_stakes_forces_in_the_loop(self):
        fw = self._make_team()
        result = fw.execute_task("task", context={"stakes": "high"})
        assert result["automation_level"] == AutomationLevel.IN_THE_LOOP.value

    def test_automation_level_is_string(self):
        fw = self._make_team()
        result = fw.execute_task("task")
        assert isinstance(result["automation_level"], str)

    # -- collective explanation --

    def test_collective_explanation_type(self):
        fw = self._make_team()
        result = fw.execute_task("task")
        assert isinstance(result["level3_explanation"], CollectiveExplanation)

    def test_collective_explanation_has_contributions(self):
        fw = self._make_team()
        result = fw.execute_task("task")
        ce = result["level3_explanation"]
        assert "Alice" in ce.agent_contributions
        assert "Bob" in ce.agent_contributions

    def test_collective_explanation_has_timeline(self):
        fw = self._make_team()
        result = fw.execute_task("task")
        assert len(result["level3_explanation"].temporal_timeline) == 2

    def test_collective_confidence_in_range(self):
        fw = self._make_team()
        result = fw.execute_task("task")
        cc = result["level3_explanation"].collective_confidence
        assert 0.0 <= cc <= 1.0

    # -- compliance report --

    def test_compliance_report_json(self):
        fw = self._make_team()
        fw.execute_task("task")
        report_str = fw.generate_compliance_report(standard="test", format="json")
        import json
        report = json.loads(report_str)
        assert report["framework"] == "CoHumAIn"
        assert report["standard"] == "test"
        assert report["total_tasks"] == 1

    def test_compliance_report_non_json(self):
        fw = self._make_team()
        report_str = fw.generate_compliance_report(format="text")
        assert isinstance(report_str, str)

    # -- performance summary --

    def test_agent_performance_summary(self):
        fw = self._make_team()
        df = fw.get_agent_performance_summary()
        assert len(df) == 2
        assert "Agent" in df.columns
        assert "Role" in df.columns


# ---------------------------------------------------------------------------
# Dataclass / enum tests
# ---------------------------------------------------------------------------

class TestEnums:
    def test_explanation_levels(self):
        assert ExplanationLevel.INDIVIDUAL.value == 1
        assert ExplanationLevel.COORDINATION.value == 2
        assert ExplanationLevel.COLLECTIVE.value == 3

    def test_automation_levels(self):
        assert AutomationLevel.IN_THE_LOOP.value == "in_loop"
        assert AutomationLevel.ON_THE_LOOP.value == "on_loop"
        assert AutomationLevel.OUT_OF_THE_LOOP.value == "out_loop"

    def test_safety_status(self):
        assert SafetyStatus.SAFE.value == "safe"
        assert SafetyStatus.WARNING.value == "warning"
        assert SafetyStatus.CRITICAL.value == "critical"


class TestCoordinationDecision:
    def test_creation(self):
        cd = CoordinationDecision(
            decision_type="delegation",
            from_agent="A",
            to_agent="B",
            rationale="A is busy",
        )
        assert cd.decision_type == "delegation"
        assert cd.from_agent == "A"
        assert cd.to_agent == "B"
        assert cd.timestamp  # auto-generated


class TestSafetyAssessment:
    def test_creation(self):
        sa = SafetyAssessment(
            status=SafetyStatus.SAFE,
            constitutional_violations=[],
            coordination_issues=[],
            emergent_risks=[],
            responsible_agents={"A": 0.5, "B": 0.5},
            intervention_required=False,
        )
        assert sa.status == SafetyStatus.SAFE
        assert sa.intervention_required is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
