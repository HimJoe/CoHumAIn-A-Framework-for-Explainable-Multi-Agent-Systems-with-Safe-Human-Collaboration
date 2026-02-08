"""
CoHumAIn Framework - Multi-Agent Workflow Page
Visual coordination graph with real-time monitoring and interrupt capability
"""

import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime
import time

st.set_page_config(page_title="Multi-Agent Workflow", page_icon="🔄", layout="wide")

st.title("🔄 Multi-Agent Workflow Designer")
st.markdown("Design, monitor, and interrupt multi-agent workflows with real-time transparency")

# Initialize session state
if 'workflow_running' not in st.session_state:
    st.session_state.workflow_running = False
if 'workflow_paused' not in st.session_state:
    st.session_state.workflow_paused = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'workflow_history' not in st.session_state:
    st.session_state.workflow_history = []

tab1, tab2, tab3 = st.tabs(["🎨 Design Workflow", "▶️ Execute & Monitor", "📈 Analytics"])

with tab1:
    st.subheader("Workflow Design Canvas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Coordination Graph")
        
        # Create network graph
        G = nx.DiGraph()
        
        # Sample workflow nodes
        agents = ["Code Generator", "Security Analyst", "Code Reviewer", "Test Generator"]
        
        # Add nodes
        for agent in agents:
            G.add_node(agent)
        
        # Add edges (workflow flow)
        G.add_edge("Code Generator", "Security Analyst")
        G.add_edge("Security Analyst", "Code Reviewer")
        G.add_edge("Code Reviewer", "Test Generator")
        G.add_edge("Security Analyst", "Code Generator", label="Revision")
        
        # Get positions
        pos = nx.spring_layout(G, seed=42)
        
        # Create Plotly figure
        edge_trace = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            edge_trace.append(go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=2, color='#888'),
                hoverinfo='none',
                showlegend=False
            ))
        
        node_trace = go.Scatter(
            x=[pos[node][0] for node in G.nodes()],
            y=[pos[node][1] for node in G.nodes()],
            mode='markers+text',
            text=list(G.nodes()),
            textposition="top center",
            marker=dict(
                size=30,
                color='#667eea',
                line=dict(width=2, color='white')
            ),
            hoverinfo='text',
            showlegend=False
        )
        
        fig = go.Figure(data=edge_trace + [node_trace])
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Workflow Configuration")
        
        workflow_name = st.text_input("Workflow Name", value="Code Review Pipeline")
        
        st.markdown("**Delegation Rules**")
        delegation_threshold = st.slider(
            "Confidence Threshold for Delegation",
            0.0, 1.0, 0.80, 0.05
        )
        
        st.markdown("**Conflict Resolution**")
        conflict_strategy = st.selectbox(
            "Strategy",
            ["Weighted Voting", "Expert Arbitration", "Human Escalation"]
        )
        
        st.markdown("**Interrupt Settings**")
        interrupt_on_low_confidence = st.checkbox("Low Confidence", value=True)
        interrupt_on_disagreement = st.checkbox("Agent Disagreement", value=True)
        interrupt_on_safety = st.checkbox("Safety Violation", value=True)
        
        if st.button("💾 Save Workflow", type="primary", use_container_width=True):
            st.success("✅ Workflow saved successfully!")

with tab2:
    st.subheader("Real-Time Workflow Execution")
    
    # Control panel
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("▶️ Start Workflow", disabled=st.session_state.workflow_running):
            st.session_state.workflow_running = True
            st.session_state.current_step = 0
            st.rerun()
    
    with col2:
        if st.button("⏸️ Pause", disabled=not st.session_state.workflow_running):
            st.session_state.workflow_paused = True
            st.warning("Workflow paused at current step")
    
    with col3:
        if st.button("▶️ Resume", disabled=not st.session_state.workflow_paused):
            st.session_state.workflow_paused = False
            st.rerun()
    
    with col4:
        if st.button("⏹️ Stop", disabled=not st.session_state.workflow_running):
            st.session_state.workflow_running = False
            st.session_state.workflow_paused = False
            st.session_state.current_step = 0
            st.info("Workflow stopped")
    
    st.divider()
    
    # Execution timeline
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Execution Timeline")
        
        steps = [
            {"step": 1, "agent": "Code Generator", "action": "Generate authentication code", "status": "completed", "confidence": 0.85},
            {"step": 2, "agent": "Security Analyst", "action": "Scan for vulnerabilities", "status": "completed", "confidence": 0.95},
            {"step": 3, "agent": "Security Analyst", "action": "Flag bcrypt rounds=10", "status": "completed", "confidence": 0.97},
            {"step": 4, "agent": "Code Generator", "action": "Revise to rounds=12", "status": "in_progress", "confidence": 0.92},
            {"step": 5, "agent": "Code Reviewer", "action": "Final review", "status": "pending", "confidence": None},
            {"step": 6, "agent": "Test Generator", "action": "Generate tests", "status": "pending", "confidence": None}
        ]
        
        for step in steps:
            status_icon = {
                "completed": "✅",
                "in_progress": "⏳",
                "pending": "⏸️",
                "interrupted": "⚠️"
            }.get(step['status'], "❓")
            
            status_color = {
                "completed": "#10b981",
                "in_progress": "#3b82f6",
                "pending": "#6b7280",
                "interrupted": "#f59e0b"
            }.get(step['status'], "#000000")
            
            with st.container():
                step_col1, step_col2, step_col3 = st.columns([1, 3, 1])
                
                with step_col1:
                    st.markdown(f"**Step {step['step']}**")
                
                with step_col2:
                    st.markdown(f"{status_icon} **{step['agent']}**: {step['action']}")
                    if step['confidence'] is not None:
                        st.progress(step['confidence'], text=f"Confidence: {step['confidence']:.0%}")
                
                with step_col3:
                    if step['status'] in ['completed', 'in_progress']:
                        if st.button("🔍 Details", key=f"detail_{step['step']}"):
                            st.session_state.selected_step = step['step']
                
                st.markdown(f"<div style='height: 2px; background-color: {status_color}; margin: 10px 0;'></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Agent Status")
        
        agent_status = [
            {"agent": "Code Generator", "status": "Active", "load": 0.65},
            {"agent": "Security Analyst", "status": "Active", "load": 0.82},
            {"agent": "Code Reviewer", "status": "Idle", "load": 0.0},
            {"agent": "Test Generator", "status": "Idle", "load": 0.0}
        ]
        
        for status in agent_status:
            with st.container():
                st.markdown(f"**{status['agent']}**")
                status_color = "🟢" if status['status'] == "Active" else "⚪"
                st.markdown(f"{status_color} {status['status']}")
                if status['load'] > 0:
                    st.progress(status['load'], text=f"Load: {status['load']:.0%}")
                st.markdown("---")
    
    # 🚨 INTERRUPT CONTROL PANEL
    st.divider()
    st.markdown("### 🚨 Window of Transparency - Interrupt Control")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Interrupt Triggers")
        
        trigger_confidence = st.checkbox("Confidence < 0.80", value=True)
        trigger_safety = st.checkbox("Safety Violation", value=True)
        trigger_disagreement = st.checkbox("Agent Disagreement > 20%", value=True)
        
        if st.button("🛑 INTERRUPT NOW", type="secondary", use_container_width=True):
            st.session_state.workflow_paused = True
            st.error("⚠️ WORKFLOW INTERRUPTED - Human review required")
            st.info("👉 View detailed explanation in the right panel")
    
    with col2:
        st.markdown("#### Current Step Details")
        
        with st.expander("**Step 4: Code Generator Revision**", expanded=True):
            st.markdown("""
            **Agent:** Code Generator  
            **Task:** Revise bcrypt salt rounds  
            **Confidence:** 92%  
            
            **Reasoning:**
            ```
            Thought: Security Analyst flagged rounds=10 as below OWASP minimum
            Action: Update bcrypt.gensalt(rounds=12)
            Observation: Change addresses security concern
            Constitutional Check: ✅ Follows secure coding practices
            ```
            
            **Dependencies:**
            - Input from: Security Analyst (Step 3)
            - Output to: Code Reviewer (Step 5)
            """)
            
            if st.button("✅ Approve & Continue"):
                st.success("Step approved - resuming workflow")
            
            if st.button("❌ Reject & Modify"):
                st.warning("Step rejected - awaiting modification")
    
    with col3:
        st.markdown("#### Coordination Decisions")
        
        st.info("""
        **Delegation Decision**
        
        FROM: Security Analyst  
        TO: Code Generator  
        
        **Rationale:**  
        Security Analyst detected OWASP violation (bcrypt rounds below minimum). 
        
        Code Generator owns implementation and has capability to fix.
        
        **Conflict Resolution:** None required (unanimous agreement)
        """)

with tab3:
    st.subheader("Workflow Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Execution Metrics")
        
        metrics = {
            "Total Workflows": 127,
            "Success Rate": "94.5%",
            "Avg Execution Time": "4.2 min",
            "Interruptions": 12,
            "Human Interventions": 8
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.divider()
        
        st.markdown("#### Step Completion Rate")
        
        completion_data = {
            "Step 1": 100,
            "Step 2": 98,
            "Step 3": 95,
            "Step 4": 92,
            "Step 5": 94,
            "Step 6": 96
        }
        
        fig = go.Figure(data=[
            go.Bar(x=list(completion_data.keys()), y=list(completion_data.values()),
                   marker_color='#667eea')
        ])
        fig.update_layout(
            yaxis_title="Completion Rate (%)",
            height=300,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Interrupt Analysis")
        
        interrupt_reasons = {
            "Low Confidence": 5,
            "Safety Violation": 4,
            "Agent Disagreement": 2,
            "Timeout": 1
        }
        
        fig = go.Figure(data=[
            go.Pie(labels=list(interrupt_reasons.keys()), 
                   values=list(interrupt_reasons.values()),
                   hole=0.4)
        ])
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        st.markdown("#### Agent Coordination Efficiency")
        
        efficiency_data = {
            "Optimal Delegation": 85,
            "Unnecessary Transfers": 10,
            "Coordination Overhead": 5
        }
        
        fig = go.Figure(data=[
            go.Bar(x=list(efficiency_data.keys()), y=list(efficiency_data.values()),
                   marker_color=['#10b981', '#f59e0b', '#ef4444'])
        ])
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🔄 Workflow Controls")
    
    st.markdown(f"""
    **Status:** {'🟢 Running' if st.session_state.workflow_running else '⚪ Stopped'}  
    **Current Step:** {st.session_state.current_step}/6  
    **Paused:** {'Yes' if st.session_state.workflow_paused else 'No'}
    """)
    
    st.divider()
    
    st.markdown("### 💡 Quick Actions")
    
    if st.button("📋 Load Example Workflow"):
        st.info("Loading software engineering workflow...")
    
    if st.button("📥 Import Workflow JSON"):
        st.info("Upload workflow configuration...")
    
    if st.button("📤 Export Current Workflow"):
        st.success("Workflow exported to JSON")
    
    st.divider()
    
    st.markdown("### ⚙️ Advanced Settings")
    
    auto_resume = st.checkbox("Auto-resume after interrupt resolution", value=False)
    detailed_logs = st.checkbox("Enable detailed logging", value=True)
    notification_alerts = st.checkbox("Send notifications on interrupts", value=True)
