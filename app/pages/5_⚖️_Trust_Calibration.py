"""
CoHumAIn Framework - Trust Calibration Page
Trust-building through calibrated confidence, automation level recommendations,
and collective confidence aggregation for explainable multi-agent systems.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

st.set_page_config(page_title="Trust Calibration", page_icon="⚖️", layout="wide")

# ---------------------------------------------------------------------------
# Custom CSS  (consistent with Home.py / other pages)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #667eea;
        margin-bottom: 0.75rem;
    }
    .metric-card-green {
        background-color: #ecfdf5;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #10b981;
        margin-bottom: 0.75rem;
    }
    .metric-card-yellow {
        background-color: #fffbeb;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #f59e0b;
        margin-bottom: 0.75rem;
    }
    .metric-card-red {
        background-color: #fef2f2;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #ef4444;
        margin-bottom: 0.75rem;
    }
    .status-safe  { color: #10b981; font-weight: bold; }
    .status-warning { color: #f59e0b; font-weight: bold; }
    .status-danger  { color: #ef4444; font-weight: bold; }
    .automation-bar {
        height: 12px;
        border-radius: 6px;
        background: linear-gradient(90deg, #10b981 0%, #f59e0b 50%, #ef4444 100%);
        position: relative;
        margin: 12px 0;
    }
    .automation-marker {
        width: 20px; height: 20px; border-radius: 50%;
        background: #667eea; border: 3px solid white;
        position: absolute; top: -4px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }
    .rec-card {
        background: linear-gradient(135deg, #f0f2f6 0%, #e8eaf6 100%);
        padding: 1.25rem; border-radius: 0.75rem;
        border-left: 4px solid #764ba2;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session-state initialisation & sample data helpers
# ---------------------------------------------------------------------------
AGENT_NAMES = ["Code Generator", "Security Analyst", "Code Reviewer", "Test Generator"]
AGENT_COLORS = {
    "Code Generator": "#667eea",
    "Security Analyst": "#ef4444",
    "Code Reviewer": "#10b981",
    "Test Generator": "#f59e0b",
}

np.random.seed(42)


def _generate_calibration_data(n_bins=10, bias=0.0):
    """Return (predicted_bins, actual_accuracy) with optional bias."""
    bins = np.linspace(0.05, 0.95, n_bins)
    noise = np.random.normal(0, 0.02, n_bins)
    actual = np.clip(bins + bias + noise, 0, 1)
    return bins, actual


def _compute_ece(predicted, actual, n_bins=10):
    """Expected Calibration Error."""
    return float(np.mean(np.abs(np.array(predicted) - np.array(actual))))


def _generate_trust_history(days=30):
    """Simulated daily trust scores."""
    base = 0.88
    dates = [datetime.now() - timedelta(days=days - i) for i in range(days)]
    scores = []
    for i in range(days):
        base += np.random.normal(0.002, 0.008)
        base = np.clip(base, 0.70, 0.99)
        scores.append(round(base, 4))
    return dates, scores


def _generate_task_log(n=20):
    """Recent task log with predicted vs actual outcomes."""
    tasks = []
    task_names = [
        "OAuth2 implementation", "SQL injection fix", "API rate limiter",
        "JWT token refresh", "Input validation", "RBAC module",
        "Logging middleware", "CORS configuration", "Data encryption",
        "Session management", "Webhook handler", "Cache invalidation",
        "Payment gateway", "Email verification", "Password reset flow",
        "File upload sanitiser", "Audit trail logger", "Load balancer config",
        "GraphQL resolver", "Docker health-check",
    ]
    for i in range(n):
        predicted_conf = round(np.random.uniform(0.65, 0.98), 2)
        # actual outcome correlated with predicted confidence (with noise)
        correct = np.random.random() < (predicted_conf + np.random.normal(0, 0.05))
        agent = np.random.choice(AGENT_NAMES)
        tasks.append({
            "task_id": f"TASK_{1000 + i}",
            "task": task_names[i % len(task_names)],
            "agent": agent,
            "predicted_confidence": predicted_conf,
            "actual_correct": bool(correct),
            "timestamp": (datetime.now() - timedelta(hours=n - i)).strftime(
                "%Y-%m-%d %H:%M"
            ),
        })
    return tasks


def init_trust_state():
    """Populate session state with sample trust data."""
    if "trust_initialized" not in st.session_state:
        st.session_state.trust_initialized = True

        # Per-agent trust scores
        st.session_state.agent_trust = {
            "Code Generator":   {"trust": 0.87, "expertise": 0.85, "calibration_bias": 0.02},
            "Security Analyst":  {"trust": 0.95, "expertise": 0.95, "calibration_bias": -0.01},
            "Code Reviewer":    {"trust": 0.91, "expertise": 0.89, "calibration_bias": 0.01},
            "Test Generator":   {"trust": 0.89, "expertise": 0.88, "calibration_bias": 0.03},
        }

        # Overall trust & history
        dates, scores = _generate_trust_history(30)
        st.session_state.trust_dates = dates
        st.session_state.trust_scores = scores
        st.session_state.overall_trust = scores[-1]

        # Task log
        st.session_state.task_log = _generate_task_log(20)

        # Sidebar defaults
        st.session_state.confidence_threshold = 0.80
        st.session_state.calibration_period = 30

        st.session_state.agent_weights = {
            "Code Generator": 0.85,
            "Security Analyst": 0.95,
            "Code Reviewer": 0.89,
            "Test Generator": 0.88,
        }


init_trust_state()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Calibration Controls")

    st.session_state.confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.50, max_value=0.99,
        value=st.session_state.confidence_threshold,
        step=0.01,
        help="Minimum collective confidence before the system acts autonomously.",
    )

    st.divider()
    st.markdown("### Agent Weight Adjustments")
    for agent in AGENT_NAMES:
        st.session_state.agent_weights[agent] = st.slider(
            agent,
            min_value=0.0, max_value=1.0,
            value=st.session_state.agent_weights[agent],
            step=0.05,
            key=f"weight_{agent}",
        )

    st.divider()
    st.markdown("### Calibration Period")
    st.session_state.calibration_period = st.selectbox(
        "Look-back window",
        options=[7, 14, 30, 60, 90],
        index=2,
        format_func=lambda d: f"Last {d} days",
    )

    st.divider()
    st.markdown("### System Status")
    trust_val = st.session_state.overall_trust
    if trust_val >= 0.90:
        st.success(f"Trust Score: {trust_val:.0%}")
    elif trust_val >= 0.80:
        st.warning(f"Trust Score: {trust_val:.0%}")
    else:
        st.error(f"Trust Score: {trust_val:.0%}")

    st.divider()
    st.markdown("### Quick Actions")
    if st.button("Recalibrate All Agents", use_container_width=True):
        st.toast("Recalibration started for all agents.")
    if st.button("Reset Weights to Defaults", use_container_width=True):
        for a in AGENT_NAMES:
            st.session_state.agent_weights[a] = st.session_state.agent_trust[a]["expertise"]
        st.rerun()

# ---------------------------------------------------------------------------
# Page Header
# ---------------------------------------------------------------------------
st.markdown('<p class="main-header">Trust Calibration</p>', unsafe_allow_html=True)
st.markdown(
    "Quantify, calibrate, and build trust across the multi-agent system through "
    "transparent confidence assessment and automation level recommendations."
)

# =========================================================================
# TAB LAYOUT
# =========================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Calibration Curves",
    "Automation Level",
    "Collective Confidence",
    "Historical Performance",
    "Recommendations",
])

# =========================================================================
# TAB 1 -- Trust Score Overview
# =========================================================================
with tab1:
    st.subheader("Trust Score Overview")

    # --- Large gauge for overall trust ---
    col_gauge, col_agents = st.columns([1, 2])

    with col_gauge:
        overall = st.session_state.overall_trust
        gauge_color = "#10b981" if overall >= 0.90 else ("#f59e0b" if overall >= 0.80 else "#ef4444")

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=overall * 100,
            number={"suffix": "%", "font": {"size": 48}},
            delta={"reference": st.session_state.trust_scores[-2] * 100,
                   "suffix": "%", "relative": False},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": gauge_color},
                "bgcolor": "#f0f2f6",
                "steps": [
                    {"range": [0, 70], "color": "#fef2f2"},
                    {"range": [70, 85], "color": "#fffbeb"},
                    {"range": [85, 100], "color": "#ecfdf5"},
                ],
                "threshold": {
                    "line": {"color": "#764ba2", "width": 3},
                    "thickness": 0.8,
                    "value": st.session_state.confidence_threshold * 100,
                },
            },
            title={"text": "Overall System Trust", "font": {"size": 16}},
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=30, r=30, t=60, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # --- Per-agent trust metric cards ---
    with col_agents:
        st.markdown("#### Per-Agent Trust Scores")
        agent_cols = st.columns(len(AGENT_NAMES))
        for idx, agent in enumerate(AGENT_NAMES):
            info = st.session_state.agent_trust[agent]
            t = info["trust"]
            card_class = (
                "metric-card-green" if t >= 0.90
                else ("metric-card-yellow" if t >= 0.80 else "metric-card-red")
            )
            status_class = (
                "status-safe" if t >= 0.90
                else ("status-warning" if t >= 0.80 else "status-danger")
            )
            with agent_cols[idx]:
                st.markdown(f"""
                <div class="{card_class}">
                    <div style="font-size:0.8rem;color:#6b7280;">{agent}</div>
                    <div class="{status_class}" style="font-size:1.75rem;">{t:.0%}</div>
                    <div style="font-size:0.75rem;color:#9ca3af;">Expertise {info['expertise']:.0%}</div>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # --- Trust trend over time ---
    st.markdown("#### Trust Score Trend")
    period = st.session_state.calibration_period
    dates = st.session_state.trust_dates[-period:]
    scores = st.session_state.trust_scores[-period:]

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=dates, y=[s * 100 for s in scores],
        mode="lines+markers",
        line=dict(color="#667eea", width=3),
        marker=dict(size=5),
        fill="tozeroy",
        fillcolor="rgba(102,126,234,0.10)",
        name="Trust Score",
    ))
    fig_trend.add_hline(
        y=st.session_state.confidence_threshold * 100,
        line_dash="dash", line_color="#764ba2", line_width=2,
        annotation_text=f"Threshold ({st.session_state.confidence_threshold:.0%})",
        annotation_position="top left",
    )
    fig_trend.update_layout(
        xaxis_title="Date",
        yaxis_title="Trust Score (%)",
        yaxis=dict(range=[60, 100]),
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# =========================================================================
# TAB 2 -- Calibration Curve Analysis
# =========================================================================
with tab2:
    st.subheader("Calibration Curve Analysis")
    st.markdown(
        "A well-calibrated system's predicted confidence matches its actual accuracy. "
        "Points close to the diagonal indicate good calibration."
    )

    col_chart, col_metrics = st.columns([3, 1])

    with col_chart:
        selected_agents = st.multiselect(
            "Select agents to display",
            AGENT_NAMES,
            default=AGENT_NAMES,
            key="cal_agent_select",
        )

        fig_cal = go.Figure()

        # Perfect calibration line
        fig_cal.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode="lines",
            line=dict(color="#9ca3af", dash="dash", width=2),
            name="Perfect Calibration",
        ))

        for agent in selected_agents:
            bias = st.session_state.agent_trust[agent]["calibration_bias"]
            bins, actual = _generate_calibration_data(n_bins=10, bias=bias)
            fig_cal.add_trace(go.Scatter(
                x=bins, y=actual,
                mode="lines+markers",
                line=dict(color=AGENT_COLORS[agent], width=3),
                marker=dict(size=8),
                name=agent,
            ))

        # System aggregate
        sys_bins, sys_actual = _generate_calibration_data(n_bins=10, bias=0.005)
        fig_cal.add_trace(go.Scatter(
            x=sys_bins, y=sys_actual,
            mode="lines+markers",
            line=dict(color="#764ba2", width=4, dash="dot"),
            marker=dict(size=10, symbol="diamond"),
            name="System Aggregate",
        ))

        fig_cal.update_layout(
            xaxis_title="Predicted Confidence",
            yaxis_title="Actual Accuracy",
            xaxis=dict(range=[0, 1]),
            yaxis=dict(range=[0, 1]),
            height=480,
            margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        )
        st.plotly_chart(fig_cal, use_container_width=True)

    with col_metrics:
        st.markdown("#### ECE Metrics")
        st.markdown(
            '<div style="font-size:0.75rem;color:#6b7280;margin-bottom:8px;">'
            "Expected Calibration Error &mdash; lower is better</div>",
            unsafe_allow_html=True,
        )

        # System ECE
        sys_ece = _compute_ece(sys_bins, sys_actual)
        ece_color = "#10b981" if sys_ece < 0.03 else ("#f59e0b" if sys_ece < 0.06 else "#ef4444")
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:{ece_color};">
            <div style="font-size:0.8rem;color:#6b7280;">System ECE</div>
            <div style="font-size:2rem;font-weight:bold;color:{ece_color};">{sys_ece:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

        for agent in AGENT_NAMES:
            bias = st.session_state.agent_trust[agent]["calibration_bias"]
            b, a = _generate_calibration_data(n_bins=10, bias=bias)
            ece = _compute_ece(b, a)
            label_color = AGENT_COLORS[agent]
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:{label_color};">
                <div style="font-size:0.8rem;color:#6b7280;">{agent}</div>
                <div style="font-size:1.25rem;font-weight:bold;">{ece:.4f}</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.markdown("#### Interpretation")
        st.info(
            "ECE < 0.03 = well-calibrated. "
            "ECE 0.03-0.06 = moderate. "
            "ECE > 0.06 = needs recalibration."
        )

# =========================================================================
# TAB 3 -- Automation Level Recommendation
# =========================================================================
with tab3:
    st.subheader("Automation Level Recommendation")
    st.markdown(
        "Based on current trust, confidence, and task stakes the system recommends "
        "an appropriate level of human oversight."
    )

    # Determine recommended level
    threshold = st.session_state.confidence_threshold
    trust = st.session_state.overall_trust

    if trust >= 0.92 and threshold <= 0.80:
        rec_level = "Out-of-the-Loop"
        rec_description = (
            "System operates autonomously with periodic audit. "
            "Human is notified only for exceptional events."
        )
        rec_color = "#10b981"
        marker_pct = 85
    elif trust >= 0.80:
        rec_level = "On-the-Loop"
        rec_description = (
            "System executes with human monitoring. "
            "Human can intervene but is not required to approve each step."
        )
        rec_color = "#f59e0b"
        marker_pct = 50
    else:
        rec_level = "In-the-Loop"
        rec_description = (
            "Human must approve every critical decision. "
            "System provides recommendations only."
        )
        rec_color = "#ef4444"
        marker_pct = 15

    col_rec, col_factors = st.columns([2, 1])

    with col_rec:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:{rec_color};padding:2rem;">
            <div style="font-size:0.9rem;color:#6b7280;">Recommended Automation Level</div>
            <div style="font-size:2.25rem;font-weight:bold;color:{rec_color};">{rec_level}</div>
            <div style="font-size:0.9rem;color:#4b5563;margin-top:0.5rem;">{rec_description}</div>
        </div>
        """, unsafe_allow_html=True)

        # Spectrum bar
        st.markdown("#### Automation Spectrum")
        st.markdown(f"""
        <div style="position:relative;margin:20px 0 40px 0;">
            <div class="automation-bar"></div>
            <div class="automation-marker" style="left:{marker_pct}%;"></div>
            <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#6b7280;margin-top:8px;">
                <span>In-the-Loop</span>
                <span>On-the-Loop</span>
                <span>Out-of-the-Loop</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Interactive "what-if" slider
        st.markdown("#### What-If Analysis")
        what_if_threshold = st.slider(
            "Adjust confidence threshold to preview automation level",
            min_value=0.50, max_value=0.99,
            value=threshold, step=0.01,
            key="what_if_slider",
        )
        if trust >= 0.92 and what_if_threshold <= 0.80:
            wi_level, wi_color = "Out-of-the-Loop", "#10b981"
        elif trust >= 0.80 or what_if_threshold <= 0.85:
            wi_level, wi_color = "On-the-Loop", "#f59e0b"
        else:
            wi_level, wi_color = "In-the-Loop", "#ef4444"

        st.markdown(
            f"With threshold **{what_if_threshold:.0%}** the recommended level would be: "
            f'<span style="color:{wi_color};font-weight:bold;">{wi_level}</span>',
            unsafe_allow_html=True,
        )

    with col_factors:
        st.markdown("#### Contributing Factors")

        factors = [
            ("Collective Confidence", trust, trust >= 0.85),
            ("Confidence Threshold", threshold, threshold <= 0.85),
            ("Task Stakes", 0.65, True),
            ("Safety Status", 0.96, True),
            ("Calibration Quality (1-ECE)", 1 - _compute_ece(sys_bins, sys_actual), True),
        ]
        for label, val, ok in factors:
            icon = "checkmark" if ok else "warning"
            badge = (
                '<span style="color:#10b981;font-weight:bold;">PASS</span>'
                if ok
                else '<span style="color:#f59e0b;font-weight:bold;">REVIEW</span>'
            )
            st.markdown(f"""
            <div class="metric-card" style="padding:0.75rem 1rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:0.85rem;">{label}</span>
                    {badge}
                </div>
                <div style="font-size:1.1rem;font-weight:bold;">{val:.0%}</div>
            </div>
            """, unsafe_allow_html=True)

# =========================================================================
# TAB 4 -- Collective Confidence Aggregation
# =========================================================================
with tab4:
    st.subheader("Collective Confidence Aggregation")
    st.markdown(
        "Visualise how individual agent confidences are combined into a single "
        "collective confidence score using expertise-weighted voting."
    )

    col_agg, col_viz = st.columns([1, 1])

    # Build per-agent confidence values (simulated latest task)
    agent_conf = {
        "Code Generator": 0.87,
        "Security Analyst": 0.94,
        "Code Reviewer": 0.91,
        "Test Generator": 0.88,
    }

    with col_agg:
        st.markdown("#### Individual Agent Confidences")
        for agent in AGENT_NAMES:
            c = agent_conf[agent]
            w = st.session_state.agent_weights[agent]
            st.markdown(f"**{agent}**  &mdash;  confidence {c:.0%}  |  weight {w:.2f}")
            st.progress(c)

        st.divider()

        # Compute weighted & unweighted
        weights = np.array([st.session_state.agent_weights[a] for a in AGENT_NAMES])
        confs = np.array([agent_conf[a] for a in AGENT_NAMES])

        unweighted = float(np.mean(confs))
        weighted = float(np.average(confs, weights=weights))

        mc1, mc2 = st.columns(2)
        with mc1:
            st.metric("Unweighted Mean", f"{unweighted:.2%}")
        with mc2:
            delta = weighted - unweighted
            st.metric("Weighted Mean", f"{weighted:.2%}",
                       delta=f"{delta:+.2%} vs unweighted")

    with col_viz:
        st.markdown("#### Expertise-Weighted Voting Breakdown")

        # Stacked horizontal bar showing each agent's weighted contribution
        contributions = weights * confs
        total = contributions.sum()
        pct = contributions / total * 100

        fig_vote = go.Figure()
        cumulative = 0.0
        for idx, agent in enumerate(AGENT_NAMES):
            fig_vote.add_trace(go.Bar(
                y=["Collective"],
                x=[pct[idx]],
                orientation="h",
                name=agent,
                marker_color=AGENT_COLORS[agent],
                text=f"{pct[idx]:.1f}%",
                textposition="inside",
                hovertemplate=(
                    f"{agent}<br>"
                    f"Confidence: {confs[idx]:.0%}<br>"
                    f"Weight: {weights[idx]:.2f}<br>"
                    f"Contribution: {pct[idx]:.1f}%<extra></extra>"
                ),
            ))
            cumulative += pct[idx]

        fig_vote.update_layout(
            barmode="stack",
            height=120,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(title="Contribution (%)", range=[0, 100]),
            yaxis=dict(visible=False),
            legend=dict(orientation="h", yanchor="top", y=-0.6),
        )
        st.plotly_chart(fig_vote, use_container_width=True)

        st.divider()
        st.markdown("#### Weighted vs Unweighted Comparison")

        comp_df = pd.DataFrame({
            "Agent": AGENT_NAMES,
            "Confidence": confs,
            "Weight": weights,
            "Weighted Contribution": contributions,
        })

        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=AGENT_NAMES, y=confs,
            name="Raw Confidence",
            marker_color="rgba(102,126,234,0.45)",
        ))
        fig_comp.add_trace(go.Bar(
            x=AGENT_NAMES, y=contributions / weights.max(),
            name="Weighted Confidence",
            marker_color="rgba(118,75,162,0.75)",
        ))
        fig_comp.update_layout(
            barmode="group",
            yaxis_title="Score",
            height=320,
            margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        st.markdown(
            f"**Final Collective Confidence:** "
            f'<span style="font-size:1.5rem;font-weight:bold;color:#667eea;">'
            f"{weighted:.2%}</span>",
            unsafe_allow_html=True,
        )

# =========================================================================
# TAB 5 -- Historical Trust Performance
# =========================================================================
with tab5:
    st.subheader("Historical Trust Performance")

    task_log = st.session_state.task_log

    # --- Recent tasks table ---
    st.markdown("#### Recent Tasks: Predicted vs Actual")
    log_df = pd.DataFrame(task_log)
    log_df["Outcome"] = log_df["actual_correct"].map({True: "Correct", False: "Incorrect"})
    log_df["Calibration Gap"] = log_df.apply(
        lambda r: round(r["predicted_confidence"] - (1.0 if r["actual_correct"] else 0.0), 2),
        axis=1,
    )

    display_df = log_df[[
        "task_id", "task", "agent", "predicted_confidence", "Outcome", "Calibration Gap", "timestamp"
    ]].rename(columns={
        "task_id": "ID",
        "task": "Task",
        "agent": "Agent",
        "predicted_confidence": "Predicted Conf.",
        "timestamp": "Timestamp",
    })
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=380)

    st.divider()

    col_acc, col_bias = st.columns(2)

    with col_acc:
        st.markdown("#### Rolling Accuracy Over Time")
        # Compute rolling accuracy (window=5)
        correct_series = log_df["actual_correct"].astype(int)
        rolling_acc = correct_series.rolling(window=5, min_periods=1).mean()

        fig_acc = go.Figure()
        fig_acc.add_trace(go.Scatter(
            x=list(range(len(rolling_acc))),
            y=rolling_acc.values * 100,
            mode="lines+markers",
            line=dict(color="#667eea", width=3),
            marker=dict(size=6),
            fill="tozeroy",
            fillcolor="rgba(102,126,234,0.08)",
            name="Rolling Accuracy (w=5)",
        ))
        fig_acc.add_hline(
            y=st.session_state.confidence_threshold * 100,
            line_dash="dash", line_color="#764ba2",
            annotation_text="Threshold",
        )
        fig_acc.update_layout(
            xaxis_title="Task Sequence",
            yaxis_title="Accuracy (%)",
            yaxis=dict(range=[40, 105]),
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_acc, use_container_width=True)

    with col_bias:
        st.markdown("#### Over-confidence & Under-confidence Detection")

        conf_vals = log_df["predicted_confidence"].values
        outcomes = log_df["actual_correct"].astype(int).values
        gaps = conf_vals - outcomes

        overconfident = int((gaps > 0.15).sum())
        underconfident = int((gaps < -0.15).sum())
        well_calibrated = len(gaps) - overconfident - underconfident

        fig_bias = go.Figure(data=[go.Pie(
            labels=["Well-Calibrated", "Over-confident", "Under-confident"],
            values=[well_calibrated, overconfident, underconfident],
            hole=0.45,
            marker=dict(colors=["#10b981", "#ef4444", "#f59e0b"]),
            textinfo="label+value",
        )])
        fig_bias.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_bias, use_container_width=True)

        if overconfident > underconfident:
            st.warning(
                f"System shows over-confidence bias ({overconfident} of {len(gaps)} predictions). "
                "Consider increasing confidence thresholds or retraining under-performing agents."
            )
        elif underconfident > overconfident:
            st.info(
                f"System is conservative ({underconfident} under-confident predictions). "
                "Trust scores could be higher with better self-assessment."
            )
        else:
            st.success("System is well-calibrated across recent tasks.")

# =========================================================================
# TAB 6 -- Trust Building Recommendations
# =========================================================================
with tab6:
    st.subheader("Trust Building Recommendations")
    st.markdown(
        "Actionable insights generated from recent calibration analysis and "
        "per-agent performance history."
    )

    # --- System-level recommendations ---
    st.markdown("#### System-Level Insights")

    sys_ece = _compute_ece(sys_bins, sys_actual)

    system_recs = []
    if sys_ece > 0.04:
        system_recs.append({
            "priority": "High",
            "title": "Recalibrate Confidence Estimators",
            "detail": (
                f"System ECE ({sys_ece:.4f}) exceeds the 0.04 target. "
                "Run a recalibration pass using the most recent task outcomes "
                "to adjust internal confidence estimators."
            ),
            "color": "#ef4444",
        })
    if st.session_state.overall_trust < 0.90:
        system_recs.append({
            "priority": "Medium",
            "title": "Increase Transparency Windows",
            "detail": (
                "Overall trust has not yet reached the 90% mark. "
                "Increase the frequency of explanation generation and "
                "expose more intermediate reasoning to human operators."
            ),
            "color": "#f59e0b",
        })

    task_log_df = pd.DataFrame(st.session_state.task_log)
    accuracy = task_log_df["actual_correct"].mean()
    if accuracy < 0.85:
        system_recs.append({
            "priority": "High",
            "title": "Review Agent Collaboration Patterns",
            "detail": (
                f"Overall accuracy ({accuracy:.0%}) is below the 85% target. "
                "Analyse recent incorrect predictions to identify systematic "
                "failure modes in agent coordination."
            ),
            "color": "#ef4444",
        })

    system_recs.append({
        "priority": "Low",
        "title": "Expand Calibration Dataset",
        "detail": (
            "Continuously adding validated outcomes to the calibration dataset "
            "improves ECE estimation reliability. Aim for at least 200 "
            "labelled outcomes per agent."
        ),
        "color": "#667eea",
    })

    for rec in system_recs:
        st.markdown(f"""
        <div class="rec-card" style="border-left-color:{rec['color']};">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-weight:bold;font-size:1rem;">{rec['title']}</span>
                <span style="font-size:0.75rem;padding:2px 8px;border-radius:4px;
                       background:{rec['color']}20;color:{rec['color']};font-weight:600;">
                    {rec['priority']}
                </span>
            </div>
            <div style="font-size:0.875rem;color:#4b5563;margin-top:0.5rem;">
                {rec['detail']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- Per-agent recommendations ---
    st.markdown("#### Agent-Specific Recommendations")

    agent_rec_cols = st.columns(2)
    for idx, agent in enumerate(AGENT_NAMES):
        info = st.session_state.agent_trust[agent]
        bias = info["calibration_bias"]
        agent_tasks = task_log_df[task_log_df["agent"] == agent]
        agent_accuracy = agent_tasks["actual_correct"].mean() if len(agent_tasks) > 0 else 1.0

        recs = []
        if abs(bias) > 0.02:
            direction = "over-confident" if bias > 0 else "under-confident"
            recs.append(
                f"Agent is {direction} (bias={bias:+.3f}). "
                f"Adjust internal confidence scoring."
            )
        if agent_accuracy < 0.85:
            recs.append(
                f"Accuracy ({agent_accuracy:.0%}) is below target. "
                f"Review recent incorrect predictions for this agent."
            )
        if info["trust"] < 0.90:
            recs.append(
                "Trust score is below 90%. Increase logging verbosity and "
                "provide more detailed reasoning chains."
            )
        if not recs:
            recs.append("Agent is performing well. No action required.")

        col_target = agent_rec_cols[idx % 2]
        with col_target:
            color = AGENT_COLORS[agent]
            rec_html = "".join(
                f'<li style="margin-bottom:4px;">{r}</li>' for r in recs
            )
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:{color};">
                <div style="font-weight:bold;color:{color};margin-bottom:6px;">{agent}</div>
                <div style="font-size:0.8rem;color:#6b7280;margin-bottom:4px;">
                    Trust {info['trust']:.0%} &nbsp;|&nbsp; Accuracy {agent_accuracy:.0%} &nbsp;|&nbsp; Bias {bias:+.3f}
                </div>
                <ul style="font-size:0.85rem;color:#374151;padding-left:1.25rem;margin:0;">
                    {rec_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # --- Quick-action buttons ---
    st.markdown("#### Quick Actions")
    qa_cols = st.columns(4)
    with qa_cols[0]:
        if st.button("Run Full Recalibration", type="primary", use_container_width=True):
            st.toast("Full recalibration queued. Results will appear in 30-60 seconds.")
    with qa_cols[1]:
        if st.button("Generate Trust Report", use_container_width=True):
            st.toast("PDF trust report is being generated.")
    with qa_cols[2]:
        if st.button("Export Calibration Data", use_container_width=True):
            export_data = {
                "overall_trust": st.session_state.overall_trust,
                "agent_trust": st.session_state.agent_trust,
                "agent_weights": st.session_state.agent_weights,
                "confidence_threshold": st.session_state.confidence_threshold,
            }
            st.download_button(
                "Download JSON",
                json.dumps(export_data, indent=2),
                file_name="trust_calibration_export.json",
                mime="application/json",
            )
    with qa_cols[3]:
        if st.button("Schedule Daily Audit", use_container_width=True):
            st.toast("Daily trust audit scheduled at 00:00 UTC.")
