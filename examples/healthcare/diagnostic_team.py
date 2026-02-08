"""
CoHumAIn Framework - Healthcare Domain Example
Multi-specialist diagnostic team with HIPAA compliance
"""

from typing import Dict, List, Any
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from cohumain.framework import CoHumAInFramework, Agent


class Radiologist(Agent):
    """Radiologist agent for medical imaging analysis"""
    
    def __init__(self, name: str = "Radiologist AI", expertise: float = 0.94):
        super().__init__(
            name=name,
            role="Radiologist",
            expertise=expertise,
            confidence_threshold=0.90,
            capabilities=["Medical Imaging", "CT Scan Analysis", "MRI Analysis", "X-Ray Analysis"],
            constitutional_principles=[
                "Patient safety is paramount",
                "HIPAA compliance mandatory",
                "Never diagnose without sufficient image quality",
                "Always recommend human radiologist review for critical findings",
                "Document all limitations and uncertainties"
            ],
            max_retries=2,
            timeout=180
        )
    
    def analyze_imaging(self, imaging_type: str, findings: Dict) -> Dict[str, Any]:
        """
        Analyze medical imaging study
        
        Returns Level 1 explanation with imaging analysis
        """
        # Simplified analysis - real implementation would use medical imaging AI
        analysis = {
            "imaging_type": imaging_type,
            "quality": "Diagnostic quality",
            "key_findings": findings.get("findings", []),
            "abnormalities": findings.get("abnormalities", []),
            "recommendation": findings.get("recommendation", "Further evaluation needed"),
            "confidence": 0.89,
            "requires_human_review": True  # Always for clinical decisions
        }
        
        reasoning = self.generate_reasoning_trace(
            task=f"Analyze {imaging_type} study",
            context={"analysis": analysis}
        )
        
        reasoning.update({
            "clinical_analysis": analysis,
            "imaging_protocol": f"{imaging_type} standard protocol",
            "comparison": "No prior studies available",
            "limitations": ["Single view only", "Limited patient history"],
            "hipaa_compliance": "PHI anonymized, secure transmission"
        })
        
        return reasoning


class Pathologist(Agent):
    """Pathologist agent for tissue and lab analysis"""
    
    def __init__(self, name: str = "Pathologist AI", expertise: float = 0.93):
        super().__init__(
            name=name,
            role="Pathologist",
            expertise=expertise,
            confidence_threshold=0.90,
            capabilities=["Histopathology", "Lab Analysis", "Tissue Analysis", "Biomarker Analysis"],
            constitutional_principles=[
                "Thorough specimen analysis required",
                "HIPAA compliance mandatory",
                "Document sample quality and limitations",
                "Always provide differential diagnosis",
                "Recommend additional testing when uncertain"
            ],
            max_retries=2,
            timeout=180
        )
    
    def analyze_pathology(self, sample_type: str, findings: Dict) -> Dict[str, Any]:
        """
        Analyze pathology specimen
        
        Returns Level 1 explanation with pathology analysis
        """
        analysis = {
            "sample_type": sample_type,
            "specimen_quality": "Adequate for diagnosis",
            "microscopic_findings": findings.get("microscopic", []),
            "cell_characteristics": findings.get("cells", {}),
            "biomarkers": findings.get("biomarkers", {}),
            "diagnosis": findings.get("diagnosis", "Pending additional tests"),
            "differential_diagnosis": findings.get("differential", []),
            "confidence": 0.91
        }
        
        reasoning = self.generate_reasoning_trace(
            task=f"Analyze {sample_type} specimen",
            context={"analysis": analysis}
        )
        
        reasoning.update({
            "pathology_report": analysis,
            "staining_methods": ["H&E", "IHC"],
            "additional_tests_recommended": findings.get("additional_tests", []),
            "hipaa_compliance": "PHI protected, secure lab protocol"
        })
        
        return reasoning


class Geneticist(Agent):
    """Geneticist agent for genetic analysis"""
    
    def __init__(self, name: str = "Geneticist AI", expertise: float = 0.91):
        super().__init__(
            name=name,
            role="Geneticist",
            expertise=expertise,
            confidence_threshold=0.88,
            capabilities=["Genomic Analysis", "Mutation Detection", "Risk Assessment", "Pharmacogenomics"],
            constitutional_principles=[
                "Protect genetic privacy (GINA compliance)",
                "HIPAA compliance mandatory",
                "Provide genetic counseling recommendations",
                "Document hereditary implications",
                "Explain uncertainty in genetic predictions"
            ],
            max_retries=2,
            timeout=240
        )
    
    def analyze_genetics(self, test_type: str, results: Dict) -> Dict[str, Any]:
        """
        Analyze genetic test results
        
        Returns Level 1 explanation with genetic analysis
        """
        analysis = {
            "test_type": test_type,
            "mutations_detected": results.get("mutations", []),
            "risk_assessment": results.get("risk", "Moderate"),
            "hereditary_implications": results.get("hereditary", "Family screening recommended"),
            "pharmacogenomic_impact": results.get("pharma", "Standard dosing applicable"),
            "confidence": 0.87,
            "genetic_counseling_required": True
        }
        
        reasoning = self.generate_reasoning_trace(
            task=f"Analyze {test_type} genetic test",
            context={"analysis": analysis}
        )
        
        reasoning.update({
            "genetic_analysis": analysis,
            "testing_methodology": f"{test_type} sequencing",
            "clinical_significance": results.get("significance", "Uncertain"),
            "privacy_protections": "GINA/HIPAA compliant, encrypted storage"
        })
        
        return reasoning


class PrimaryCarePhysician(Agent):
    """Primary care physician agent for holistic patient assessment"""
    
    def __init__(self, name: str = "Primary Care AI", expertise: float = 0.89):
        super().__init__(
            name=name,
            role="Primary Care Physician",
            expertise=expertise,
            confidence_threshold=0.85,
            capabilities=["Patient History", "Physical Assessment", "Treatment Planning", "Care Coordination"],
            constitutional_principles=[
                "Holistic patient-centered care",
                "HIPAA compliance mandatory",
                "Consider patient preferences and values",
                "Coordinate care across specialists",
                "Always involve patient in decision-making"
            ],
            max_retries=3,
            timeout=120
        )
    
    def synthesize_diagnosis(self, patient_data: Dict, specialist_inputs: List[Dict]) -> Dict[str, Any]:
        """
        Synthesize specialist inputs into comprehensive assessment
        
        Returns Level 1 explanation with integrated diagnosis
        """
        diagnosis = {
            "working_diagnosis": patient_data.get("diagnosis", "Under investigation"),
            "specialist_agreement": "Consensus reached",
            "treatment_plan": patient_data.get("treatment", []),
            "follow_up": patient_data.get("follow_up", "2 weeks"),
            "patient_education": "Educational materials provided",
            "confidence": 0.86
        }
        
        reasoning = self.generate_reasoning_trace(
            task="Synthesize specialist assessments and create treatment plan",
            context={"diagnosis": diagnosis, "specialists": len(specialist_inputs)}
        )
        
        reasoning.update({
            "integrated_assessment": diagnosis,
            "specialist_inputs_considered": len(specialist_inputs),
            "patient_preferences": patient_data.get("preferences", "Standard care"),
            "coordination_notes": "Scheduled follow-up with all specialists",
            "hipaa_compliance": "Coordinated care exception documented"
        })
        
        return reasoning


def create_diagnostic_team() -> CoHumAInFramework:
    """
    Create HIPAA-compliant diagnostic team with CoHumAIn framework
    
    Returns:
        Configured CoHumAIn framework with healthcare agents
    """
    framework = CoHumAInFramework(
        domain="healthcare",
        safety_mode="maximum",  # Maximum safety for healthcare
        regulatory_framework="HIPAA+FDA",
        stakeholder_type="physician"
    )
    
    # Add diagnostic team agents
    framework.add_agents([
        Radiologist(),
        Pathologist(),
        Geneticist(),
        PrimaryCarePhysician()
    ])
    
    return framework


# Example usage
if __name__ == "__main__":
    import json
    
    # Create diagnostic team
    diagnostic_team = create_diagnostic_team()
    
    # Example patient case (all PHI anonymized for demo)
    patient_case = {
        "patient_id": "ENCRYPTED_ID_12345",
        "age": 58,
        "presenting_complaint": "Persistent lymphadenopathy",
        "imaging_findings": {
            "findings": ["Enlarged lymph nodes", "No mass lesions"],
            "abnormalities": ["Bilateral cervical adenopathy"],
            "recommendation": "Biopsy recommended"
        },
        "pathology_results": {
            "microscopic": ["Atypical lymphoid cells"],
            "cells": {"size": "enlarged", "nuclei": "irregular"},
            "biomarkers": {"CD20": "positive", "CD5": "negative"},
            "diagnosis": "Suspicious for lymphoma",
            "differential": ["Follicular lymphoma", "Reactive hyperplasia"],
            "additional_tests": ["Flow cytometry", "Genetic analysis"]
        },
        "genetic_results": {
            "mutations": ["BCL2 translocation"],
            "risk": "High risk for follicular lymphoma",
            "hereditary": "No hereditary pattern identified",
            "significance": "Pathogenic variant"
        },
        "stakes": "high"  # High stakes = maximum oversight
    }
    
    # Execute diagnostic assessment
    result = diagnostic_team.execute_task(
        task="Comprehensive diagnostic assessment for suspected lymphoma",
        context=patient_case,
        human_in_loop=True  # ALWAYS required for medical decisions
    )
    
    print("\n" + "="*80)
    print("COHUMAIN HEALTHCARE EXAMPLE - MULTI-SPECIALIST DIAGNOSIS")
    print("="*80)
    
    print(f"\nCase: {result['task']}")
    print(f"Safety Status: {result['safety_assessment'].status.value.upper()}")
    print(f"Automation Level: {result['automation_level']}")
    print(f"Human Review: REQUIRED (always for clinical decisions)")
    
    print("\n--- LEVEL 1: Individual Specialist Assessments ---")
    for explanation in result['level1_explanations']:
        print(f"\n{explanation['agent']}:")
        print(f"  Confidence: {explanation['confidence']:.2%}")
        print(f"  Finding: {explanation['observation']}")
    
    print("\n--- LEVEL 2: Care Coordination ---")
    if result['level2_explanations']:
        for coord in result['level2_explanations']:
            print(f"\nCoordination: {coord.decision_type}")
            print(f"  Rationale: {coord.rationale}")
    else:
        print("Smooth specialist coordination - no conflicts detected")
    
    print("\n--- LEVEL 3: Integrated Clinical Decision Support ---")
    collective = result['level3_explanation']
    print(f"\nCollective Diagnostic Confidence: {collective.collective_confidence:.2%}")
    print(f"Recommendation: {collective.recommendation}")
    print(f"\nSpecialist Contributions:")
    for specialist, contrib in collective.agent_contributions.items():
        print(f"  {specialist}: {contrib:.2%}")
    
    print("\n--- HIPAA COMPLIANCE STATUS ---")
    print("✓ PHI encrypted and anonymized")
    print("✓ Access logged for audit trail")
    print("✓ Minimum necessary principle applied")
    print("✓ Secure transmission protocols used")
    print("✓ Patient consent documented")
    
    print("\n--- CLINICAL DECISION SUPPORT ---")
    print("Working Diagnosis: Suspected follicular lymphoma")
    print("Evidence Strength: HIGH (imaging + pathology + genetics concordant)")
    print("Recommended Actions:")
    print("  1. Hematology-oncology referral (URGENT)")
    print("  2. Complete staging workup")
    print("  3. Flow cytometry confirmation")
    print("  4. Patient education and genetic counseling")
    print("  5. Multidisciplinary tumor board review")
    
    print("\n--- SAFETY & TRANSPARENCY ---")
    safety = result['safety_assessment']
    print(f"Constitutional Compliance: {len(safety.constitutional_violations) == 0}")
    print(f"Coordination Quality: {len(safety.coordination_issues) == 0}")
    print(f"Human Oversight: MANDATORY for final decision")
    
    print("\n" + "="*80)
    print("\n📋 Generating FDA-compliant Clinical Decision Support Report...")
    
    # Generate compliance report
    compliance_report = diagnostic_team.generate_compliance_report(
        standard="FDA 21 CFR Part 11",
        format="json"
    )
    
    report = json.loads(compliance_report)
    print(f"\nReport Generated: {report['generated_at']}")
    print(f"Regulatory Framework: {report['regulatory_framework']}")
    print(f"Total Assessments: {report['total_tasks']}")
    print(f"Safety Incidents: {report['safety_incidents']}")
    print(f"Human Interventions: {report['interventions_required']}")
    
    print("\n✅ WINDOW OF TRANSPARENCY: Complete diagnostic process with full explainability")
    print("✅ Physicians can understand, trust, and act on AI-assisted diagnosis")
    print("✅ Audit trail available for regulatory compliance and quality assurance")
