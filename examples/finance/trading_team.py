"""
CoHumAIn Framework - Finance Domain Example
Trading agent team with regulatory compliance for SEC/MiFID II
"""

from typing import Dict, List, Any
import time
from cohumain.framework import CoHumAInFramework, Agent


class MarketAnalyst(Agent):
    """Market analysis agent for trading recommendations"""
    
    def __init__(self, name: str = "Market Analyst", expertise: float = 0.92):
        super().__init__(
            name=name,
            role="Market Analyst",
            expertise=expertise,
            confidence_threshold=0.85,
            capabilities=["Market Analysis", "Technical Analysis", "Sentiment Analysis"],
            constitutional_principles=[
                "Evidence-based recommendations only",
                "Disclose data sources and assumptions",
                "No speculation without clear disclaimer"
            ],
            max_retries=3,
            timeout=120
        )
    
    def analyze_security(self, ticker: str, timeframe: str = "1M") -> Dict[str, Any]:
        """
        Analyze security and generate recommendation
        
        Returns Level 1 explanation with market analysis
        """
        # Simplified analysis - real implementation would use market data APIs
        analysis = {
            "ticker": ticker,
            "timeframe": timeframe,
            "technical_indicators": {
                "RSI": 65.2,
                "MACD": "Bullish",
                "Moving_Avg_50": "Above",
                "Volume": "Above Average"
            },
            "sentiment": "Positive",
            "recommendation": "BUY",
            "target_price": 185.00,
            "confidence": 0.87
        }
        
        reasoning = self.generate_reasoning_trace(
            task=f"Analyze {ticker} for {timeframe}",
            context={"analysis": analysis}
        )
        
        reasoning.update({
            "analysis": analysis,
            "data_sources": ["Market Data API", "News Sentiment API"],
            "assumptions": ["Historical patterns continue", "No major events"]
        })
        
        return reasoning


class RiskManager(Agent):
    """Risk assessment agent ensuring portfolio safety"""
    
    def __init__(self, name: str = "Risk Manager", expertise: float = 0.96):
        super().__init__(
            name=name,
            role="Risk Manager",
            expertise=expertise,
            confidence_threshold=0.95,
            capabilities=["Risk Assessment", "Portfolio Analysis", "Stress Testing"],
            constitutional_principles=[
                "Conservative risk management",
                "Maximum drawdown limits must be enforced",
                "Position sizing based on volatility",
                "No single position exceeds 10% of portfolio"
            ],
            max_retries=2,
            timeout=90
        )
    
    def assess_trade_risk(self, trade: Dict[str, Any], portfolio: Dict) -> Dict[str, Any]:
        """
        Assess risk of proposed trade
        
        Returns Level 1 explanation with risk metrics
        """
        # Simplified risk calculation
        position_size_pct = (trade.get("value", 0) / portfolio.get("total_value", 1)) * 100
        
        risk_assessment = {
            "position_size_percent": position_size_pct,
            "max_drawdown_risk": 0.05,
            "portfolio_correlation": 0.3,
            "volatility": 0.18,
            "risk_score": 0.25,  # 0-1 scale
            "approved": position_size_pct <= 10 and True,
            "concerns": []
        }
        
        if position_size_pct > 10:
            risk_assessment["concerns"].append("Position size exceeds 10% limit")
        
        if risk_assessment["volatility"] > 0.25:
            risk_assessment["concerns"].append("High volatility detected")
        
        reasoning = self.generate_reasoning_trace(
            task=f"Assess risk for {trade.get('ticker')} trade",
            context={"risk_assessment": risk_assessment}
        )
        
        reasoning.update({
            "risk_assessment": risk_assessment,
            "portfolio_impact": f"{position_size_pct:.2f}% of portfolio",
            "risk_limits": self.constitutional_principles
        })
        
        return reasoning


class ComplianceOfficer(Agent):
    """Compliance checking agent for regulatory requirements"""
    
    def __init__(self, name: str = "Compliance Officer", expertise: float = 0.99):
        super().__init__(
            name=name,
            role="Compliance Officer",
            expertise=expertise,
            confidence_threshold=0.98,
            capabilities=["Compliance Checking", "Regulatory Analysis", "Audit Trail"],
            constitutional_principles=[
                "Strict adherence to SEC regulations",
                "MiFID II transparency requirements",
                "Complete audit trail for all trades",
                "No conflicts of interest",
                "Insider trading checks mandatory"
            ],
            max_retries=2,
            timeout=120
        )
    
    def check_compliance(self, trade: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check trade for regulatory compliance
        
        Returns Level 1 explanation with compliance status
        """
        compliance_check = {
            "sec_rules": {
                "Rule_15c3-5": "Compliant",  # Market access rule
                "Reg_SHO": "Compliant",  # Short sale rule
                "Reg_NMS": "Compliant"  # National market system
            },
            "mifid_ii": {
                "best_execution": "Verified",
                "transaction_reporting": "Ready",
                "client_classification": "Retail"
            },
            "insider_trading_check": "Clear",
            "conflicts_of_interest": "None detected",
            "approved": True,
            "compliance_score": 1.0
        }
        
        reasoning = self.generate_reasoning_trace(
            task=f"Compliance check for {trade.get('ticker')} trade",
            context={"compliance": compliance_check}
        )
        
        reasoning.update({
            "compliance_check": compliance_check,
            "regulations_checked": ["SEC", "MiFID II", "Insider Trading"],
            "audit_trail_id": f"AUDIT_{trade.get('ticker')}_{int(time.time())}"
        })
        
        return reasoning


class TradeExecutor(Agent):
    """Trade execution agent"""
    
    def __init__(self, name: str = "Trade Executor", expertise: float = 0.88):
        super().__init__(
            name=name,
            role="Trade Executor",
            expertise=expertise,
            confidence_threshold=0.85,
            capabilities=["Order Execution", "Market Orders", "Limit Orders"],
            constitutional_principles=[
                "Best execution practices",
                "Price improvement when possible",
                "Minimize market impact"
            ],
            max_retries=3,
            timeout=60
        )


def create_trading_team(regulatory_framework: str = "SEC") -> CoHumAInFramework:
    """
    Create a complete trading team with CoHumAIn framework
    
    Args:
        regulatory_framework: "SEC", "MiFID II", or "Both"
    
    Returns:
        Configured CoHumAIn framework with trading agents
    """
    framework = CoHumAInFramework(
        domain="finance",
        safety_mode="strict",
        regulatory_framework=regulatory_framework,
        stakeholder_type="trader"
    )
    
    # Add trading team agents
    framework.add_agents([
        MarketAnalyst(),
        RiskManager(),
        ComplianceOfficer(),
        TradeExecutor()
    ])
    
    return framework


# Example usage
if __name__ == "__main__":
    import time
    
    # Create trading team
    trading_team = create_trading_team(regulatory_framework="SEC")
    
    # Execute trade analysis task
    result = trading_team.execute_task(
        task="Analyze AAPL for portfolio addition",
        context={
            "ticker": "AAPL",
            "portfolio_value": 1_000_000,
            "proposed_investment": 50_000,
            "stakes": "high"  # High stakes = human-in-the-loop
        },
        human_in_loop=True
    )
    
    print("\n" + "="*80)
    print("COHUMAIN FINANCE EXAMPLE - TRADING DECISION")
    print("="*80)
    
    print(f"\nTask: {result['task']}")
    print(f"Success: {result['success']}")
    print(f"Automation Level: {result['automation_level']}")
    print(f"Human Review Required: {result['requires_human_review']}")
    
    print("\n--- LEVEL 1: Individual Agent Reasoning ---")
    for explanation in result['level1_explanations']:
        print(f"\n{explanation['agent']}:")
        print(f"  Confidence: {explanation['confidence']:.2%}")
        print(f"  Action: {explanation['action']}")
    
    print("\n--- LEVEL 2: Coordination Decisions ---")
    if result['level2_explanations']:
        for coord in result['level2_explanations']:
            print(f"\nDecision: {coord.decision_type}")
            print(f"  From: {coord.from_agent}")
            if coord.to_agent:
                print(f"  To: {coord.to_agent}")
            print(f"  Rationale: {coord.rationale}")
    else:
        print("No coordination decisions required")
    
    print("\n--- LEVEL 3: Collective Explanation ---")
    collective = result['level3_explanation']
    print(f"\nCollective Confidence: {collective.collective_confidence:.2%}")
    print(f"Recommendation: {collective.recommendation}")
    print(f"\nAgent Contributions:")
    for agent, contrib in collective.agent_contributions.items():
        print(f"  {agent}: {contrib:.2%}")
    
    print("\n--- SAFETY ASSESSMENT ---")
    safety = result['safety_assessment']
    print(f"Status: {safety.status.value.upper()}")
    print(f"Constitutional Violations: {len(safety.constitutional_violations)}")
    print(f"Coordination Issues: {len(safety.coordination_issues)}")
    print(f"Intervention Required: {safety.intervention_required}")
    
    print("\n" + "="*80)
    
    # Generate compliance report
    print("\n--- COMPLIANCE REPORT ---")
    compliance_report = trading_team.generate_compliance_report(
        standard="SEC Rule 15c3-5",
        format="json"
    )
    print(compliance_report)
