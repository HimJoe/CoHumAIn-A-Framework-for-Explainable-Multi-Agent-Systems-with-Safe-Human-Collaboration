"""
CoHumAIn Framework - Explanation Explorer
Three-level hierarchical explanations with interactive timeline
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

st.set_page_config(page_title="Explanation Explorer", page_icon="📊", layout="wide")

st.title("📊 Explanation Explorer")
st.markdown("Navigate through three levels of explainability: Individual → Coordination → Collective")

# Sample explanation data
sample_task = {
    "task_id": "AUTH_2024_001",
    "task": "Implement user authentication with bcrypt",
    "timestamp": "2024-02-07T15:30:00",
    "collective_confidence": 0.94,
    "status": "completed",
    "automation_level": "human_on_the_loop"
}

tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Level 1: Individual",
    "🤝 Level 2: Coordination",
    "🌐 Level 3: Collective",
    "📈 Timeline View"
])

with tab1:
    st.subheader("Level 1: Individual Agent Explanations")
    st.markdown("*Why did each agent make their specific decisions?*")
    
    # Agent selector
    agents = ["Code Generator", "Security Analyst", "Code Reviewer", "Test Generator"]
    selected_agent = st.selectbox("Select Agent to Inspect", agents)
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if selected_agent == "Code Generator":
            st.markdown("### Code Generator - Decision Trace")
            
            with st.expander("**Initial Implementation (Step 1)**", expanded=True):
                st.markdown("""
                **Task:** Generate bcrypt password hashing implementation
                
                **Thought Process:**
                ```
                THOUGHT: Need secure password hashing for authentication
                → Research: bcrypt is industry standard
                → Decision: Use bcrypt with salt rounds
                → Initial value: rounds=10 (common default)
                ```
                
                **Action Taken:**
                ```python
                def register_user(username, password):
                    salt = bcrypt.gensalt(rounds=10)
                    hashed = bcrypt.hashpw(password.encode(), salt)
                    return save_user(username, hashed)
                ```
                
                **Observation:**
                Code generated successfully. Basic functionality working.
                
                **Confidence:** 85%  
                *Rationale:* Standard implementation, but not verified against latest security standards
                
                **Constitutional Check:**
                ✅ Follow secure coding practices  
                ⚠️ Questionable: May not meet OWASP 2024 recommendations
                """)
                
                st.info("💡 **Why this confidence level?** Agent is confident in basic implementation but recognizes need for security validation.")
            
            with st.expander("**Revision (Step 4)**"):
                st.markdown("""
                **Task:** Update bcrypt rounds based on Security Analyst feedback
                
                **Thought Process:**
                ```
                THOUGHT: Security Analyst flagged rounds=10 as insufficient
                → Research: OWASP recommends minimum 12 rounds as of 2024
                → Decision: Update to rounds=12
                → Validation: Meets security requirements
                ```
                
                **Action Taken:**
                ```python
                def register_user(username, password):
                    salt = bcrypt.gensalt(rounds=12)  # ← Updated
                    hashed = bcrypt.hashpw(password.encode(), salt)
                    return save_user(username, hashed)
                ```
                
                **Observation:**
                Security concern addressed. OWASP compliant.
                
                **Confidence:** 95%  
                *Rationale:* Now aligns with current security standards
                
                **Constitutional Check:**
                ✅ Follow secure coding practices  
                ✅ Meets OWASP 2024 standards
                """)
        
        elif selected_agent == "Security Analyst":
            st.markdown("### Security Analyst - Detection Trace")
            
            with st.expander("**Vulnerability Scan (Step 2)**", expanded=True):
                st.markdown("""
                **Task:** Analyze generated code for security vulnerabilities
                
                **Analysis Process:**
                ```
                SCAN: Authentication implementation detected
                → Check 1: Password hashing algorithm ✅ bcrypt (secure)
                → Check 2: Salt generation ✅ Per-password unique salt
                → Check 3: Salt rounds ⚠️ rounds=10 detected
                → Lookup: OWASP 2024 recommends minimum 12 rounds
                → Verdict: MEDIUM severity issue found
                ```
                
                **Findings:**
                | Check | Status | Details |
                |-------|--------|---------|
                | Algorithm | ✅ Pass | bcrypt approved |
                | Salt | ✅ Pass | Unique per password |
                | Rounds | ⚠️ Fail | 10 < 12 (OWASP min) |
                | Storage | ✅ Pass | Secure database |
                
                **Recommendation:**
                Increase bcrypt rounds from 10 to 12 (OWASP 2024 minimum)
                
                **Confidence:** 97%  
                *Rationale:* Clear policy violation with documented standard
                
                **Constitutional Principles:**
                ✅ Zero tolerance for known vulnerabilities  
                ⚠️ OWASP violation detected → Must fix
                """)
                
                st.error("🚨 **Security Issue Detected:** bcrypt rounds below OWASP 2024 recommendation")
                st.success("✅ **Delegation Triggered:** Assigned back to Code Generator for fix")
    
    with col2:
        st.markdown("### Agent Metadata")
        
        agent_info = {
            "Code Generator": {
                "Expertise": 0.85,
                "Confidence Threshold": 0.80,
                "Tasks Completed": 87,
                "Avg Confidence": 0.87,
                "Capabilities": ["Code Generation", "Refactoring"]
            },
            "Security Analyst": {
                "Expertise": 0.95,
                "Confidence Threshold": 0.90,
                "Tasks Completed": 65,
                "Avg Confidence": 0.96,
                "Capabilities": ["Security Analysis", "OWASP Compliance"]
            },
            "Code Reviewer": {
                "Expertise": 0.89,
                "Confidence Threshold": 0.85,
                "Tasks Completed": 91,
                "Avg Confidence": 0.92,
                "Capabilities": ["Code Review", "Best Practices"]
            },
            "Test Generator": {
                "Expertise": 0.88,
                "Confidence Threshold": 0.85,
                "Tasks Completed": 72,
                "Avg Confidence": 0.90,
                "Capabilities": ["Test Generation", "Coverage Analysis"]
            }
        }
        
        info = agent_info[selected_agent]
        
        for key, value in info.items():
            if isinstance(value, float):
                st.metric(key, f"{value:.2f}")
            elif isinstance(value, list):
                st.markdown(f"**{key}:**")
                for item in value:
                    st.markdown(f"- {item}")
            else:
                st.metric(key, value)
        
        st.divider()
        
        st.markdown("### 📊 Performance Trend")
        
        # Confidence trend
        trend_data = [0.83, 0.85, 0.86, 0.87, 0.88, 0.87, 0.85, 0.86, 0.87, 0.87]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=trend_data,
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            fill='tozeroy'
        ))
        fig.update_layout(
            yaxis_title="Avg Confidence",
            xaxis_title="Last 10 Tasks",
            height=200,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Level 2: Coordination Explanations")
    st.markdown("*How did agents collaborate and resolve conflicts?*")
    
    st.markdown("### Coordination Timeline")
    
    coordination_events = [
        {
            "time": "15:30:05",
            "type": "delegation",
            "from": "Orchestrator",
            "to": "Code Generator",
            "decision": "Initial task assignment",
            "rationale": "Code Generator has highest expertise for code generation tasks"
        },
        {
            "time": "15:30:12",
            "type": "delegation",
            "from": "Code Generator",
            "to": "Security Analyst",
            "decision": "Request security review",
            "rationale": "Authentication code requires security validation per constitutional principles"
        },
        {
            "time": "15:30:18",
            "type": "issue_detected",
            "from": "Security Analyst",
            "to": "System",
            "decision": "OWASP violation found",
            "rationale": "bcrypt rounds=10 below minimum 12 (MEDIUM severity)"
        },
        {
            "time": "15:30:19",
            "type": "delegation",
            "from": "System",
            "to": "Code Generator",
            "decision": "Delegate revision",
            "rationale": "Code Generator owns implementation. Security Analyst lacks modification capability. Constitutional priority: Security recommendations must be addressed."
        },
        {
            "time": "15:30:25",
            "type": "validation",
            "from": "Code Generator",
            "to": "Code Reviewer",
            "decision": "Request final review",
            "rationale": "Revision complete, requires peer validation"
        },
        {
            "time": "15:30:30",
            "type": "consensus",
            "from": "System",
            "to": "All Agents",
            "decision": "Collective approval achieved",
            "rationale": "All agents agree on revised implementation (consensus: 100%)"
        }
    ]
    
    for event in coordination_events:
        event_type_emoji = {
            "delegation": "📤",
            "issue_detected": "🚨",
            "validation": "✅",
            "consensus": "🤝"
        }.get(event['type'], "📌")
        
        event_color = {
            "delegation": "#3b82f6",
            "issue_detected": "#ef4444",
            "validation": "#10b981",
            "consensus": "#8b5cf6"
        }.get(event['type'], "#6b7280")
        
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"**{event['time']}**")
                st.markdown(f"{event_type_emoji} {event['type'].replace('_', ' ').title()}")
            
            with col2:
                st.markdown(f"**{event['decision']}**")
                st.markdown(f"*From:* {event['from']} → *To:* {event['to']}")
                st.info(f"💡 **Rationale:** {event['rationale']}")
            
            st.markdown(f"<div style='height: 2px; background-color: {event_color}; margin: 15px 0;'></div>", unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Coordination Metrics")
        
        st.metric("Total Delegation Events", "4")
        st.metric("Conflict Resolutions", "0")
        st.metric("Information Exchanges", "6")
        st.metric("Consensus Achieved", "Yes (100%)")
    
    with col2:
        st.markdown("### 🎯 Decision Quality")
        
        quality_metrics = {
            "Appropriate Delegation": 100,
            "Coordination Efficiency": 94,
            "Conflict Resolution": 100,
            "Transparency": 98
        }
        
        for metric, value in quality_metrics.items():
            st.progress(value/100, text=f"{metric}: {value}%")

with tab3:
    st.subheader("Level 3: Collective Explanation")
    st.markdown("*How did the team produce this outcome together?*")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 🌐 Collective Summary")
        
        st.success(f"""
        **Task:** {sample_task['task']}  
        **Status:** ✅ {sample_task['status'].title()}  
        **Collective Confidence:** {sample_task['collective_confidence']:.0%}  
        **Automation Level:** {sample_task['automation_level'].replace('_', ' ').title()}
        """)
        
        st.markdown("""
        ### How the Team Worked Together
        
        The agent team successfully implemented secure user authentication through coordinated effort:
        
        1. **Code Generator** produced initial implementation using bcrypt with 10 salt rounds
        2. **Security Analyst** identified OWASP compliance gap (minimum 12 rounds required)
        3. **System coordination** delegated revision back to Code Generator with clear rationale
        4. **Code Generator** updated implementation to meet security standards (rounds=12)
        5. **Code Reviewer** validated revised implementation for best practices
        6. **Test Generator** created comprehensive test coverage
        
        ### Key Coordination Decisions
        
        **Why Security Analyst was consulted:**  
        Authentication code requires security validation per Code Generator's constitutional principles
        
        **Why revision was delegated back to Generator:**  
        - Security Analyst detected issue but lacks code modification capability
        - Code Generator owns the implementation
        - Constitutional priority: Security recommendations must be addressed
        
        **Why no human intervention was required:**  
        - High collective confidence (94%)
        - Clear delegation logic
        - All agents reached consensus
        - No constitutional conflicts
        
        ### Emergent Behaviors Detected
        
        1. **Self-correction loop:** Team detected and fixed issue without human intervention
        2. **Expertise-based delegation:** Each agent operated within their specialty
        3. **Constitutional alignment:** All decisions aligned with stated principles
        """)
    
    with col2:
        st.markdown("### 📊 Attribution Analysis")
        
        # Agent contributions
        contributions = {
            "Code Generator": 40,
            "Security Analyst": 30,
            "Code Reviewer": 20,
            "Test Generator": 10
        }
        
        fig = go.Figure(data=[
            go.Pie(
                labels=list(contributions.keys()),
                values=list(contributions.values()),
                hole=0.4,
                marker=dict(colors=['#667eea', '#ef4444', '#10b981', '#f59e0b'])
            )
        ])
        fig.update_layout(
            title="Agent Contributions",
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🎯 Critical Contributions")
        
        st.markdown("""
        **🥇 Security Analyst (+50% value)**  
        Critical vulnerability detection prevented deployment of sub-standard security
        
        **🥈 Code Generator (+40% value)**  
        Primary author + responsive to feedback
        
        **🥉 Code Reviewer (+10% value)**  
        Logic validation ensured maintainability
        """)
        
        st.divider()
        
        st.markdown("### 🔄 Counterfactual Analysis")
        
        with st.expander("What if Security Analyst wasn't consulted?"):
            st.warning("⚠️ **High Risk**: OWASP violation would have gone undetected. Vulnerable code would be deployed.")
        
        with st.expander("What if delegation threshold was lower?"):
            st.info("🔄 **More Transfers**: More delegation events would occur, potentially slowing workflow but increasing quality checks.")

with tab4:
    st.subheader("Timeline View")
    st.markdown("*Complete temporal sequence of decisions*")
    
    # Interactive timeline
    timeline_data = [
        {"time": 0, "agent": "Code Generator", "event": "Start implementation", "confidence": 0.85},
        {"time": 5, "agent": "Security Analyst", "event": "Begin security scan", "confidence": 0.95},
        {"time": 8, "agent": "Security Analyst", "event": "Vulnerability detected", "confidence": 0.97},
        {"time": 9, "agent": "System", "event": "Delegate revision", "confidence": None},
        {"time": 12, "agent": "Code Generator", "event": "Apply fix", "confidence": 0.95},
        {"time": 15, "agent": "Code Reviewer", "event": "Validate changes", "confidence": 0.92},
        {"time": 18, "agent": "Test Generator", "event": "Generate tests", "confidence": 0.90},
        {"time": 20, "agent": "System", "event": "Collective approval", "confidence": 0.94}
    ]
    
    fig = go.Figure()
    
    for i, event in enumerate(timeline_data):
        color = {
            "Code Generator": "#667eea",
            "Security Analyst": "#ef4444",
            "Code Reviewer": "#10b981",
            "Test Generator": "#f59e0b",
            "System": "#8b5cf6"
        }.get(event['agent'], "#6b7280")
        
        fig.add_trace(go.Scatter(
            x=[event['time']],
            y=[i],
            mode='markers+text',
            marker=dict(size=20, color=color),
            text=[event['agent'][:4]],
            textposition="top center",
            hovertext=f"{event['agent']}: {event['event']}<br>Confidence: {event['confidence']:.0%}" if event['confidence'] else f"{event['agent']}: {event['event']}",
            showlegend=False
        ))
    
    fig.update_layout(
        xaxis_title="Time (seconds)",
        yaxis_title="Event Sequence",
        height=500,
        yaxis=dict(showticklabels=False)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed event list
    st.markdown("### Detailed Event Log")
    
    for event in timeline_data:
        with st.expander(f"T+{event['time']}s: {event['agent']} - {event['event']}"):
            st.markdown(f"**Agent:** {event['agent']}")
            st.markdown(f"**Event:** {event['event']}")
            if event['confidence']:
                st.progress(event['confidence'], text=f"Confidence: {event['confidence']:.0%}")
            
            # Add mock detailed info
            st.json({
                "timestamp": f"15:30:{event['time']:02d}",
                "agent": event['agent'],
                "event_type": event['event'],
                "confidence": event.get('confidence'),
                "inputs": ["Previous step output"],
                "outputs": ["Next step input"]
            })

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Explanation Controls")
    
    explanation_format = st.selectbox(
        "Format",
        ["Interactive", "PDF Report", "JSON Export", "Timeline Video"]
    )
    
    detail_level = st.select_slider(
        "Detail Level",
        ["Summary", "Standard", "Detailed", "Comprehensive"]
    )
    
    st.divider()
    
    if st.button("📥 Export Explanation", use_container_width=True):
        explanation_export = {
            "task": sample_task,
            "level1": "Individual agent explanations...",
            "level2": "Coordination decisions...",
            "level3": "Collective summary..."
        }
        st.download_button(
            "Download JSON",
            json.dumps(explanation_export, indent=2),
            file_name="cohumain_explanation.json",
            mime="application/json"
        )
    
    st.divider()
    
    st.markdown("### 🎯 Quick Filters")
    
    show_level1 = st.checkbox("Level 1: Individual", value=True)
    show_level2 = st.checkbox("Level 2: Coordination", value=True)
    show_level3 = st.checkbox("Level 3: Collective", value=True)
    
    st.divider()
    
    st.markdown("### 💡 Tips")
    st.info("""
    **Understanding Explanations:**
    - Level 1: What each agent thought
    - Level 2: How agents worked together
    - Level 3: What the team accomplished
    
    Use timeline view to see the complete story!
    """)
