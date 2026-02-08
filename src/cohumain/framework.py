"""
CoHumAIn Framework - Core Implementation
Collective Human and Machine Intelligence for Explainable Multi-Agent Systems
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time
from datetime import datetime
import json
import pandas as pd


class ExplanationLevel(Enum):
    """Three levels of explanation in CoHumAIn framework"""
    INDIVIDUAL = 1  # Agent-level reasoning
    COORDINATION = 2  # Inter-agent delegation and conflict resolution
    COLLECTIVE = 3  # Team-level emergent behavior


class AutomationLevel(Enum):
    """Human oversight levels"""
    IN_THE_LOOP = "in_loop"  # Human approves each decision
    ON_THE_LOOP = "on_loop"  # Human monitors with intervention capability
    OUT_OF_THE_LOOP = "out_loop"  # Autonomous with logging


class SafetyStatus(Enum):
    """Safety status indicators"""
    SAFE = "safe"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Agent:
    """Individual agent in the multi-agent system"""
    name: str
    role: str
    expertise: float  # 0.0 to 1.0
    confidence_threshold: float
    capabilities: List[str]
    constitutional_principles: List[str]
    max_retries: int = 3
    timeout: int = 60
    
    def __post_init__(self):
        self.task_history: List[Dict] = []
        self.performance_metrics: Dict[str, float] = {
            "accuracy": 0.0,
            "avg_confidence": 0.0,
            "tasks_completed": 0
        }
    
    def generate_reasoning_trace(self, task: str, context: Dict) -> Dict[str, Any]:
        """
        Generate Level 1 (Individual) explanation
        Extends ReAct with safety-aware reasoning
        """
        reasoning = {
            "agent": self.name,
            "task": task,
            "thought": f"Analyzing task: {task}",
            "action": "Execute primary capability",
            "observation": "Task completed",
            "confidence": self._calculate_confidence(task, context),
            "constitutional_check": self._check_principles(task),
            "timestamp": datetime.now().isoformat()
        }
        
        self.task_history.append(reasoning)
        return reasoning
    
    def _calculate_confidence(self, task: str, context: Dict) -> float:
        """Calculate agent's confidence for this task"""
        # Simplified confidence calculation
        base_confidence = self.expertise
        
        # Adjust based on task complexity
        if context.get("complexity") == "high":
            base_confidence *= 0.9
        
        # Adjust based on constitutional alignment
        if not self._check_principles(task)["all_satisfied"]:
            base_confidence *= 0.8
        
        return min(base_confidence, 1.0)
    
    def _check_principles(self, task: str) -> Dict[str, Any]:
        """Check constitutional principles compliance"""
        violations = []
        
        # Simplified principle checking
        for principle in self.constitutional_principles:
            # In real implementation, use LLM to check principle compliance
            satisfied = True  # Placeholder
            if not satisfied:
                violations.append(principle)
        
        return {
            "all_satisfied": len(violations) == 0,
            "violations": violations,
            "principles_checked": self.constitutional_principles
        }


@dataclass
class CoordinationDecision:
    """Level 2 (Coordination) explanation"""
    decision_type: str  # "delegation", "conflict_resolution", "information_sharing"
    from_agent: str
    to_agent: Optional[str]
    rationale: str
    delegation_reason: Optional[str] = None
    conflict_resolution_strategy: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CollectiveExplanation:
    """Level 3 (Collective) explanation"""
    task: str
    agent_contributions: Dict[str, float]
    emergent_behaviors: List[str]
    temporal_timeline: List[Dict]
    counterfactuals: List[str]
    collective_confidence: float
    recommendation: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SafetyAssessment:
    """Safety-aware attribution results"""
    status: SafetyStatus
    constitutional_violations: List[Dict]
    coordination_issues: List[str]
    emergent_risks: List[str]
    responsible_agents: Dict[str, float]  # Agent name -> responsibility score
    intervention_required: bool
    intervention_reason: Optional[str] = None


class CoHumAInFramework:
    """
    Main CoHumAIn Framework
    Provides transparent, safe, and human-centered multi-agent coordination
    """
    
    def __init__(
        self,
        domain: str = "general",
        safety_mode: str = "balanced",
        regulatory_framework: Optional[str] = None,
        stakeholder_type: str = "developer"
    ):
        self.domain = domain
        self.safety_mode = safety_mode
        self.regulatory_framework = regulatory_framework
        self.stakeholder_type = stakeholder_type
        
        self.agents: List[Agent] = []
        self.coordination_history: List[CoordinationDecision] = []
        self.task_history: List[Dict] = []
        
        # Configuration thresholds
        self.confidence_threshold = self._get_confidence_threshold()
        self.intervention_thresholds = self._get_intervention_thresholds()
    
    def _get_confidence_threshold(self) -> float:
        """Get confidence threshold based on safety mode"""
        thresholds = {
            "permissive": 0.70,
            "balanced": 0.80,
            "strict": 0.90,
            "maximum": 0.95
        }
        return thresholds.get(self.safety_mode, 0.80)
    
    def _get_intervention_thresholds(self) -> Dict[str, float]:
        """Get intervention thresholds based on domain and safety mode"""
        return {
            "confidence_min": self.confidence_threshold,
            "risk_max": 0.3,
            "violation_tolerance": 0
        }
    
    def add_agent(self, agent: Agent):
        """Add agent to the framework"""
        self.agents.append(agent)
    
    def add_agents(self, agents: List[Agent]):
        """Add multiple agents to the framework"""
        self.agents.extend(agents)
    
    def execute_task(
        self,
        task: str,
        context: Optional[Dict] = None,
        human_in_loop: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a task with full CoHumAIn transparency
        
        Returns complete explanation package with all three levels
        """
        if context is None:
            context = {}
        
        start_time = time.time()
        
        # Step 1: Generate individual agent reasoning (Level 1)
        level1_explanations = []
        for agent in self.agents:
            reasoning = agent.generate_reasoning_trace(task, context)
            level1_explanations.append(reasoning)
        
        # Step 2: Generate coordination explanations (Level 2)
        level2_explanations = self._generate_coordination_explanations(
            task, level1_explanations, context
        )
        
        # Step 3: Safety-aware attribution
        safety_assessment = self._assess_safety(
            level1_explanations, level2_explanations
        )
        
        # Step 4: Determine automation level
        automation_level = self._calibrate_trust(
            level1_explanations, safety_assessment, context
        )
        
        # Step 5: Generate collective explanation (Level 3)
        level3_explanation = self._generate_collective_explanation(
            task, level1_explanations, level2_explanations, safety_assessment
        )
        
        # Step 6: Check if intervention required
        requires_intervention = (
            safety_assessment.intervention_required or
            human_in_loop or
            automation_level == AutomationLevel.IN_THE_LOOP
        )
        
        execution_time = time.time() - start_time
        
        result = {
            "task": task,
            "success": safety_assessment.status != SafetyStatus.CRITICAL,
            "level1_explanations": level1_explanations,
            "level2_explanations": level2_explanations,
            "level3_explanation": level3_explanation,
            "safety_assessment": safety_assessment,
            "automation_level": automation_level.value,
            "requires_human_review": requires_intervention,
            "intervention_reason": safety_assessment.intervention_reason,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat()
        }
        
        self.task_history.append(result)
        return result
    
    def _generate_coordination_explanations(
        self,
        task: str,
        level1_explanations: List[Dict],
        context: Dict
    ) -> List[CoordinationDecision]:
        """
        Generate Level 2 (Coordination) explanations
        NOVEL CONTRIBUTION: Makes delegation and conflict resolution transparent
        """
        coordination_explanations = []
        
        # Determine which agents should handle subtasks
        for i, explanation in enumerate(level1_explanations):
            agent_name = explanation["agent"]
            
            # Check if delegation needed
            if explanation["confidence"] < self.confidence_threshold:
                # Find best agent for delegation
                target_agent = self._find_best_delegate(task, explanation["agent"])
                
                if target_agent:
                    coordination = CoordinationDecision(
                        decision_type="delegation",
                        from_agent=agent_name,
                        to_agent=target_agent.name,
                        rationale=f"Agent {agent_name} confidence ({explanation['confidence']:.2f}) below threshold",
                        delegation_reason=f"Agent {target_agent.name} has higher expertise ({target_agent.expertise:.2f})"
                    )
                    coordination_explanations.append(coordination)
        
        # Check for agent disagreements
        if len(level1_explanations) > 1:
            confidences = [e["confidence"] for e in level1_explanations]
            if max(confidences) - min(confidences) > 0.2:
                coordination = CoordinationDecision(
                    decision_type="conflict_resolution",
                    from_agent="System",
                    to_agent=None,
                    rationale="Significant confidence variance detected among agents",
                    conflict_resolution_strategy="Weighted voting by expertise"
                )
                coordination_explanations.append(coordination)
        
        return coordination_explanations
    
    def _find_best_delegate(self, task: str, current_agent: str) -> Optional[Agent]:
        """Find best agent to delegate task to"""
        candidates = [a for a in self.agents if a.name != current_agent]
        
        if not candidates:
            return None
        
        # Sort by expertise
        candidates.sort(key=lambda a: a.expertise, reverse=True)
        return candidates[0]
    
    def _assess_safety(
        self,
        level1_explanations: List[Dict],
        level2_explanations: List[CoordinationDecision]
    ) -> SafetyAssessment:
        """
        Assess safety with multi-agent attribution
        Integrates safety monitoring with explainability
        """
        violations = []
        coordination_issues = []
        emergent_risks = []
        
        # Check constitutional violations
        for explanation in level1_explanations:
            principle_check = explanation.get("constitutional_check", {})
            if not principle_check.get("all_satisfied", True):
                violations.append({
                    "agent": explanation["agent"],
                    "violations": principle_check.get("violations", [])
                })
        
        # Check coordination issues
        delegation_count = sum(
            1 for c in level2_explanations if c.decision_type == "delegation"
        )
        if delegation_count > 3:
            coordination_issues.append("Excessive delegation detected")
        
        # Calculate responsibility scores
        responsible_agents = {}
        for agent in self.agents:
            # Simplified responsibility calculation
            direct_contribution = 1.0 / len(self.agents)
            responsible_agents[agent.name] = direct_contribution
        
        # Determine status
        if len(violations) > 0:
            status = SafetyStatus.CRITICAL
            intervention_required = True
            intervention_reason = f"Constitutional violations: {len(violations)}"
        elif len(coordination_issues) > 0:
            status = SafetyStatus.WARNING
            intervention_required = False
            intervention_reason = None
        else:
            status = SafetyStatus.SAFE
            intervention_required = False
            intervention_reason = None
        
        return SafetyAssessment(
            status=status,
            constitutional_violations=violations,
            coordination_issues=coordination_issues,
            emergent_risks=emergent_risks,
            responsible_agents=responsible_agents,
            intervention_required=intervention_required,
            intervention_reason=intervention_reason
        )
    
    def _calibrate_trust(
        self,
        level1_explanations: List[Dict],
        safety_assessment: SafetyAssessment,
        context: Dict
    ) -> AutomationLevel:
        """
        Calibrate trust and determine automation level
        Extends single-agent trust metrics to collective confidence
        """
        # Calculate collective confidence
        confidences = [e["confidence"] for e in level1_explanations]
        weights = [self._get_agent_weight(e["agent"]) for e in level1_explanations]
        
        collective_confidence = sum(c * w for c, w in zip(confidences, weights)) / sum(weights)
        
        # Get task stakes
        stakes = context.get("stakes", "medium")
        
        # Determine automation level
        if collective_confidence < 0.7 or stakes == "high" or safety_assessment.status == SafetyStatus.CRITICAL:
            return AutomationLevel.IN_THE_LOOP
        elif collective_confidence < 0.85 or stakes == "medium":
            return AutomationLevel.ON_THE_LOOP
        else:
            return AutomationLevel.OUT_OF_THE_LOOP
    
    def _get_agent_weight(self, agent_name: str) -> float:
        """Get weight for agent in collective confidence calculation"""
        agent = next((a for a in self.agents if a.name == agent_name), None)
        return agent.expertise if agent else 0.5
    
    def _generate_collective_explanation(
        self,
        task: str,
        level1_explanations: List[Dict],
        level2_explanations: List[CoordinationDecision],
        safety_assessment: SafetyAssessment
    ) -> CollectiveExplanation:
        """
        Generate Level 3 (Collective) explanation
        NOVEL CONTRIBUTION: Explains emergent team behavior
        """
        # Calculate agent contributions
        agent_contributions = {}
        for agent in self.agents:
            # Simplified contribution calculation
            agent_contributions[agent.name] = 1.0 / len(self.agents)
        
        # Identify emergent behaviors
        emergent_behaviors = []
        if len(level2_explanations) > 2:
            emergent_behaviors.append("High coordination required")
        
        # Build temporal timeline
        timeline = []
        for i, explanation in enumerate(level1_explanations):
            timeline.append({
                "step": i + 1,
                "agent": explanation["agent"],
                "action": explanation["action"],
                "confidence": explanation["confidence"]
            })
        
        # Generate counterfactuals
        counterfactuals = [
            "If delegation threshold was lower, fewer transfers would occur",
            "If all agents had higher expertise, confidence would increase"
        ]
        
        # Calculate collective confidence
        confidences = [e["confidence"] for e in level1_explanations]
        collective_confidence = sum(confidences) / len(confidences)
        
        # Generate recommendation
        if safety_assessment.status == SafetyStatus.SAFE:
            recommendation = "Task completed successfully with appropriate agent collaboration"
        elif safety_assessment.status == SafetyStatus.WARNING:
            recommendation = "Task completed with coordination issues - review recommended"
        else:
            recommendation = "Critical safety concerns - human intervention required"
        
        return CollectiveExplanation(
            task=task,
            agent_contributions=agent_contributions,
            emergent_behaviors=emergent_behaviors,
            temporal_timeline=timeline,
            counterfactuals=counterfactuals,
            collective_confidence=collective_confidence,
            recommendation=recommendation
        )
    
    def generate_compliance_report(
        self,
        standard: str = "general",
        format: str = "json"
    ) -> str:
        """Generate regulatory compliance report"""
        report = {
            "framework": "CoHumAIn",
            "standard": standard,
            "regulatory_framework": self.regulatory_framework,
            "domain": self.domain,
            "agents": [
                {
                    "name": a.name,
                    "role": a.role,
                    "expertise": a.expertise,
                    "tasks_completed": a.performance_metrics["tasks_completed"]
                }
                for a in self.agents
            ],
            "total_tasks": len(self.task_history),
            "safety_incidents": sum(
                1 for t in self.task_history
                if isinstance(t.get("safety_assessment"), SafetyAssessment)
                and t["safety_assessment"].status == SafetyStatus.CRITICAL
            ),
            "interventions_required": sum(
                1 for t in self.task_history if t.get("requires_human_review", False)
            ),
            "generated_at": datetime.now().isoformat()
        }
        
        if format == "json":
            return json.dumps(report, indent=2)
        else:
            # Placeholder for other formats
            return str(report)
    
    def get_agent_performance_summary(self) -> pd.DataFrame:
        """Get performance summary for all agents"""
        
        data = []
        for agent in self.agents:
            data.append({
                "Agent": agent.name,
                "Role": agent.role,
                "Expertise": agent.expertise,
                "Tasks": agent.performance_metrics["tasks_completed"],
                "Avg Confidence": agent.performance_metrics["avg_confidence"],
                "Accuracy": agent.performance_metrics["accuracy"]
            })
        
        return pd.DataFrame(data)
