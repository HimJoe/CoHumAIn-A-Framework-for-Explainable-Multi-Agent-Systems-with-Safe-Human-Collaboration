"""
CoHumAIn Framework - Safety Dashboard
Real-time safety monitoring, constitutional compliance, misalignment detection, and intervention tracking
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Safety Dashboard", page_icon="🛡️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .safety-card-safe {
        background-color: #ecfdf5;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10b981;
        margin-bottom: 0.5rem;
    }
    .safety-card-warning {
        background-color: #fffbeb;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
        margin-bottom: 0.5rem;
    }
    .safety-card-critical {
        background-color: #fef2f2;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ef4444;
        margin-bottom: 0.5rem;
    }
    .status-badge-safe {
        display: inline-block;
        background-color: #10b981;
        color: white;
        padding: 0.2rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .status-badge-warning {
        display: inline-block;
        background-color: #f59e0b;
        color: white;
        padding: 0.2rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .status-badge-critical {
        display: inline-block;
        background-color: #ef4444;
        color: white;
        padding: 0.2rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .principle-row {
        padding: 0.5rem 0;
        border-bottom: 1px solid #e5e7eb;
    }
    .intervention-card {
        background-color: #f8fafc;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)


def init_safety_session_state():
    """Initialize all session state variables for the safety dashboard."""
    if 'safety_mode' not in st.session_state:
        st.session_state.safety_mode = "Balanced"
    if 'alert_threshold' not in st.session_state:
        st.session_state.alert_threshold = 0.75
    if 'notify_email' not in st.session_state:
        st.session_state.notify_email = True
    if 'notify_slack' not in st.session_state:
        st.session_state.notify_slack = False
    if 'notify_dashboard' not in st.session_state:
        st.session_state.notify_dashboard = True
    if 'safety_score_history' not in st.session_state:
        st.session_state.safety_score_history = generate_safety_score_history()
    if 'violation_log' not in st.session_state:
        st.session_state.violation_log = generate_violation_log()
    if 'intervention_log' not in st.session_state:
        st.session_state.intervention_log = generate_intervention_log()
    if 'agent_compliance' not in st.session_state:
        st.session_state.agent_compliance = generate_agent_compliance()
    if 'constitutional_principles' not in st.session_state:
        st.session_state.constitutional_principles = generate_constitutional_principles()


# ---------------------------------------------------------------------------
# Sample data generators
# ---------------------------------------------------------------------------

def generate_safety_score_history():
    """Generate 30 days of safety score history."""
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=i) for i in range(29, -1, -1)]
    base = 0.92
    scores = []
    for i in range(30):
        noise = np.random.normal(0, 0.015)
        trend = 0.001 * i
        score = min(max(base + noise + trend, 0.70), 1.0)
        scores.append(round(score, 4))
    return {"dates": [d.strftime("%Y-%m-%d") for d in dates], "scores": scores}


def generate_violation_log():
    """Generate sample constitutional violation records."""
    return [
        {
            "id": "V-001",
            "timestamp": "2024-02-07 14:22:08",
            "agent": "Code Generator",
            "principle": "Follow secure coding practices",
            "severity": "Medium",
            "description": "Generated code included hard-coded API key in source file. Detected before deployment.",
            "status": "Resolved",
            "resolution": "Agent re-generated code using environment variable injection pattern."
        },
        {
            "id": "V-002",
            "timestamp": "2024-02-07 11:05:33",
            "agent": "Market Analyst",
            "principle": "Evidence-based recommendations only",
            "severity": "Low",
            "description": "Provided speculative forecast without citing data source for one of three claims.",
            "status": "Resolved",
            "resolution": "Agent appended citation to missing claim. Confidence adjusted downward."
        },
        {
            "id": "V-003",
            "timestamp": "2024-02-06 16:48:12",
            "agent": "Risk Manager",
            "principle": "Conservative risk management",
            "severity": "High",
            "description": "Approved portfolio allocation exceeding sector concentration limit by 3.2%.",
            "status": "Escalated",
            "resolution": "Human operator overrode allocation and recalibrated agent thresholds."
        },
        {
            "id": "V-004",
            "timestamp": "2024-02-06 09:15:44",
            "agent": "Code Generator",
            "principle": "Maintain test coverage above 80%",
            "severity": "Low",
            "description": "Submitted module with 74% test coverage. Test Generator flagged deficiency.",
            "status": "Resolved",
            "resolution": "Test Generator produced additional unit tests bringing coverage to 88%."
        },
        {
            "id": "V-005",
            "timestamp": "2024-02-05 20:32:19",
            "agent": "Primary Care AI",
            "principle": "Patient safety first",
            "severity": "Critical",
            "description": "Suggested medication dosage outside approved range for pediatric patient profile.",
            "status": "Blocked",
            "resolution": "Safety layer blocked output before delivery. Human physician notified immediately."
        },
        {
            "id": "V-006",
            "timestamp": "2024-02-05 13:10:55",
            "agent": "Security Analyst",
            "principle": "Zero tolerance for known vulnerabilities",
            "severity": "Medium",
            "description": "Rated a known CVE-listed dependency as low risk rather than flagging it immediately.",
            "status": "Resolved",
            "resolution": "Vulnerability database sync refreshed. Agent re-scanned and flagged correctly."
        },
        {
            "id": "V-007",
            "timestamp": "2024-02-04 17:44:30",
            "agent": "Compliance Officer",
            "principle": "Strict regulatory compliance",
            "severity": "High",
            "description": "Failed to flag a transaction pattern that matched a regulatory reporting requirement.",
            "status": "Resolved",
            "resolution": "Pattern matching rules updated. Retrospective report filed within deadline."
        },
    ]


def generate_intervention_log():
    """Generate sample human intervention records."""
    return [
        {
            "id": "INT-001",
            "timestamp": "2024-02-07 14:25:00",
            "trigger": "Safety Violation",
            "severity": "Medium",
            "description": "Code Generator produced hard-coded credentials. Safety layer paused workflow.",
            "operator": "Dr. Sarah Chen",
            "action_taken": "Rejected output and instructed agent to use environment variables.",
            "resolution": "Agent regenerated code with proper secret management.",
            "outcome": "Successful",
            "duration_minutes": 4,
            "agents_involved": ["Code Generator", "Security Analyst"]
        },
        {
            "id": "INT-002",
            "timestamp": "2024-02-07 10:12:30",
            "trigger": "Low Confidence",
            "severity": "Low",
            "description": "Collective confidence dropped to 0.68 on ambiguous requirement interpretation.",
            "operator": "James Rodriguez",
            "action_taken": "Clarified requirement scope and provided additional context to agents.",
            "resolution": "Agents re-evaluated with new context; confidence rose to 0.91.",
            "outcome": "Successful",
            "duration_minutes": 8,
            "agents_involved": ["Code Generator", "Code Reviewer"]
        },
        {
            "id": "INT-003",
            "timestamp": "2024-02-06 16:50:00",
            "trigger": "Safety Violation",
            "severity": "High",
            "description": "Risk Manager approved over-concentrated portfolio allocation.",
            "operator": "Dr. Sarah Chen",
            "action_taken": "Overrode allocation, recalibrated concentration limits, retrained risk model.",
            "resolution": "Agent thresholds tightened. New guardrail added for sector limits.",
            "outcome": "Successful",
            "duration_minutes": 22,
            "agents_involved": ["Risk Manager", "Compliance Officer"]
        },
        {
            "id": "INT-004",
            "timestamp": "2024-02-06 08:30:15",
            "trigger": "Agent Disagreement",
            "severity": "Medium",
            "description": "Code Generator and Security Analyst disagreed on input validation approach.",
            "operator": "Alex Kim",
            "action_taken": "Reviewed both proposals, selected Security Analyst recommendation with modifications.",
            "resolution": "Hybrid approach adopted: strict validation with user-friendly error messages.",
            "outcome": "Successful",
            "duration_minutes": 12,
            "agents_involved": ["Code Generator", "Security Analyst", "Code Reviewer"]
        },
        {
            "id": "INT-005",
            "timestamp": "2024-02-05 20:35:00",
            "trigger": "Safety Violation",
            "severity": "Critical",
            "description": "Primary Care AI suggested out-of-range pediatric medication dosage.",
            "operator": "Dr. Maria Lopez",
            "action_taken": "Blocked output. Conducted full audit of dosage calculation module.",
            "resolution": "Identified edge case in weight-based calculation. Module patched and re-validated.",
            "outcome": "Successful",
            "duration_minutes": 45,
            "agents_involved": ["Primary Care AI", "Radiologist AI"]
        },
        {
            "id": "INT-006",
            "timestamp": "2024-02-05 11:20:00",
            "trigger": "Threshold Breach",
            "severity": "Low",
            "description": "Aggregate safety score dipped below 0.85 threshold for 5 consecutive minutes.",
            "operator": "James Rodriguez",
            "action_taken": "Investigated root cause: temporary spike in low-confidence responses during load test.",
            "resolution": "No underlying issue. Threshold breach was transient and self-corrected.",
            "outcome": "No Action Required",
            "duration_minutes": 6,
            "agents_involved": []
        },
        {
            "id": "INT-007",
            "timestamp": "2024-02-04 15:05:45",
            "trigger": "Scheduled Review",
            "severity": "Low",
            "description": "Weekly safety audit of constitutional compliance across all agents.",
            "operator": "Dr. Sarah Chen",
            "action_taken": "Reviewed violation trends, updated two constitutional principles, approved current config.",
            "resolution": "Principles updated. All agents re-acknowledged constitutional framework.",
            "outcome": "Successful",
            "duration_minutes": 35,
            "agents_involved": ["Code Generator", "Security Analyst", "Code Reviewer", "Test Generator"]
        },
    ]


def generate_agent_compliance():
    """Generate per-agent compliance data."""
    return {
        "Code Generator": {
            "compliance_rate": 0.94,
            "total_checks": 312,
            "violations": 5,
            "last_violation": "2024-02-07 14:22:08",
            "status": "Active",
            "principles_count": 4
        },
        "Security Analyst": {
            "compliance_rate": 0.98,
            "total_checks": 248,
            "violations": 1,
            "last_violation": "2024-02-05 13:10:55",
            "status": "Active",
            "principles_count": 3
        },
        "Code Reviewer": {
            "compliance_rate": 1.00,
            "total_checks": 295,
            "violations": 0,
            "last_violation": "None",
            "status": "Active",
            "principles_count": 3
        },
        "Test Generator": {
            "compliance_rate": 0.99,
            "total_checks": 210,
            "violations": 0,
            "last_violation": "None",
            "status": "Active",
            "principles_count": 2
        },
        "Risk Manager": {
            "compliance_rate": 0.96,
            "total_checks": 185,
            "violations": 2,
            "last_violation": "2024-02-06 16:48:12",
            "status": "Active",
            "principles_count": 3
        },
        "Compliance Officer": {
            "compliance_rate": 0.97,
            "total_checks": 220,
            "violations": 1,
            "last_violation": "2024-02-04 17:44:30",
            "status": "Active",
            "principles_count": 4
        },
        "Primary Care AI": {
            "compliance_rate": 0.95,
            "total_checks": 178,
            "violations": 1,
            "last_violation": "2024-02-05 20:32:19",
            "status": "Under Review",
            "principles_count": 3
        },
    }


def generate_constitutional_principles():
    """Generate the master list of constitutional principles across agents."""
    return [
        {"id": "CP-01", "principle": "Follow secure coding practices", "agents": ["Code Generator", "Code Reviewer"], "category": "Security", "priority": "Critical"},
        {"id": "CP-02", "principle": "Zero tolerance for known vulnerabilities", "agents": ["Security Analyst"], "category": "Security", "priority": "Critical"},
        {"id": "CP-03", "principle": "Maintain test coverage above 80%", "agents": ["Code Generator", "Test Generator"], "category": "Quality", "priority": "High"},
        {"id": "CP-04", "principle": "Enforce coding standards", "agents": ["Code Reviewer"], "category": "Quality", "priority": "High"},
        {"id": "CP-05", "principle": "Ensure maintainability", "agents": ["Code Reviewer"], "category": "Quality", "priority": "Medium"},
        {"id": "CP-06", "principle": "Evidence-based recommendations only", "agents": ["Market Analyst", "Risk Manager"], "category": "Integrity", "priority": "Critical"},
        {"id": "CP-07", "principle": "Conservative risk management", "agents": ["Risk Manager"], "category": "Risk", "priority": "Critical"},
        {"id": "CP-08", "principle": "Strict regulatory compliance", "agents": ["Compliance Officer"], "category": "Compliance", "priority": "Critical"},
        {"id": "CP-09", "principle": "Patient safety first", "agents": ["Primary Care AI", "Radiologist AI", "Pathologist AI"], "category": "Safety", "priority": "Critical"},
        {"id": "CP-10", "principle": "HIPAA compliance", "agents": ["Primary Care AI", "Radiologist AI", "Pathologist AI"], "category": "Compliance", "priority": "Critical"},
        {"id": "CP-11", "principle": "Test failure paths", "agents": ["Test Generator"], "category": "Quality", "priority": "High"},
        {"id": "CP-12", "principle": "Transparent decision rationale", "agents": ["Code Generator", "Security Analyst", "Risk Manager", "Primary Care AI"], "category": "Explainability", "priority": "High"},
        {"id": "CP-13", "principle": "Escalate when confidence is below threshold", "agents": ["Code Generator", "Security Analyst", "Risk Manager", "Primary Care AI", "Compliance Officer"], "category": "Safety", "priority": "Critical"},
        {"id": "CP-14", "principle": "No hallucinated data or citations", "agents": ["Market Analyst", "Primary Care AI"], "category": "Integrity", "priority": "Critical"},
    ]


# ---------------------------------------------------------------------------
# Chart builders
# ---------------------------------------------------------------------------

def build_safety_gauge(score):
    """Build a plotly gauge chart for the overall safety score."""
    if score >= 0.90:
        bar_color = "#10b981"
    elif score >= 0.75:
        bar_color = "#f59e0b"
    else:
        bar_color = "#ef4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score * 100,
        number={"suffix": "%", "font": {"size": 42}},
        delta={"reference": 92, "increasing": {"color": "#10b981"}, "decreasing": {"color": "#ef4444"}},
        title={"text": "Overall Safety Score", "font": {"size": 16}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#667eea"},
            "bar": {"color": bar_color, "thickness": 0.3},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#e5e7eb",
            "steps": [
                {"range": [0, 60], "color": "#fef2f2"},
                {"range": [60, 75], "color": "#fffbeb"},
                {"range": [75, 90], "color": "#f0fdf4"},
                {"range": [90, 100], "color": "#ecfdf5"},
            ],
            "threshold": {
                "line": {"color": "#ef4444", "width": 3},
                "thickness": 0.8,
                "value": st.session_state.alert_threshold * 100,
            },
        },
    ))
    fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=10))
    return fig


def build_safety_trend_chart(history):
    """Build a line chart of safety score over time."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history["dates"],
        y=[s * 100 for s in history["scores"]],
        mode='lines+markers',
        name='Safety Score',
        line=dict(color='#667eea', width=3),
        marker=dict(size=5),
        fill='tozeroy',
        fillcolor='rgba(102,126,234,0.08)',
    ))
    # threshold line
    fig.add_hline(
        y=st.session_state.alert_threshold * 100,
        line_dash="dash",
        line_color="#ef4444",
        annotation_text=f"Alert Threshold ({st.session_state.alert_threshold:.0%})",
        annotation_position="bottom right",
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Safety Score (%)",
        yaxis=dict(range=[60, 100]),
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        hovermode="x unified",
    )
    return fig


def build_violations_by_category(violations):
    """Build a bar chart showing violation counts by category."""
    categories = {}
    for v in violations:
        # Map principles to categories
        cat = "Other"
        for p in st.session_state.constitutional_principles:
            if p["principle"] == v["principle"]:
                cat = p["category"]
                break
        categories[cat] = categories.get(cat, 0) + 1

    cats = list(categories.keys())
    counts = list(categories.values())
    colors = []
    palette = {"Security": "#ef4444", "Quality": "#f59e0b", "Safety": "#ef4444",
               "Compliance": "#764ba2", "Risk": "#f59e0b", "Integrity": "#667eea",
               "Explainability": "#10b981", "Other": "#6b7280"}
    for c in cats:
        colors.append(palette.get(c, "#6b7280"))

    fig = go.Figure(data=[go.Bar(x=cats, y=counts, marker_color=colors)])
    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Violations",
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    return fig


def build_intervention_reasons_pie(interventions):
    """Build a pie chart of intervention trigger reasons."""
    reasons = {}
    for intv in interventions:
        reasons[intv["trigger"]] = reasons.get(intv["trigger"], 0) + 1

    color_map = {
        "Safety Violation": "#ef4444",
        "Low Confidence": "#f59e0b",
        "Agent Disagreement": "#667eea",
        "Threshold Breach": "#764ba2",
        "Scheduled Review": "#10b981",
    }
    labels = list(reasons.keys())
    values = list(reasons.values())
    colors = [color_map.get(l, "#6b7280") for l in labels]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=colors),
        textinfo="label+percent",
        textposition="outside",
    )])
    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=10, b=10),
        showlegend=False,
    )
    return fig


def build_disagreement_heatmap():
    """Build a heatmap of pairwise agent agreement scores."""
    agents = ["Code Gen", "Sec Analyst", "Code Rev", "Test Gen", "Risk Mgr", "Compliance", "Primary Care"]
    np.random.seed(7)
    n = len(agents)
    matrix = np.ones((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            val = round(np.random.uniform(0.72, 0.99), 2)
            matrix[i][j] = val
            matrix[j][i] = val

    # Introduce a couple of lower agreement pairs for visual interest
    matrix[0][4] = 0.68
    matrix[4][0] = 0.68
    matrix[2][6] = 0.71
    matrix[6][2] = 0.71
    matrix[1][4] = 0.74
    matrix[4][1] = 0.74

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=agents,
        y=agents,
        colorscale=[
            [0.0, "#ef4444"],
            [0.3, "#f59e0b"],
            [0.6, "#fbbf24"],
            [0.8, "#a7f3d0"],
            [1.0, "#10b981"],
        ],
        zmin=0.5,
        zmax=1.0,
        text=np.round(matrix, 2),
        texttemplate="%{text}",
        textfont={"size": 11},
        hovertemplate="Agent A: %{y}<br>Agent B: %{x}<br>Agreement: %{z:.2f}<extra></extra>",
        colorbar=dict(title="Agreement", tickformat=".0%"),
    ))
    fig.update_layout(
        height=420,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(side="bottom"),
    )
    return fig, matrix, agents


# ---------------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------------

def main():
    init_safety_session_state()

    # Header
    st.markdown('<p class="main-header">Safety Dashboard</p>', unsafe_allow_html=True)
    st.markdown("Real-time safety monitoring, constitutional compliance, and intervention tracking for the CoHumAIn multi-agent system.")

    # Compute current aggregate safety score
    current_score = st.session_state.safety_score_history["scores"][-1]

    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_violations = len(st.session_state.violation_log)
        recent_violations = sum(1 for v in st.session_state.violation_log if "2024-02-07" in v["timestamp"])
        st.metric("Total Violations", total_violations, delta=f"+{recent_violations} today", delta_color="inverse")

    with col2:
        total_interventions = len(st.session_state.intervention_log)
        st.metric("Interventions (7 days)", total_interventions, delta="-2 vs last week")

    with col3:
        compliant_agents = sum(1 for a in st.session_state.agent_compliance.values() if a["compliance_rate"] >= 0.95)
        total_agents = len(st.session_state.agent_compliance)
        st.metric("Compliant Agents", f"{compliant_agents}/{total_agents}", delta="All within tolerance")

    with col4:
        mode = st.session_state.safety_mode
        mode_color = {
            "Permissive": "safety-card-warning",
            "Balanced": "safety-card-safe",
            "Strict": "safety-card-safe",
            "Maximum": "safety-card-critical",
        }.get(mode, "safety-card-safe")
        st.markdown(f"""
        <div class="{mode_color}">
            <div style="font-size: 0.875rem; color: #6b7280;">Safety Mode</div>
            <div style="font-size: 1.5rem; font-weight: 700;">{mode}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview",
        "Constitutional Principles",
        "Misalignment Detection",
        "Intervention Log",
        "Safety Trends",
    ])

    # ------------------------------------------------------------------
    # Tab 1 - Safety Overview
    # ------------------------------------------------------------------
    with tab1:
        show_safety_overview(current_score)

    # ------------------------------------------------------------------
    # Tab 2 - Constitutional Principles Monitor
    # ------------------------------------------------------------------
    with tab2:
        show_constitutional_monitor()

    # ------------------------------------------------------------------
    # Tab 3 - Misalignment Detection
    # ------------------------------------------------------------------
    with tab3:
        show_misalignment_detection()

    # ------------------------------------------------------------------
    # Tab 4 - Intervention Log
    # ------------------------------------------------------------------
    with tab4:
        show_intervention_log()

    # ------------------------------------------------------------------
    # Tab 5 - Safety Trends
    # ------------------------------------------------------------------
    with tab5:
        show_safety_trends()

    # ------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------
    with st.sidebar:
        show_sidebar()


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------

def show_safety_overview(current_score):
    """Tab 1: Safety Overview with gauge, agent status, and mode display."""
    st.subheader("Real-Time Safety Status")

    col_gauge, col_agents = st.columns([1, 2])

    with col_gauge:
        fig = build_safety_gauge(current_score)
        st.plotly_chart(fig, use_container_width=True)

        # Current safety mode card
        mode = st.session_state.safety_mode
        mode_descriptions = {
            "Permissive": "Agents operate with minimal constraints. Human review is optional. Suitable for low-risk experimentation.",
            "Balanced": "Standard guardrails active. Constitutional checks enforced. Human-on-the-loop for medium/high risk.",
            "Strict": "All outputs require constitutional validation. Human-in-the-loop for high risk. Tight confidence thresholds.",
            "Maximum": "Full lockdown. Every agent output requires human approval before delivery. All safety layers active.",
        }
        st.markdown(f"**Current Mode: {mode}**")
        st.caption(mode_descriptions.get(mode, ""))

    with col_agents:
        st.markdown("#### Agent Compliance Status")

        for agent_name, data in st.session_state.agent_compliance.items():
            rate = data["compliance_rate"]
            violations = data["violations"]

            if rate >= 0.98:
                badge = "status-badge-safe"
                badge_label = "Compliant"
            elif rate >= 0.95:
                badge = "status-badge-warning"
                badge_label = "Minor Issues"
            else:
                badge = "status-badge-critical"
                badge_label = "Review Needed"

            with st.container():
                c1, c2, c3 = st.columns([3, 4, 2])
                with c1:
                    st.markdown(f"**{agent_name}**")
                    st.markdown(f'<span class="{badge}">{badge_label}</span>', unsafe_allow_html=True)
                with c2:
                    st.progress(rate, text=f"Compliance: {rate:.1%} ({data['total_checks']} checks)")
                with c3:
                    st.markdown(f"Violations: **{violations}**")
                    if data["status"] == "Under Review":
                        st.warning("Under Review")

    st.divider()

    # Quick summary boxes
    st.markdown("#### Safety Summary")
    s1, s2, s3 = st.columns(3)
    with s1:
        critical_count = sum(1 for v in st.session_state.violation_log if v["severity"] == "Critical")
        st.markdown(f"""
        <div class="safety-card-critical">
            <div style="font-weight:600;">Critical Violations</div>
            <div style="font-size:2rem; font-weight:700; color:#ef4444;">{critical_count}</div>
            <div style="font-size:0.8rem; color:#6b7280;">Last 7 days</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        blocked_count = sum(1 for v in st.session_state.violation_log if v["status"] == "Blocked")
        st.markdown(f"""
        <div class="safety-card-warning">
            <div style="font-weight:600;">Outputs Blocked</div>
            <div style="font-size:2rem; font-weight:700; color:#f59e0b;">{blocked_count}</div>
            <div style="font-size:0.8rem; color:#6b7280;">Prevented by safety layer</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        resolved_count = sum(1 for v in st.session_state.violation_log if v["status"] == "Resolved")
        st.markdown(f"""
        <div class="safety-card-safe">
            <div style="font-weight:600;">Resolved Issues</div>
            <div style="font-size:2rem; font-weight:700; color:#10b981;">{resolved_count}</div>
            <div style="font-size:0.8rem; color:#6b7280;">Successfully remediated</div>
        </div>
        """, unsafe_allow_html=True)


def show_constitutional_monitor():
    """Tab 2: Constitutional Principles table, violations, and compliance bars."""
    st.subheader("Constitutional Principles Monitor")

    # Principles table
    st.markdown("#### Active Principles")

    principles = st.session_state.constitutional_principles
    df_principles = pd.DataFrame([
        {
            "ID": p["id"],
            "Principle": p["principle"],
            "Category": p["category"],
            "Priority": p["priority"],
            "Agents": ", ".join(p["agents"]),
        }
        for p in principles
    ])

    # Category filter
    categories = sorted(set(p["category"] for p in principles))
    selected_cats = st.multiselect("Filter by category", categories, default=categories)
    filtered_df = df_principles[df_principles["Category"].isin(selected_cats)]
    st.dataframe(filtered_df, use_container_width=True, hide_index=True, height=350)

    st.divider()

    # Violation history
    st.markdown("#### Violation History")

    severity_filter = st.multiselect(
        "Filter by severity",
        ["Critical", "High", "Medium", "Low"],
        default=["Critical", "High", "Medium", "Low"],
    )

    for v in st.session_state.violation_log:
        if v["severity"] not in severity_filter:
            continue

        severity_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(v["severity"], "")
        status_emoji = {"Resolved": "✅", "Escalated": "⚠️", "Blocked": "🛑"}.get(v["status"], "")

        with st.expander(f'{severity_emoji} {v["id"]} | {v["agent"]} - {v["principle"]} ({v["status"]})'):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**Timestamp:** {v['timestamp']}")
                st.markdown(f"**Description:** {v['description']}")
                st.markdown(f"**Resolution:** {v['resolution']}")
            with c2:
                st.markdown(f"**Severity:** {v['severity']}")
                st.markdown(f"**Status:** {status_emoji} {v['status']}")

    st.divider()

    # Per-agent compliance rate bars
    st.markdown("#### Compliance Rate by Agent")

    agent_names = list(st.session_state.agent_compliance.keys())
    rates = [st.session_state.agent_compliance[a]["compliance_rate"] for a in agent_names]

    colors = []
    for r in rates:
        if r >= 0.98:
            colors.append("#10b981")
        elif r >= 0.95:
            colors.append("#f59e0b")
        else:
            colors.append("#ef4444")

    fig = go.Figure(data=[go.Bar(
        x=agent_names,
        y=[r * 100 for r in rates],
        marker_color=colors,
        text=[f"{r:.1%}" for r in rates],
        textposition="outside",
    )])
    fig.update_layout(
        yaxis_title="Compliance Rate (%)",
        yaxis=dict(range=[80, 102]),
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)


def show_misalignment_detection():
    """Tab 3: Agent disagreement heatmap and emergent risk alerts."""
    st.subheader("Misalignment Detection")

    col_heat, col_alerts = st.columns([3, 2])

    with col_heat:
        st.markdown("#### Pairwise Agent Agreement Heatmap")
        fig, matrix, agents = build_disagreement_heatmap()
        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Scores below the alert threshold are highlighted. "
            "Low agreement between agent pairs may indicate misalignment or conflicting constitutional principles."
        )

    with col_alerts:
        st.markdown("#### Emergent Risk Alerts")

        threshold = st.session_state.alert_threshold

        # Detect low-agreement pairs
        alerts = []
        n = len(agents)
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] < threshold:
                    alerts.append({
                        "pair": f"{agents[i]} <-> {agents[j]}",
                        "score": matrix[i][j],
                        "severity": "High" if matrix[i][j] < 0.70 else "Medium",
                    })

        if alerts:
            for alert in sorted(alerts, key=lambda a: a["score"]):
                sev = alert["severity"]
                card_class = "safety-card-critical" if sev == "High" else "safety-card-warning"
                st.markdown(f"""
                <div class="{card_class}">
                    <div style="font-weight:600;">{alert['pair']}</div>
                    <div>Agreement: <strong>{alert['score']:.2f}</strong></div>
                    <div style="font-size:0.8rem;">Severity: {sev} | Below threshold of {threshold:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="safety-card-safe">
                <div style="font-weight:600;">No Misalignment Detected</div>
                <div style="font-size:0.85rem;">All agent pairs are above the agreement threshold.</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        st.markdown("#### Threshold-Based Alert System")

        st.markdown(f"**Current threshold:** {threshold:.2f}")
        st.markdown(f"**Active alerts:** {len(alerts)}")

        if alerts:
            st.warning(f"{len(alerts)} agent pair(s) below agreement threshold. Review recommended.")
        else:
            st.success("All agent pairs within acceptable alignment range.")

        st.divider()

        st.markdown("#### Potential Risks")

        risk_items = [
            {"risk": "Constitutional principle conflict between Code Generator and Risk Manager on data handling approach.", "level": "Medium", "detected": "2024-02-07 09:15"},
            {"risk": "Divergent confidence calibration curves between Primary Care AI and other agents.", "level": "Low", "detected": "2024-02-06 14:30"},
            {"risk": "Security Analyst and Risk Manager disagree on acceptable vulnerability severity thresholds.", "level": "Medium", "detected": "2024-02-05 11:45"},
        ]
        for r in risk_items:
            level_color = {"High": "safety-card-critical", "Medium": "safety-card-warning", "Low": "safety-card-safe"}.get(r["level"], "safety-card-safe")
            st.markdown(f"""
            <div class="{level_color}">
                <div style="font-weight:600;">Risk Level: {r['level']}</div>
                <div style="font-size:0.85rem;">{r['risk']}</div>
                <div style="font-size:0.75rem; color:#6b7280;">Detected: {r['detected']}</div>
            </div>
            """, unsafe_allow_html=True)


def show_intervention_log():
    """Tab 4: Timeline and detail view of all human interventions."""
    st.subheader("Human Intervention Log")

    # Timeline chart
    st.markdown("#### Intervention Timeline")
    interventions = st.session_state.intervention_log

    timeline_df = pd.DataFrame([
        {
            "Timestamp": intv["timestamp"],
            "Trigger": intv["trigger"],
            "Severity": intv["severity"],
            "Duration (min)": intv["duration_minutes"],
            "Outcome": intv["outcome"],
        }
        for intv in interventions
    ])

    severity_color = {"Critical": "#ef4444", "High": "#f59e0b", "Medium": "#667eea", "Low": "#10b981"}
    colors = [severity_color.get(intv["severity"], "#6b7280") for intv in interventions]

    fig = go.Figure()
    for i, intv in enumerate(interventions):
        fig.add_trace(go.Scatter(
            x=[intv["timestamp"]],
            y=[intv["duration_minutes"]],
            mode='markers+text',
            marker=dict(
                size=max(14, intv["duration_minutes"]),
                color=severity_color.get(intv["severity"], "#6b7280"),
                line=dict(width=2, color="white"),
            ),
            text=[intv["id"]],
            textposition="top center",
            hovertext=(
                f"<b>{intv['id']}</b><br>"
                f"Trigger: {intv['trigger']}<br>"
                f"Severity: {intv['severity']}<br>"
                f"Duration: {intv['duration_minutes']} min<br>"
                f"Operator: {intv['operator']}<br>"
                f"Outcome: {intv['outcome']}"
            ),
            hoverinfo="text",
            showlegend=False,
        ))

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Duration (minutes)",
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        hovermode="closest",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Summary table
    st.dataframe(timeline_df, use_container_width=True, hide_index=True)

    st.divider()

    # Expandable detail cards
    st.markdown("#### Intervention Details")

    trigger_filter = st.multiselect(
        "Filter by trigger",
        sorted(set(intv["trigger"] for intv in interventions)),
        default=sorted(set(intv["trigger"] for intv in interventions)),
    )

    for intv in interventions:
        if intv["trigger"] not in trigger_filter:
            continue

        severity_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(intv["severity"], "")
        outcome_emoji = {"Successful": "✅", "No Action Required": "ℹ️"}.get(intv["outcome"], "")

        with st.expander(f'{severity_emoji} {intv["id"]} | {intv["trigger"]} - {intv["timestamp"]}'):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**Description:** {intv['description']}")
                st.markdown(f"**Operator:** {intv['operator']}")
                st.markdown(f"**Action Taken:** {intv['action_taken']}")
                st.markdown(f"**Resolution:** {intv['resolution']}")
                if intv["agents_involved"]:
                    st.markdown(f"**Agents Involved:** {', '.join(intv['agents_involved'])}")
            with c2:
                st.markdown(f"**Severity:** {intv['severity']}")
                st.markdown(f"**Duration:** {intv['duration_minutes']} min")
                st.markdown(f"**Outcome:** {outcome_emoji} {intv['outcome']}")


def show_safety_trends():
    """Tab 5: Safety score line chart, violation bar chart, intervention pie chart."""
    st.subheader("Safety Trends & Analytics")

    # Row 1: Safety score over time
    st.markdown("#### Safety Score Over Time (30 Days)")
    fig_trend = build_safety_trend_chart(st.session_state.safety_score_history)
    st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()

    # Row 2: Violations by category + Intervention reasons
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Violations by Category")
        fig_bar = build_violations_by_category(st.session_state.violation_log)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown("#### Intervention Reasons")
        fig_pie = build_intervention_reasons_pie(st.session_state.intervention_log)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # Row 3: Additional trend metrics
    st.markdown("#### Key Trend Indicators")
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Avg Safety Score (30d)", f"{np.mean(st.session_state.safety_score_history['scores']):.1%}", delta="+1.2%")
    with m2:
        st.metric("Min Safety Score (30d)", f"{np.min(st.session_state.safety_score_history['scores']):.1%}", delta_color="inverse")
    with m3:
        st.metric("Mean Intervention Duration", "18.9 min", delta="-3.1 min")
    with m4:
        st.metric("Auto-Resolution Rate", "71%", delta="+5%")

    # Severity distribution over time
    st.markdown("#### Violation Severity Distribution (Last 7 Days)")
    severity_counts = {"Critical": 1, "High": 2, "Medium": 2, "Low": 2}
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    np.random.seed(99)
    fig_sev = go.Figure()
    for sev, base in [("Low", 2), ("Medium", 1), ("High", 1), ("Critical", 0)]:
        vals = [max(0, base + np.random.randint(-1, 2)) for _ in days]
        color = {"Critical": "#ef4444", "High": "#f59e0b", "Medium": "#667eea", "Low": "#10b981"}[sev]
        fig_sev.add_trace(go.Bar(x=days, y=vals, name=sev, marker_color=color))
    fig_sev.update_layout(
        barmode="stack",
        yaxis_title="Violations",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_sev, use_container_width=True)


def show_sidebar():
    """Render the sidebar with safety mode selector, thresholds, and notifications."""
    st.markdown("### Safety Controls")

    # Safety mode selector
    st.session_state.safety_mode = st.select_slider(
        "Safety Mode",
        options=["Permissive", "Balanced", "Strict", "Maximum"],
        value=st.session_state.safety_mode,
        help="Controls how aggressively safety mechanisms intervene.",
    )

    mode_icon = {"Permissive": "🟡", "Balanced": "🟢", "Strict": "🔵", "Maximum": "🔴"}
    st.info(f"{mode_icon.get(st.session_state.safety_mode, '')} Mode: **{st.session_state.safety_mode}**")

    st.divider()

    # Alert threshold
    st.markdown("### Alert Thresholds")

    st.session_state.alert_threshold = st.slider(
        "Agreement Threshold",
        min_value=0.50,
        max_value=0.95,
        value=st.session_state.alert_threshold,
        step=0.05,
        help="Agent pairs with agreement below this value trigger alerts.",
    )

    safety_floor = st.slider(
        "Safety Score Floor",
        min_value=0.50,
        max_value=0.95,
        value=0.85,
        step=0.05,
        help="System alert when aggregate safety score drops below this level.",
    )

    confidence_min = st.slider(
        "Min Confidence for Auto-Approval",
        min_value=0.50,
        max_value=0.99,
        value=0.80,
        step=0.05,
        help="Outputs below this confidence require human review.",
    )

    st.divider()

    # Notification settings
    st.markdown("### Notifications")

    st.session_state.notify_dashboard = st.checkbox("Dashboard alerts", value=st.session_state.notify_dashboard)
    st.session_state.notify_email = st.checkbox("Email notifications", value=st.session_state.notify_email)
    st.session_state.notify_slack = st.checkbox("Slack notifications", value=st.session_state.notify_slack)

    critical_only = st.checkbox("Critical severity only", value=False,
                                help="Only send notifications for critical-severity events.")

    st.divider()

    # Quick stats
    st.markdown("### Quick Stats")
    current_score = st.session_state.safety_score_history["scores"][-1]
    st.metric("Current Safety Score", f"{current_score:.1%}")
    st.metric("Active Principles", len(st.session_state.constitutional_principles))
    st.metric("Agents Monitored", len(st.session_state.agent_compliance))

    st.divider()

    # Actions
    st.markdown("### Actions")

    if st.button("Refresh Safety Data", use_container_width=True):
        st.session_state.safety_score_history = generate_safety_score_history()
        st.session_state.violation_log = generate_violation_log()
        st.session_state.intervention_log = generate_intervention_log()
        st.session_state.agent_compliance = generate_agent_compliance()
        st.success("Safety data refreshed.")
        st.rerun()

    if st.button("Export Safety Report", use_container_width=True):
        report = {
            "generated_at": datetime.now().isoformat(),
            "safety_mode": st.session_state.safety_mode,
            "current_score": current_score,
            "violations": st.session_state.violation_log,
            "interventions": st.session_state.intervention_log,
            "agent_compliance": {k: {kk: vv for kk, vv in v.items()} for k, v in st.session_state.agent_compliance.items()},
        }
        import json
        st.download_button(
            "Download Report (JSON)",
            json.dumps(report, indent=2, default=str),
            file_name="cohumain_safety_report.json",
            mime="application/json",
        )

    st.divider()
    st.markdown("### Support")
    st.markdown("""
    - [Safety Documentation](https://cohumain.ai/docs/safety)
    - [Compliance Guide](https://cohumain.ai/docs/compliance)
    - [Email Support](mailto:safety@cohumain.ai)
    """)


if __name__ == "__main__":
    main()
