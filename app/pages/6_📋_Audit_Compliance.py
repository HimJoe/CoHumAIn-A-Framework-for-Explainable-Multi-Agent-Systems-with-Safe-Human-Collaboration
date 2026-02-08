"""
CoHumAIn Framework - Audit & Compliance Page
Regulatory compliance tracking, audit trail management, and stakeholder reporting
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from datetime import datetime, timedelta
import random
import io
import csv

st.set_page_config(page_title="Audit & Compliance", page_icon="📋", layout="wide")

# ---------------------------------------------------------------------------
# Custom CSS -- consistent with the rest of the CoHumAIn app
# ---------------------------------------------------------------------------
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
    .compliance-safe {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .compliance-warning {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .compliance-critical {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .status-safe { color: #10b981; font-weight: bold; }
    .status-warning { color: #f59e0b; font-weight: bold; }
    .status-danger { color: #ef4444; font-weight: bold; }
    .provenance-step {
        border-left: 3px solid #667eea;
        padding-left: 1rem;
        margin-bottom: 0.75rem;
    }
    .report-section {
        background-color: #f8f9fa;
        padding: 1rem 1.25rem;
        border-radius: 0.5rem;
        margin-bottom: 0.75rem;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session-state initialisation & sample data
# ---------------------------------------------------------------------------

def _generate_audit_entries():
    """Return a list of sample audit-trail entries."""
    agents_pool = [
        "Code Generator", "Security Analyst", "Code Reviewer",
        "Test Generator", "Risk Manager", "Compliance Officer",
        "Market Analyst", "Radiologist AI", "Pathologist AI",
    ]
    tasks = [
        ("Implement OAuth 2.0 authentication", "Software Engineering"),
        ("Scan API endpoints for OWASP Top-10", "Security"),
        ("Refactor database query layer", "Software Engineering"),
        ("Assess credit-risk exposure for Q4", "Finance"),
        ("Generate unit tests for payment module", "Software Engineering"),
        ("Evaluate HIPAA compliance of data pipeline", "Healthcare"),
        ("Review trading algorithm edge cases", "Finance"),
        ("Detect anomalous transaction patterns", "Finance"),
        ("Validate patient-data anonymisation", "Healthcare"),
        ("Audit model bias in loan approvals", "Finance"),
        ("Patch XSS vulnerability in user input", "Security"),
        ("Generate integration tests for auth flow", "Software Engineering"),
        ("Review radiology diagnostic model", "Healthcare"),
        ("Update encryption standards to AES-256", "Security"),
        ("Verify GDPR data-deletion workflow", "Compliance"),
        ("Assess EU AI Act risk classification", "Compliance"),
        ("Validate FDA SaMD documentation", "Healthcare"),
        ("Review SEC algorithmic trading safeguards", "Finance"),
    ]
    safety_choices = ["Safe", "Safe", "Safe", "Warning", "Warning", "Critical"]
    decisions = [
        "Approved with full consensus",
        "Approved after revision cycle",
        "Escalated to human reviewer",
        "Approved with conditions",
        "Rejected - safety violation",
        "Approved after peer review",
        "Deferred pending additional data",
    ]

    random.seed(42)
    base_time = datetime(2024, 2, 7, 8, 0, 0)
    entries = []
    for idx, (task, domain) in enumerate(tasks):
        num_agents = random.randint(2, 4)
        involved = random.sample(agents_pool, num_agents)
        confidence = round(random.uniform(0.72, 0.99), 2)
        safety = random.choice(safety_choices)
        human = random.choice([True, False, False, False])
        decision = random.choice(decisions)
        ts = base_time + timedelta(minutes=idx * 47 + random.randint(0, 15))

        entries.append({
            "id": f"DEC-2024-{idx + 1:04d}",
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "task": task,
            "domain": domain,
            "agents": involved,
            "decision": decision,
            "confidence": confidence,
            "safety_status": safety,
            "human_intervention": human,
            "reasoning": [
                f"Agent {involved[0]} initiated analysis based on task requirements.",
                f"Agent {involved[1] if len(involved) > 1 else involved[0]} cross-validated findings against policy constraints.",
                f"Collective confidence computed via weighted voting: {confidence:.0%}.",
                "Constitutional alignment verified across all participating agents.",
                f"Final decision: {decision}.",
            ],
            "data_sources": [
                "Internal policy database v3.2",
                "OWASP Top-10 2024",
                "Historical decision log",
                "Regulatory framework reference",
            ],
        })
    return entries


def _init_session_state():
    if "audit_entries" not in st.session_state:
        st.session_state.audit_entries = _generate_audit_entries()
    if "selected_framework" not in st.session_state:
        st.session_state.selected_framework = "EU AI Act"
    if "date_range" not in st.session_state:
        st.session_state.date_range = (
            datetime(2024, 2, 7).date(),
            datetime(2024, 2, 8).date(),
        )
    if "stakeholder_view" not in st.session_state:
        st.session_state.stakeholder_view = "Auditor"


_init_session_state()

# ---------------------------------------------------------------------------
# Compliance framework data
# ---------------------------------------------------------------------------

COMPLIANCE_FRAMEWORKS = {
    "GDPR": {
        "full_name": "General Data Protection Regulation",
        "categories": {
            "Data Minimisation": {"score": 94, "status": "safe"},
            "Purpose Limitation": {"score": 91, "status": "safe"},
            "Right to Explanation": {"score": 97, "status": "safe"},
            "Data Subject Access": {"score": 88, "status": "safe"},
            "Data Portability": {"score": 82, "status": "warning"},
            "Breach Notification": {"score": 96, "status": "safe"},
            "Data Protection Impact": {"score": 79, "status": "warning"},
            "Consent Management": {"score": 93, "status": "safe"},
        },
        "overall": 90,
    },
    "EU AI Act": {
        "full_name": "EU Artificial Intelligence Act",
        "categories": {
            "Risk Classification": {"score": 95, "status": "safe"},
            "Transparency Requirements": {"score": 98, "status": "safe"},
            "Human Oversight": {"score": 93, "status": "safe"},
            "Technical Documentation": {"score": 86, "status": "warning"},
            "Post-Market Monitoring": {"score": 88, "status": "safe"},
            "Conformity Assessment": {"score": 81, "status": "warning"},
            "Bias & Fairness": {"score": 77, "status": "warning"},
            "Robustness & Accuracy": {"score": 92, "status": "safe"},
        },
        "overall": 89,
    },
    "HIPAA": {
        "full_name": "Health Insurance Portability and Accountability Act",
        "categories": {
            "PHI Safeguards": {"score": 96, "status": "safe"},
            "Access Controls": {"score": 94, "status": "safe"},
            "Audit Controls": {"score": 91, "status": "safe"},
            "Transmission Security": {"score": 97, "status": "safe"},
            "Breach Notification": {"score": 93, "status": "safe"},
            "Business Associates": {"score": 72, "status": "critical"},
            "Minimum Necessary": {"score": 89, "status": "safe"},
            "Patient Rights": {"score": 95, "status": "safe"},
        },
        "overall": 91,
    },
    "SEC": {
        "full_name": "Securities and Exchange Commission Regulations",
        "categories": {
            "Algorithmic Trading Safeguards": {"score": 88, "status": "safe"},
            "Market Manipulation Prevention": {"score": 91, "status": "safe"},
            "Disclosure Requirements": {"score": 85, "status": "warning"},
            "Record Keeping": {"score": 93, "status": "safe"},
            "Risk Controls": {"score": 90, "status": "safe"},
            "Reporting Obligations": {"score": 87, "status": "safe"},
            "Conflict of Interest": {"score": 78, "status": "warning"},
            "Client Protection": {"score": 94, "status": "safe"},
        },
        "overall": 88,
    },
    "FDA": {
        "full_name": "Food and Drug Administration (SaMD)",
        "categories": {
            "Software Validation": {"score": 92, "status": "safe"},
            "Clinical Evaluation": {"score": 84, "status": "warning"},
            "Risk Management (ISO 14971)": {"score": 90, "status": "safe"},
            "Quality Management System": {"score": 87, "status": "safe"},
            "Post-Market Surveillance": {"score": 76, "status": "warning"},
            "Labelling & Instructions": {"score": 95, "status": "safe"},
            "Change Control": {"score": 83, "status": "warning"},
            "Cybersecurity": {"score": 91, "status": "safe"},
        },
        "overall": 87,
    },
}

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📋 Audit Controls")

    st.markdown("**Date Range**")
    date_start = st.date_input(
        "From",
        value=st.session_state.date_range[0],
        key="sidebar_date_start",
    )
    date_end = st.date_input(
        "To",
        value=st.session_state.date_range[1],
        key="sidebar_date_end",
    )
    st.session_state.date_range = (date_start, date_end)

    st.divider()

    st.markdown("**Regulatory Framework**")
    st.session_state.selected_framework = st.selectbox(
        "Select Framework",
        list(COMPLIANCE_FRAMEWORKS.keys()),
        index=list(COMPLIANCE_FRAMEWORKS.keys()).index(
            st.session_state.selected_framework
        ),
        key="sidebar_framework",
    )

    st.divider()

    st.markdown("**Stakeholder View**")
    st.session_state.stakeholder_view = st.radio(
        "Perspective",
        ["Developer", "Auditor", "Regulator", "End User"],
        index=["Developer", "Auditor", "Regulator", "End User"].index(
            st.session_state.stakeholder_view
        ),
        key="sidebar_stakeholder",
    )

    st.divider()

    st.markdown("**Export Options**")
    export_fmt = st.selectbox(
        "Format",
        ["JSON", "CSV", "PDF Report"],
        key="sidebar_export_fmt",
    )
    if st.button("📥 Export Audit Trail", use_container_width=True):
        if export_fmt == "JSON":
            st.download_button(
                "Download JSON",
                json.dumps(st.session_state.audit_entries, indent=2),
                file_name="cohumain_audit_trail.json",
                mime="application/json",
            )
        elif export_fmt == "CSV":
            rows = []
            for e in st.session_state.audit_entries:
                rows.append({
                    "ID": e["id"],
                    "Timestamp": e["timestamp"],
                    "Task": e["task"],
                    "Domain": e["domain"],
                    "Agents": "; ".join(e["agents"]),
                    "Decision": e["decision"],
                    "Confidence": e["confidence"],
                    "Safety": e["safety_status"],
                    "Human Intervention": e["human_intervention"],
                })
            csv_buf = io.StringIO()
            writer = csv.DictWriter(csv_buf, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
            st.download_button(
                "Download CSV",
                csv_buf.getvalue(),
                file_name="cohumain_audit_trail.csv",
                mime="text/csv",
            )
        else:
            st.info("PDF export is generated in the Regulatory Reports tab.")

    st.divider()

    st.markdown("### System Status")
    st.success("Audit system active")
    fw = COMPLIANCE_FRAMEWORKS[st.session_state.selected_framework]
    overall = fw["overall"]
    if overall >= 90:
        st.success(f"Compliance: {overall}%")
    elif overall >= 80:
        st.warning(f"Compliance: {overall}%")
    else:
        st.error(f"Compliance: {overall}%")

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.markdown('<p class="main-header">📋 Audit & Compliance</p>', unsafe_allow_html=True)
st.markdown(
    "Regulatory compliance tracking, decision audit trails, and stakeholder reporting "
    "for the CoHumAIn multi-agent system."
)

# ---------------------------------------------------------------------------
# Helper to adapt content depth to the selected stakeholder view
# ---------------------------------------------------------------------------
VIEW = st.session_state.stakeholder_view

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Compliance Dashboard",
    "📜 Audit Trail",
    "🔗 Decision Provenance",
    "📄 Regulatory Reports",
    "👥 Stakeholder Views",
])

# ===================================================================
# TAB 1 -- Compliance Dashboard
# ===================================================================
with tab1:
    st.subheader("Compliance Dashboard")

    fw_key = st.session_state.selected_framework
    fw = COMPLIANCE_FRAMEWORKS[fw_key]

    st.markdown(f"**Active Framework:** {fw_key} -- {fw['full_name']}")

    # Framework selector row (quick-switch buttons)
    fw_cols = st.columns(len(COMPLIANCE_FRAMEWORKS))
    for idx, (fk, fv) in enumerate(COMPLIANCE_FRAMEWORKS.items()):
        with fw_cols[idx]:
            delta_color = "normal"
            if fv["overall"] >= 90:
                status_label = "Compliant"
            elif fv["overall"] >= 80:
                status_label = "Needs Attention"
                delta_color = "inverse"
            else:
                status_label = "At Risk"
                delta_color = "inverse"
            st.metric(
                label=fk,
                value=f"{fv['overall']}%",
                delta=status_label,
                delta_color=delta_color,
            )

    st.divider()

    # Key metrics row
    entries = st.session_state.audit_entries
    total_decisions = len(entries)
    safe_count = sum(1 for e in entries if e["safety_status"] == "Safe")
    warning_count = sum(1 for e in entries if e["safety_status"] == "Warning")
    critical_count = sum(1 for e in entries if e["safety_status"] == "Critical")
    intervention_count = sum(1 for e in entries if e["human_intervention"])
    avg_confidence = sum(e["confidence"] for e in entries) / len(entries)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Decisions", total_decisions)
    m2.metric("Avg Confidence", f"{avg_confidence:.0%}")
    m3.metric("Safe Outcomes", safe_count, delta=f"{safe_count/total_decisions:.0%}")
    m4.metric("Warnings / Critical", f"{warning_count} / {critical_count}")
    m5.metric("Human Interventions", intervention_count)

    st.divider()

    # Detailed category breakdown for the selected framework
    st.markdown(f"### {fw_key} Category Compliance")

    cat_cols = st.columns(4)
    for idx, (cat, info) in enumerate(fw["categories"].items()):
        col = cat_cols[idx % 4]
        with col:
            css_class = {
                "safe": "compliance-safe",
                "warning": "compliance-warning",
                "critical": "compliance-critical",
            }[info["status"]]
            icon = {"safe": "🟢", "warning": "🟡", "critical": "🔴"}[info["status"]]
            st.markdown(
                f'<div class="{css_class}">{icon} <strong>{cat}</strong><br/>'
                f'Score: {info["score"]}%</div>',
                unsafe_allow_html=True,
            )

    st.divider()

    # Compliance trend chart
    st.markdown("### Compliance Score Trend (Last 12 Months)")

    months = [
        "Mar", "Apr", "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec", "Jan", "Feb",
    ]
    random.seed(7)
    trend_data = {}
    for fk in COMPLIANCE_FRAMEWORKS:
        base = COMPLIANCE_FRAMEWORKS[fk]["overall"]
        trend_data[fk] = [
            max(60, min(100, base - 8 + i * 0.6 + random.randint(-2, 2)))
            for i in range(12)
        ]
        trend_data[fk][-1] = base  # ensure current month matches overall

    fig = go.Figure()
    colors = ["#667eea", "#764ba2", "#10b981", "#f59e0b", "#ef4444"]
    for idx, (fk, vals) in enumerate(trend_data.items()):
        fig.add_trace(go.Scatter(
            x=months,
            y=vals,
            mode="lines+markers",
            name=fk,
            line=dict(color=colors[idx % len(colors)], width=2),
            marker=dict(size=6),
        ))
    fig.update_layout(
        yaxis_title="Compliance Score (%)",
        xaxis_title="Month",
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)

# ===================================================================
# TAB 2 -- Audit Trail
# ===================================================================
with tab2:
    st.subheader("Decision Audit Trail")
    st.markdown("Searchable log of all decisions made by the multi-agent system.")

    # Filters
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        search_query = st.text_input("Search tasks", "", key="audit_search")
    with f2:
        safety_filter = st.multiselect(
            "Safety Status",
            ["Safe", "Warning", "Critical"],
            default=["Safe", "Warning", "Critical"],
            key="audit_safety_filter",
        )
    with f3:
        domain_filter = st.multiselect(
            "Domain",
            list({e["domain"] for e in entries}),
            default=list({e["domain"] for e in entries}),
            key="audit_domain_filter",
        )
    with f4:
        intervention_filter = st.selectbox(
            "Human Intervention",
            ["All", "Yes", "No"],
            key="audit_intervention_filter",
        )

    # Apply filters
    filtered = entries
    if search_query:
        sq = search_query.lower()
        filtered = [e for e in filtered if sq in e["task"].lower() or sq in e["id"].lower()]
    filtered = [e for e in filtered if e["safety_status"] in safety_filter]
    filtered = [e for e in filtered if e["domain"] in domain_filter]
    if intervention_filter == "Yes":
        filtered = [e for e in filtered if e["human_intervention"]]
    elif intervention_filter == "No":
        filtered = [e for e in filtered if not e["human_intervention"]]

    st.markdown(f"**Showing {len(filtered)} of {len(entries)} entries**")

    # Summary table
    table_rows = []
    for e in filtered:
        safety_icon = {"Safe": "🟢", "Warning": "🟡", "Critical": "🔴"}[e["safety_status"]]
        table_rows.append({
            "ID": e["id"],
            "Timestamp": e["timestamp"],
            "Task": e["task"],
            "Domain": e["domain"],
            "Agents": ", ".join(e["agents"]),
            "Decision": e["decision"],
            "Confidence": f"{e['confidence']:.0%}",
            "Safety": f"{safety_icon} {e['safety_status']}",
            "Human": "Yes" if e["human_intervention"] else "No",
        })

    df_audit = pd.DataFrame(table_rows)
    st.dataframe(df_audit, use_container_width=True, hide_index=True, height=400)

    # Expandable details
    st.markdown("### Decision Details")
    st.markdown("Select a decision to view full provenance.")

    selected_id = st.selectbox(
        "Decision ID",
        [e["id"] for e in filtered],
        key="audit_detail_id",
    )
    selected_entry = next((e for e in filtered if e["id"] == selected_id), None)

    if selected_entry:
        with st.expander(f"Full details for {selected_id}", expanded=True):
            d1, d2 = st.columns([2, 1])
            with d1:
                st.markdown(f"**Task:** {selected_entry['task']}")
                st.markdown(f"**Timestamp:** {selected_entry['timestamp']}")
                st.markdown(f"**Domain:** {selected_entry['domain']}")
                st.markdown(f"**Agents:** {', '.join(selected_entry['agents'])}")
                st.markdown(f"**Decision:** {selected_entry['decision']}")
                st.markdown("**Reasoning Chain:**")
                for step_idx, step in enumerate(selected_entry["reasoning"], 1):
                    st.markdown(
                        f'<div class="provenance-step">'
                        f"<strong>Step {step_idx}:</strong> {step}</div>",
                        unsafe_allow_html=True,
                    )
            with d2:
                st.markdown("**Metrics**")
                st.metric("Confidence", f"{selected_entry['confidence']:.0%}")
                safety_color_map = {"Safe": "#10b981", "Warning": "#f59e0b", "Critical": "#ef4444"}
                st.markdown(
                    f"<span style='color:{safety_color_map[selected_entry['safety_status']]}"
                    f";font-size:1.2rem;font-weight:bold;'>"
                    f"{selected_entry['safety_status']}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"**Human Intervention:** {'Yes' if selected_entry['human_intervention'] else 'No'}"
                )
                st.markdown("**Data Sources:**")
                for ds in selected_entry["data_sources"]:
                    st.markdown(f"- {ds}")

    # Export buttons for filtered data
    st.divider()
    ex1, ex2, _ = st.columns([1, 1, 3])
    with ex1:
        st.download_button(
            "📥 Export Filtered (JSON)",
            json.dumps(filtered, indent=2, default=str),
            file_name="audit_trail_filtered.json",
            mime="application/json",
        )
    with ex2:
        csv_rows = []
        for e in filtered:
            csv_rows.append({
                "ID": e["id"],
                "Timestamp": e["timestamp"],
                "Task": e["task"],
                "Domain": e["domain"],
                "Agents": "; ".join(e["agents"]),
                "Decision": e["decision"],
                "Confidence": e["confidence"],
                "Safety": e["safety_status"],
                "Human Intervention": e["human_intervention"],
            })
        buf = io.StringIO()
        if csv_rows:
            w = csv.DictWriter(buf, fieldnames=csv_rows[0].keys())
            w.writeheader()
            w.writerows(csv_rows)
        st.download_button(
            "📥 Export Filtered (CSV)",
            buf.getvalue(),
            file_name="audit_trail_filtered.csv",
            mime="text/csv",
        )

# ===================================================================
# TAB 3 -- Decision Provenance
# ===================================================================
with tab3:
    st.subheader("Decision Provenance Explorer")
    st.markdown("Trace the complete chain of reasoning for any system decision.")

    prov_id = st.selectbox(
        "Select Decision",
        [f"{e['id']} -- {e['task']}" for e in entries],
        key="provenance_select",
    )
    prov_entry = entries[
        [f"{e['id']} -- {e['task']}" for e in entries].index(prov_id)
    ]

    p1, p2 = st.columns([3, 2])

    with p1:
        st.markdown("### Reasoning Flow")

        # Build a visual Sankey-style flow showing agent contributions
        agents_involved = prov_entry["agents"]
        steps = prov_entry["reasoning"]

        # Visual flow diagram using plotly Sankey
        labels = ["Task Input"] + agents_involved + ["Collective Decision"]
        source_indices = []
        target_indices = []
        values = []
        link_labels = []

        # Task Input -> each agent
        for i, agent in enumerate(agents_involved):
            source_indices.append(0)
            target_indices.append(i + 1)
            values.append(1)
            link_labels.append(f"Assigned to {agent}")

        # Each agent -> Collective Decision
        decision_idx = len(agents_involved) + 1
        for i, agent in enumerate(agents_involved):
            source_indices.append(i + 1)
            target_indices.append(decision_idx)
            values.append(1)
            link_labels.append(f"{agent} contribution")

        node_colors = (
            ["#667eea"]
            + ["#764ba2"] * len(agents_involved)
            + ["#10b981"]
        )

        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=node_colors,
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=values,
                label=link_labels,
                color="rgba(102, 126, 234, 0.3)",
            ),
        )])
        fig_sankey.update_layout(
            title_text="Agent Contribution Flow",
            font_size=12,
            height=350,
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig_sankey, use_container_width=True)

        # Step-by-step reasoning
        st.markdown("### Step-by-Step Reasoning")
        for step_idx, step in enumerate(steps, 1):
            st.markdown(
                f'<div class="provenance-step">'
                f"<strong>Step {step_idx}:</strong> {step}</div>",
                unsafe_allow_html=True,
            )

    with p2:
        st.markdown("### Decision Metadata")

        st.metric("Decision ID", prov_entry["id"])
        st.metric("Confidence", f"{prov_entry['confidence']:.0%}")
        st.metric("Agents Involved", len(prov_entry["agents"]))

        st.divider()

        st.markdown("### Data Lineage")
        st.markdown("Sources consulted during this decision:")
        for ds in prov_entry["data_sources"]:
            st.markdown(f"- {ds}")

        st.divider()

        st.markdown("### Agent Contribution Weights")
        weight_labels = prov_entry["agents"]
        random.seed(hash(prov_entry["id"]))
        raw_weights = [random.uniform(0.5, 1.0) for _ in weight_labels]
        total_w = sum(raw_weights)
        norm_weights = [w / total_w for w in raw_weights]

        fig_bar = go.Figure(data=[go.Bar(
            x=weight_labels,
            y=[w * 100 for w in norm_weights],
            marker_color=["#667eea", "#764ba2", "#10b981", "#f59e0b"][:len(weight_labels)],
        )])
        fig_bar.update_layout(
            yaxis_title="Contribution (%)",
            height=250,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()

        st.markdown("### Constitutional Alignment")
        alignment_items = [
            ("Transparency", random.randint(90, 100)),
            ("Safety First", random.randint(85, 100)),
            ("Human Oversight", random.randint(88, 100)),
            ("Fairness", random.randint(82, 100)),
        ]
        for principle, score in alignment_items:
            st.progress(score / 100, text=f"{principle}: {score}%")

# ===================================================================
# TAB 4 -- Regulatory Reports
# ===================================================================
with tab4:
    st.subheader("Regulatory Report Generator")
    st.markdown("Generate pre-built compliance reports for regulatory submissions.")

    rpt_fw = st.selectbox(
        "Report Framework",
        list(COMPLIANCE_FRAMEWORKS.keys()),
        key="report_framework",
    )
    rpt_data = COMPLIANCE_FRAMEWORKS[rpt_fw]

    report_period = st.selectbox(
        "Reporting Period",
        ["Last 7 Days", "Last 30 Days", "Last Quarter", "Custom"],
        key="report_period",
    )

    st.divider()

    st.markdown(f"### {rpt_fw} Compliance Report Preview")
    st.markdown(f"*{rpt_data['full_name']}*")

    # Section 1 -- System overview
    st.markdown(
        '<div class="report-section">'
        "<h4>1. System Overview</h4>"
        "<p><strong>System:</strong> CoHumAIn Multi-Agent Framework v2.1</p>"
        "<p><strong>Purpose:</strong> Explainable multi-agent AI system with constitutional "
        "principles and hierarchical transparency for regulated industries.</p>"
        "<p><strong>Deployment:</strong> Production environment, on-premise with cloud monitoring.</p>"
        "<p><strong>Classification:</strong> High-risk AI system (under EU AI Act Art. 6)</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Section 2 -- Agent inventory
    agent_inventory = [
        {"Agent": "Code Generator", "Role": "Code Generation", "Risk Level": "Medium", "Status": "Active"},
        {"Agent": "Security Analyst", "Role": "Security Analysis", "Risk Level": "High", "Status": "Active"},
        {"Agent": "Code Reviewer", "Role": "Code Review", "Risk Level": "Medium", "Status": "Active"},
        {"Agent": "Test Generator", "Role": "Test Generation", "Risk Level": "Low", "Status": "Active"},
        {"Agent": "Risk Manager", "Role": "Risk Assessment", "Risk Level": "High", "Status": "Active"},
        {"Agent": "Compliance Officer", "Role": "Compliance Checking", "Risk Level": "Critical", "Status": "Active"},
    ]
    st.markdown(
        '<div class="report-section"><h4>2. Agent Inventory</h4></div>',
        unsafe_allow_html=True,
    )
    st.dataframe(pd.DataFrame(agent_inventory), use_container_width=True, hide_index=True)

    # Section 3 -- Decision summary
    st.markdown(
        '<div class="report-section"><h4>3. Decision Summary</h4></div>',
        unsafe_allow_html=True,
    )
    ds1, ds2, ds3, ds4 = st.columns(4)
    ds1.metric("Total Decisions", total_decisions)
    ds2.metric("Average Confidence", f"{avg_confidence:.0%}")
    ds3.metric("Safe Outcomes", f"{safe_count / total_decisions:.0%}")
    ds4.metric("Human Interventions", intervention_count)

    # Decision breakdown chart
    fig_dec = go.Figure(data=[go.Pie(
        labels=["Safe", "Warning", "Critical"],
        values=[safe_count, warning_count, critical_count],
        marker=dict(colors=["#10b981", "#f59e0b", "#ef4444"]),
        hole=0.4,
    )])
    fig_dec.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_dec, use_container_width=True)

    # Section 4 -- Safety incidents
    st.markdown(
        '<div class="report-section"><h4>4. Safety Incidents</h4></div>',
        unsafe_allow_html=True,
    )
    incidents = [e for e in entries if e["safety_status"] in ("Warning", "Critical")]
    if incidents:
        inc_rows = []
        for e in incidents:
            inc_rows.append({
                "ID": e["id"],
                "Timestamp": e["timestamp"],
                "Task": e["task"],
                "Severity": e["safety_status"],
                "Decision": e["decision"],
                "Resolved": "Yes",
            })
        st.dataframe(pd.DataFrame(inc_rows), use_container_width=True, hide_index=True)
    else:
        st.success("No safety incidents recorded in the reporting period.")

    # Section 5 -- Intervention log
    st.markdown(
        '<div class="report-section"><h4>5. Human Intervention Log</h4></div>',
        unsafe_allow_html=True,
    )
    interventions = [e for e in entries if e["human_intervention"]]
    if interventions:
        int_rows = []
        for e in interventions:
            int_rows.append({
                "ID": e["id"],
                "Timestamp": e["timestamp"],
                "Task": e["task"],
                "Agents": ", ".join(e["agents"]),
                "Reason": "Confidence below threshold" if e["confidence"] < 0.85 else "Policy escalation",
                "Outcome": e["decision"],
            })
        st.dataframe(pd.DataFrame(int_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No human interventions recorded in the reporting period.")

    # Section 6 -- Compliance category scores
    st.markdown(
        '<div class="report-section"><h4>6. Compliance Attestation</h4></div>',
        unsafe_allow_html=True,
    )

    cat_data = []
    for cat, info in rpt_data["categories"].items():
        status_label = {"safe": "Compliant", "warning": "Needs Attention", "critical": "Non-Compliant"}[info["status"]]
        cat_data.append({
            "Category": cat,
            "Score": f"{info['score']}%",
            "Status": status_label,
        })
    st.dataframe(pd.DataFrame(cat_data), use_container_width=True, hide_index=True)

    st.markdown(
        f"<p style='margin-top:1rem;'><strong>Overall {rpt_fw} Compliance Score: "
        f"{rpt_data['overall']}%</strong></p>",
        unsafe_allow_html=True,
    )

    non_compliant = [c for c, i in rpt_data["categories"].items() if i["status"] in ("warning", "critical")]
    if non_compliant:
        st.warning(
            f"Action required in {len(non_compliant)} categories: {', '.join(non_compliant)}"
        )
    else:
        st.success("All categories meet compliance thresholds.")

    st.divider()

    # Build downloadable report (JSON)
    report_payload = {
        "report_title": f"{rpt_fw} Compliance Report",
        "framework": rpt_fw,
        "full_name": rpt_data["full_name"],
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reporting_period": report_period,
        "system": "CoHumAIn Multi-Agent Framework v2.1",
        "overall_score": rpt_data["overall"],
        "categories": {
            cat: {"score": info["score"], "status": info["status"]}
            for cat, info in rpt_data["categories"].items()
        },
        "decision_summary": {
            "total": total_decisions,
            "avg_confidence": round(avg_confidence, 2),
            "safe": safe_count,
            "warning": warning_count,
            "critical": critical_count,
            "human_interventions": intervention_count,
        },
        "agent_inventory": agent_inventory,
        "safety_incidents": [
            {"id": e["id"], "task": e["task"], "severity": e["safety_status"]}
            for e in incidents
        ],
        "attestation": (
            f"This report certifies that the CoHumAIn system has been evaluated "
            f"against {rpt_fw} ({rpt_data['full_name']}) requirements. "
            f"Overall compliance score: {rpt_data['overall']}%. "
            f"Generated automatically on {datetime.now().strftime('%Y-%m-%d')}."
        ),
    }

    st.download_button(
        "📥 Download Full Report (JSON)",
        json.dumps(report_payload, indent=2),
        file_name=f"cohumain_{rpt_fw.lower().replace(' ', '_')}_report.json",
        mime="application/json",
        use_container_width=True,
    )

# ===================================================================
# TAB 5 -- Stakeholder Views
# ===================================================================
with tab5:
    st.subheader("Stakeholder Views")
    st.markdown(
        "Toggle between perspectives to see compliance and audit data at different "
        "levels of detail."
    )

    view_choice = st.radio(
        "Select Perspective",
        ["Developer", "Auditor", "Regulator", "End User"],
        horizontal=True,
        index=["Developer", "Auditor", "Regulator", "End User"].index(VIEW),
        key="tab5_view",
    )

    st.divider()

    # Pick a representative entry for the deep-dive
    demo_entry = entries[0]
    fw_key_sv = st.session_state.selected_framework
    fw_sv = COMPLIANCE_FRAMEWORKS[fw_key_sv]

    # ----- DEVELOPER VIEW -----
    if view_choice == "Developer":
        st.markdown("### Developer View -- Technical Details")
        st.markdown(
            "Full technical trace including agent internals, confidence calibration, "
            "constitutional checks, and raw data lineage."
        )

        sv1, sv2 = st.columns([2, 1])
        with sv1:
            st.markdown("#### Representative Decision Trace")
            st.markdown(f"**ID:** `{demo_entry['id']}`")
            st.markdown(f"**Task:** {demo_entry['task']}")
            st.markdown(f"**Agents:** `{demo_entry['agents']}`")
            st.markdown(f"**Confidence:** `{demo_entry['confidence']}`")
            st.markdown(f"**Safety Status:** `{demo_entry['safety_status']}`")

            st.markdown("**Full Reasoning (raw):**")
            for i, r in enumerate(demo_entry["reasoning"]):
                st.code(f"[Step {i+1}] {r}", language="text")

            st.markdown("**Data Sources:**")
            for ds in demo_entry["data_sources"]:
                st.code(ds, language="text")

            st.markdown("**Raw Entry JSON:**")
            st.json(demo_entry)

        with sv2:
            st.markdown("#### Compliance API Response")
            st.json({
                "framework": fw_key_sv,
                "overall_score": fw_sv["overall"],
                "categories": fw_sv["categories"],
                "timestamp": datetime.now().isoformat(),
                "api_version": "v2.1",
            })

            st.markdown("#### System Configuration")
            st.json({
                "confidence_threshold": 0.80,
                "delegation_strategy": "weighted_voting",
                "constitutional_check": True,
                "max_retries": 3,
                "timeout_seconds": 60,
                "audit_logging": "verbose",
            })

    # ----- AUDITOR VIEW -----
    elif view_choice == "Auditor":
        st.markdown("### Auditor View -- Compliance Focus")
        st.markdown(
            "Structured compliance evidence, category scores, and audit trail summaries "
            "aligned with regulatory requirements."
        )

        sv1, sv2 = st.columns(2)
        with sv1:
            st.markdown(f"#### {fw_key_sv} Compliance Summary")

            for cat, info in fw_sv["categories"].items():
                icon = {"safe": "🟢", "warning": "🟡", "critical": "🔴"}[info["status"]]
                label = {"safe": "Compliant", "warning": "Needs Attention", "critical": "Non-Compliant"}[info["status"]]
                st.markdown(f"{icon} **{cat}** -- {info['score']}% ({label})")

            st.divider()

            st.markdown("#### Audit Trail Summary")
            st.metric("Decisions Audited", total_decisions)
            st.metric("Decisions with Human Review", intervention_count)
            st.metric("Safety Incidents", warning_count + critical_count)

        with sv2:
            st.markdown("#### Evidence of Compliance")

            st.markdown("**Transparency:**")
            st.markdown(
                "- Three-level hierarchical explanations available for every decision\n"
                "- Full reasoning chain recorded in audit trail\n"
                "- Agent contribution weights documented"
            )
            st.markdown("**Human Oversight:**")
            st.markdown(
                "- Window of Transparency enables real-time interrupts\n"
                f"- {intervention_count} human interventions in reporting period\n"
                "- Configurable confidence thresholds for escalation"
            )
            st.markdown("**Safety Mechanisms:**")
            st.markdown(
                "- Constitutional principles enforced per agent\n"
                f"- {safe_count}/{total_decisions} decisions classified as Safe\n"
                "- Automated safety checks at every decision point"
            )
            st.markdown("**Record Keeping:**")
            st.markdown(
                "- Immutable audit trail with decision provenance\n"
                "- Data lineage tracking for all inputs\n"
                "- Export available in JSON and CSV formats"
            )

    # ----- REGULATOR VIEW -----
    elif view_choice == "Regulator":
        st.markdown("### Regulator View -- Risk & Safety Focus")
        st.markdown(
            "High-level risk indicators, safety incident summary, and compliance posture "
            "for regulatory review."
        )

        sv1, sv2 = st.columns(2)
        with sv1:
            st.markdown("#### Risk Dashboard")
            risk_metrics = {
                "System Risk Classification": "High-Risk (EU AI Act Art. 6)",
                "Overall Compliance": f"{fw_sv['overall']}%",
                "Open Non-Conformities": len([
                    c for c, i in fw_sv["categories"].items()
                    if i["status"] in ("warning", "critical")
                ]),
                "Critical Safety Events": critical_count,
                "Human Override Capability": "Enabled",
            }
            for k, v in risk_metrics.items():
                st.markdown(f"**{k}:** {v}")

            st.divider()

            st.markdown("#### Safety Incident Summary")

            fig_safety = go.Figure(data=[go.Bar(
                x=["Safe", "Warning", "Critical"],
                y=[safe_count, warning_count, critical_count],
                marker_color=["#10b981", "#f59e0b", "#ef4444"],
            )])
            fig_safety.update_layout(
                yaxis_title="Count",
                height=250,
                margin=dict(l=0, r=0, t=10, b=0),
            )
            st.plotly_chart(fig_safety, use_container_width=True)

        with sv2:
            st.markdown("#### Non-Compliant Categories")

            flagged = [
                (cat, info)
                for cat, info in fw_sv["categories"].items()
                if info["status"] in ("warning", "critical")
            ]
            if flagged:
                for cat, info in flagged:
                    severity = "WARNING" if info["status"] == "warning" else "CRITICAL"
                    css = "compliance-warning" if info["status"] == "warning" else "compliance-critical"
                    st.markdown(
                        f'<div class="{css}"><strong>[{severity}] {cat}</strong><br/>'
                        f"Score: {info['score']}% -- Below required threshold.<br/>"
                        f"Remediation plan required.</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.success("All categories meet compliance thresholds.")

            st.divider()

            st.markdown("#### Human Oversight Assurance")
            st.markdown(
                "- Human-in-the-loop capability verified and active\n"
                "- Window of Transparency provides real-time interrupt mechanism\n"
                f"- {intervention_count} human interventions recorded\n"
                "- Escalation policies configured for low-confidence decisions\n"
                "- All agent decisions are explainable via 3-level hierarchy"
            )

    # ----- END USER VIEW -----
    elif view_choice == "End User":
        st.markdown("### End User View -- Simplified Overview")
        st.markdown(
            "A plain-language summary of how the AI system makes decisions and how "
            "your interests are protected."
        )

        st.markdown("#### How Does This System Work?")
        st.info(
            "The CoHumAIn system uses multiple specialised AI agents that work together "
            "to make decisions. Each agent has a specific role, and they check each "
            "other's work to ensure quality and safety. A human can step in at any time "
            "to review or override a decision."
        )

        st.markdown("#### Is This System Safe?")
        overall_pct = fw_sv["overall"]
        if overall_pct >= 90:
            st.success(
                f"The system currently meets {overall_pct}% of the {fw_key_sv} "
                f"safety and compliance requirements. This is considered a strong "
                f"compliance posture."
            )
        elif overall_pct >= 80:
            st.warning(
                f"The system meets {overall_pct}% of the {fw_key_sv} requirements. "
                f"Some areas need improvement, but the core safety features are active."
            )
        else:
            st.error(
                f"The system meets only {overall_pct}% of the {fw_key_sv} requirements. "
                f"Remediation is in progress."
            )

        st.markdown("#### Key Protections in Place")
        st.markdown(
            "- Every decision made by the AI is recorded and can be explained.\n"
            "- A human reviewer can pause or override the AI at any time.\n"
            "- The system follows strict rules (constitutional principles) to ensure "
            "fairness and safety.\n"
            "- Regular compliance checks are performed automatically.\n"
            "- Your data is handled according to applicable regulations."
        )

        st.markdown("#### Your Rights")
        if fw_key_sv == "GDPR":
            st.markdown(
                "- **Right to Explanation:** You can request an explanation of any "
                "automated decision that affects you.\n"
                "- **Right to Access:** You can request a copy of your data.\n"
                "- **Right to Rectification:** You can correct inaccurate data.\n"
                "- **Right to Erasure:** You can request deletion of your data."
            )
        elif fw_key_sv == "HIPAA":
            st.markdown(
                "- Your health information is protected by federal law.\n"
                "- You have the right to access your health records.\n"
                "- You will be notified if there is a data breach."
            )
        else:
            st.markdown(
                "- You have the right to understand how AI decisions affect you.\n"
                "- You can request a human review of any automated decision.\n"
                "- Your data is processed according to applicable regulations."
            )

        st.markdown("#### Recent System Performance")
        eu_cols = st.columns(3)
        eu_cols[0].metric("Decisions Made", total_decisions)
        eu_cols[1].metric("Safety Rating", f"{safe_count/total_decisions:.0%}")
        eu_cols[2].metric("Human Reviews", intervention_count)
