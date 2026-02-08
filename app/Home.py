"""
CoHumAIn Framework - Streamlit Home Page
Window of Transparency for Multi-Agent Systems
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Page configuration
st.set_page_config(
    page_title="CoHumAIn - Window of Transparency",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .status-safe {
        color: #10b981;
        font-weight: bold;
    }
    .status-warning {
        color: #f59e0b;
        font-weight: bold;
    }
    .status-danger {
        color: #ef4444;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'framework_initialized' not in st.session_state:
        st.session_state.framework_initialized = False
    if 'active_agents' not in st.session_state:
        st.session_state.active_agents = []
    if 'recent_tasks' not in st.session_state:
        st.session_state.recent_tasks = []
    if 'safety_status' not in st.session_state:
        st.session_state.safety_status = "Optimal"

def main():
    init_session_state()
    
    # Header
    st.markdown('<p class="main-header">🤖 CoHumAIn Framework</p>', unsafe_allow_html=True)
    st.markdown("### Window of Transparency for Multi-Agent Systems")
    
    st.markdown("""
    **Collective Human and Machine Intelligence** - Making multi-agent AI systems 
    transparent, safe, and trustworthy for regulated industries.
    """)
    
    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active Agents",
            value=len(st.session_state.active_agents),
            delta="2 since yesterday"
        )
    
    with col2:
        st.metric(
            label="Tasks Completed",
            value="127",
            delta="+15 today"
        )
    
    with col3:
        st.metric(
            label="Trust Score",
            value="94%",
            delta="+3%"
        )
    
    with col4:
        status_color = "status-safe" if st.session_state.safety_status == "Optimal" else "status-warning"
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.875rem; color: #6b7280;">Safety Status</div>
            <div class="{status_color}" style="font-size: 1.875rem;">{st.session_state.safety_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🔍 Recent Activity", 
        "🎯 Quick Start",
        "📚 Documentation"
    ])
    
    with tab1:
        show_overview()
    
    with tab2:
        show_recent_activity()
    
    with tab3:
        show_quick_start()
    
    with tab4:
        show_documentation()
    
    # Sidebar
    with st.sidebar:
        show_sidebar()

def show_overview():
    """Display system overview and metrics"""
    st.subheader("System Health & Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Trust calibration chart
        st.markdown("#### Trust Calibration Curve")
        
        confidence_bins = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        actual_accuracy = [0.48, 0.62, 0.71, 0.82, 0.91, 0.98]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=confidence_bins, y=confidence_bins,
            mode='lines', name='Perfect Calibration',
            line=dict(color='gray', dash='dash')
        ))
        fig.add_trace(go.Scatter(
            x=confidence_bins, y=actual_accuracy,
            mode='lines+markers', name='CoHumAIn System',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            xaxis_title="Predicted Confidence",
            yaxis_title="Actual Accuracy",
            height=300,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Explanation level distribution
        st.markdown("#### Explanation Requests by Level")
        
        levels = ['Level 1\n(Individual)', 'Level 2\n(Coordination)', 'Level 3\n(Collective)']
        requests = [145, 89, 73]
        
        fig = go.Figure(data=[go.Bar(
            x=levels, y=requests,
            marker_color=['#667eea', '#764ba2', '#f59e0b']
        )])
        
        fig.update_layout(
            yaxis_title="Number of Requests",
            height=300,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Agent performance metrics
    st.markdown("#### Agent Performance Matrix")
    
    agent_data = pd.DataFrame({
        'Agent': ['Code Generator', 'Security Analyst', 'Code Reviewer', 'Test Generator'],
        'Tasks': [87, 65, 91, 72],
        'Confidence': [0.85, 0.95, 0.89, 0.88],
        'Accuracy': [0.87, 0.97, 0.92, 0.90],
        'Interventions': [3, 1, 2, 1]
    })
    
    st.dataframe(
        agent_data,
        use_container_width=True,
        hide_index=True
    )

def show_recent_activity():
    """Display recent tasks and decisions"""
    st.subheader("Recent Multi-Agent Activities")
    
    # Sample recent tasks
    tasks = [
        {
            "time": "2 minutes ago",
            "task": "Implement OAuth 2.0 authentication",
            "team": ["Code Generator", "Security Analyst", "Test Generator"],
            "status": "✅ Completed",
            "confidence": 0.94,
            "intervention": "None"
        },
        {
            "time": "15 minutes ago",
            "task": "Refactor database query optimization",
            "team": ["Code Generator", "Code Reviewer"],
            "status": "✅ Completed",
            "confidence": 0.88,
            "intervention": "None"
        },
        {
            "time": "1 hour ago",
            "task": "Fix XSS vulnerability in user input",
            "team": ["Security Analyst", "Code Generator", "Code Reviewer"],
            "status": "⚠️ Human Review",
            "confidence": 0.76,
            "intervention": "Security critical"
        },
        {
            "time": "2 hours ago",
            "task": "Add unit tests for payment processing",
            "team": ["Test Generator", "Code Reviewer"],
            "status": "✅ Completed",
            "confidence": 0.92,
            "intervention": "None"
        }
    ]
    
    for task in tasks:
        with st.expander(f"{task['task']} - {task['time']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Status:** {task['status']}")
                st.markdown(f"**Agent Team:** {', '.join(task['team'])}")
                st.markdown(f"**Collective Confidence:** {task['confidence']:.2%}")
                
                if task['intervention'] != "None":
                    st.warning(f"⚠️ Intervention Required: {task['intervention']}")
            
            with col2:
                if st.button("View Full Explanation", key=f"explain_{task['time']}"):
                    st.info("Navigate to 'Explanation Explorer' page for detailed breakdown")

def show_quick_start():
    """Quick start guide for new users"""
    st.subheader("🚀 Get Started with CoHumAIn")
    
    st.markdown("""
    ### Three Steps to Transparent Multi-Agent Systems
    
    #### 1️⃣ Configure Your Agent Team
    Navigate to **Agent Configuration** to:
    - Define agent roles and capabilities
    - Set constitutional principles
    - Configure confidence thresholds
    """)
    
    if st.button("→ Go to Agent Configuration", key="nav_agents"):
        st.switch_page("pages/1_🤖_Agent_Configuration.py")
    
    st.markdown("""
    #### 2️⃣ Design Your Workflow
    Navigate to **Multi-Agent Workflow** to:
    - Create coordination graphs
    - Set delegation rules
    - Define conflict resolution strategies
    """)
    
    if st.button("→ Go to Workflow Designer", key="nav_workflow"):
        st.switch_page("pages/2_🔄_Multi_Agent_Workflow.py")
    
    st.markdown("""
    #### 3️⃣ Monitor & Explain
    Navigate to **Explanation Explorer** to:
    - View real-time decisions
    - Access 3-level explanations
    - Track safety metrics
    """)
    
    if st.button("→ Go to Explanation Explorer", key="nav_explain"):
        st.switch_page("pages/3_📊_Explanation_Explorer.py")
    
    st.divider()
    
    st.markdown("### 📺 Watch Tutorial")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Replace with actual tutorial
    
    st.divider()
    
    st.markdown("### 📖 Example Scenarios")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 💰 Finance")
        st.markdown("Trading agent team with risk management and compliance")
        if st.button("Load Finance Example"):
            st.info("Loading finance scenario...")
    
    with col2:
        st.markdown("#### 🏥 Healthcare")
        st.markdown("Multi-specialist diagnostic team with HIPAA compliance")
        if st.button("Load Healthcare Example"):
            st.info("Loading healthcare scenario...")
    
    with col3:
        st.markdown("#### 💻 Software")
        st.markdown("Code generation team with security analysis")
        if st.button("Load Software Example"):
            st.info("Loading software scenario...")

def show_documentation():
    """Display documentation links and resources"""
    st.subheader("📚 Documentation & Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📖 Core Documentation
        - [Getting Started Guide](https://cohumain.ai/docs/getting-started)
        - [Framework Architecture](https://cohumain.ai/docs/architecture)
        - [API Reference](https://cohumain.ai/docs/api)
        - [Python SDK](https://cohumain.ai/docs/sdk)
        
        #### 🏭 Industry Guides
        - [Finance & Trading](https://cohumain.ai/docs/finance)
        - [Healthcare & Medical](https://cohumain.ai/docs/healthcare)
        - [Software Engineering](https://cohumain.ai/docs/software)
        
        #### 🔒 Safety & Compliance
        - [Regulatory Compliance](https://cohumain.ai/docs/compliance)
        - [Safety Mechanisms](https://cohumain.ai/docs/safety)
        - [Audit Trail Generation](https://cohumain.ai/docs/audit)
        """)
    
    with col2:
        st.markdown("""
        #### 📄 Research & Papers
        - [XAI-2026 Paper](https://drive.google.com/file/d/1fc0bBEF0jxjlgBDZcTUkIuxVSkGLf39M/view?usp=drive_link)
        - [Evaluation Results](https://cohumain.ai/research/evaluation)
        - [Case Studies](https://cohumain.ai/research/case-studies)
        
        #### 🎓 Tutorials & Videos
        - [Video Tutorials](https://cohumain.ai/tutorials)
        - [Webinar Recordings](https://cohumain.ai/webinars)
        - [Code Examples](https://github.com/HimJoe/CoHumAIn-A-Framework-for-Explainable-Multi-Agent-Systems-with-Safe-Human-Collaboration/tree/main/examples)
        
        #### 💬 Community & Support
        - [Discord Community](https://discord.gg/cohumain)
        - [GitHub Discussions](https://github.com/HimJoe/CoHumAIn-A-Framework-for-Explainable-Multi-Agent-Systems-with-Safe-Human-Collaboration/discussions)
        - [Email Support](mailto:support@cohumain.ai)
        """)
    
    st.divider()
    
    st.markdown("#### 🎯 Quick Links")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.link_button("📦 PyPI Package", "https://pypi.org/project/cohumain/")
    
    with col2:
        st.link_button("🐙 GitHub Repo", "https://github.com/HimJoe/CoHumAIn-A-Framework-for-Explainable-Multi-Agent-Systems-with-Safe-Human-Collaboration")
    
    with col3:
        st.link_button("🌐 Website", "https://cohumain.ai")
    
    with col4:
        st.link_button("📧 Contact", "mailto:info@cohumain.ai")

def show_sidebar():
    """Display sidebar content"""
    st.markdown("### Navigation")
    
    st.markdown("""
    **Core Features:**
    - 🤖 Agent Configuration
    - 🔄 Multi-Agent Workflow
    - 📊 Explanation Explorer
    - 🛡️ Safety Dashboard
    - ⚖️ Trust Calibration
    - 📋 Audit & Compliance
    """)
    
    st.divider()
    
    st.markdown("### Settings")
    
    domain = st.selectbox(
        "Domain",
        ["Software Engineering", "Finance", "Healthcare", "General"]
    )
    
    regulatory_framework = st.selectbox(
        "Regulatory Framework",
        ["None", "GDPR", "EU AI Act", "HIPAA", "SEC", "FDA"]
    )
    
    safety_mode = st.select_slider(
        "Safety Mode",
        options=["Permissive", "Balanced", "Strict", "Maximum"],
        value="Balanced"
    )
    
    st.divider()
    
    st.markdown("### System Status")
    st.success("✅ Framework Active")
    st.info(f"⚙️ Mode: {safety_mode}")
    st.info(f"🏭 Domain: {domain}")
    
    if regulatory_framework != "None":
        st.info(f"📜 Compliance: {regulatory_framework}")
    
    st.divider()
    
    st.markdown("### Support")
    st.markdown("""
    Need help? 
    - [Documentation](https://cohumain.ai/docs)
    - [Discord](https://discord.gg/cohumain)
    - [Email Support](mailto:support@cohumain.ai)
    """)

if __name__ == "__main__":
    main()
