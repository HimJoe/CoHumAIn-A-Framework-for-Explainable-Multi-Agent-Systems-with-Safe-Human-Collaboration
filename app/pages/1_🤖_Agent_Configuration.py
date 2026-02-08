"""
CoHumAIn Framework - Agent Configuration Page
Configure agents with roles, capabilities, and constitutional principles
"""

import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Agent Configuration", page_icon="🤖", layout="wide")

st.title("🤖 Agent Configuration")
st.markdown("Define and configure agents for your multi-agent system")

# Initialize session state
if 'agents' not in st.session_state:
    st.session_state.agents = []

tab1, tab2, tab3 = st.tabs(["➕ Create Agent", "📋 Manage Agents", "📦 Templates"])

with tab1:
    st.subheader("Create New Agent")
    
    col1, col2 = st.columns(2)
    
    with col1:
        agent_name = st.text_input("Agent Name", placeholder="e.g., Code Generator")
        agent_role = st.selectbox(
            "Agent Role",
            ["Code Generator", "Security Analyst", "Code Reviewer", "Test Generator",
             "Market Analyst", "Risk Manager", "Compliance Officer",
             "Radiologist", "Pathologist", "Primary Care Physician",
             "Custom"]
        )
        
        if agent_role == "Custom":
            custom_role = st.text_input("Custom Role Name")
        
        expertise_level = st.slider(
            "Expertise Level",
            min_value=0.0,
            max_value=1.0,
            value=0.85,
            step=0.05
        )
        
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.80,
            step=0.05,
            help="Minimum confidence required before agent makes decisions"
        )
    
    with col2:
        st.markdown("#### Capabilities")
        
        capabilities = st.multiselect(
            "Select Agent Capabilities",
            [
                "Code Generation",
                "Code Review",
                "Security Analysis",
                "Test Generation",
                "Market Analysis",
                "Risk Assessment",
                "Compliance Checking",
                "Diagnostic Analysis",
                "Data Analysis",
                "Natural Language Processing"
            ]
        )
        
        st.markdown("#### Constitutional Principles")
        
        principles = st.text_area(
            "Define Constitutional Principles (one per line)",
            placeholder="e.g.,\nAlways follow secure coding practices\nMaintain test coverage above 80%\nZero tolerance for known vulnerabilities",
            height=150
        )
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_retries = st.number_input("Max Retries", min_value=1, max_value=10, value=3)
    
    with col2:
        timeout = st.number_input("Timeout (seconds)", min_value=10, max_value=300, value=60)
    
    with col3:
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    
    if st.button("✅ Create Agent", type="primary", use_container_width=True):
        new_agent = {
            "name": agent_name,
            "role": agent_role if agent_role != "Custom" else custom_role,
            "expertise": expertise_level,
            "confidence_threshold": confidence_threshold,
            "capabilities": capabilities,
            "principles": principles.split('\n') if principles else [],
            "max_retries": max_retries,
            "timeout": timeout,
            "priority": priority
        }
        
        st.session_state.agents.append(new_agent)
        st.success(f"✅ Agent '{agent_name}' created successfully!")
        st.balloons()

with tab2:
    st.subheader("Manage Existing Agents")
    
    if st.session_state.agents:
        # Create DataFrame from agents
        df = pd.DataFrame([
            {
                "Name": agent['name'],
                "Role": agent['role'],
                "Expertise": f"{agent['expertise']:.2f}",
                "Confidence": f"{agent['confidence_threshold']:.2f}",
                "Capabilities": len(agent['capabilities']),
                "Principles": len(agent['principles']),
                "Priority": agent['priority']
            }
            for agent in st.session_state.agents
        ])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Agent details
        if st.session_state.agents:
            agent_names = [a['name'] for a in st.session_state.agents]
            selected_agent = st.selectbox("Select Agent to View/Edit", agent_names)
            
            agent = next(a for a in st.session_state.agents if a['name'] == selected_agent)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Agent Details")
                st.json(agent)
            
            with col2:
                st.markdown("#### Actions")
                
                if st.button("🔄 Reload Agent"):
                    st.info("Agent reloaded")
                
                if st.button("⏸️ Pause Agent"):
                    st.warning("Agent paused")
                
                if st.button("❌ Delete Agent", type="secondary"):
                    st.session_state.agents = [a for a in st.session_state.agents if a['name'] != selected_agent]
                    st.success(f"Agent '{selected_agent}' deleted")
                    st.rerun()
        
        st.divider()
        
        # Export/Import
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Export Configuration")
            config_json = json.dumps(st.session_state.agents, indent=2)
            st.download_button(
                "📥 Download Configuration (JSON)",
                config_json,
                file_name="cohumain_agents.json",
                mime="application/json"
            )
        
        with col2:
            st.markdown("#### Import Configuration")
            uploaded_file = st.file_uploader("Upload Configuration JSON", type=['json'])
            if uploaded_file:
                imported_config = json.load(uploaded_file)
                if st.button("Import Agents"):
                    st.session_state.agents.extend(imported_config)
                    st.success(f"Imported {len(imported_config)} agents")
                    st.rerun()
    
    else:
        st.info("No agents configured yet. Create your first agent in the 'Create Agent' tab!")

with tab3:
    st.subheader("Agent Templates")
    st.markdown("Quick-start templates for common agent configurations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 💻 Software Engineering")
        
        if st.button("Load Software Team"):
            software_agents = [
                {
                    "name": "Code Generator",
                    "role": "Code Generator",
                    "expertise": 0.85,
                    "confidence_threshold": 0.80,
                    "capabilities": ["Code Generation"],
                    "principles": ["Follow secure coding practices", "Maintain test coverage"],
                    "max_retries": 3,
                    "timeout": 60,
                    "priority": "High"
                },
                {
                    "name": "Security Analyst",
                    "role": "Security Analyst",
                    "expertise": 0.95,
                    "confidence_threshold": 0.90,
                    "capabilities": ["Security Analysis", "Compliance Checking"],
                    "principles": ["Zero tolerance for known vulnerabilities"],
                    "max_retries": 2,
                    "timeout": 90,
                    "priority": "Critical"
                },
                {
                    "name": "Code Reviewer",
                    "role": "Code Reviewer",
                    "expertise": 0.89,
                    "confidence_threshold": 0.85,
                    "capabilities": ["Code Review"],
                    "principles": ["Enforce coding standards", "Ensure maintainability"],
                    "max_retries": 3,
                    "timeout": 60,
                    "priority": "High"
                },
                {
                    "name": "Test Generator",
                    "role": "Test Generator",
                    "expertise": 0.88,
                    "confidence_threshold": 0.85,
                    "capabilities": ["Test Generation"],
                    "principles": ["Achieve 80% coverage", "Test failure paths"],
                    "max_retries": 3,
                    "timeout": 60,
                    "priority": "Medium"
                }
            ]
            st.session_state.agents.extend(software_agents)
            st.success("✅ Loaded 4 software engineering agents")
            st.rerun()
    
    with col2:
        st.markdown("#### 💰 Finance & Trading")
        
        if st.button("Load Finance Team"):
            finance_agents = [
                {
                    "name": "Market Analyst",
                    "role": "Market Analyst",
                    "expertise": 0.92,
                    "confidence_threshold": 0.85,
                    "capabilities": ["Market Analysis", "Data Analysis"],
                    "principles": ["Evidence-based recommendations"],
                    "max_retries": 3,
                    "timeout": 120,
                    "priority": "High"
                },
                {
                    "name": "Risk Manager",
                    "role": "Risk Manager",
                    "expertise": 0.96,
                    "confidence_threshold": 0.95,
                    "capabilities": ["Risk Assessment"],
                    "principles": ["Conservative risk management"],
                    "max_retries": 2,
                    "timeout": 90,
                    "priority": "Critical"
                },
                {
                    "name": "Compliance Officer",
                    "role": "Compliance Officer",
                    "expertise": 0.99,
                    "confidence_threshold": 0.98,
                    "capabilities": ["Compliance Checking"],
                    "principles": ["Strict regulatory compliance"],
                    "max_retries": 2,
                    "timeout": 120,
                    "priority": "Critical"
                }
            ]
            st.session_state.agents.extend(finance_agents)
            st.success("✅ Loaded 3 finance & trading agents")
            st.rerun()
    
    with col3:
        st.markdown("#### 🏥 Healthcare")
        
        if st.button("Load Healthcare Team"):
            healthcare_agents = [
                {
                    "name": "Radiologist AI",
                    "role": "Radiologist",
                    "expertise": 0.94,
                    "confidence_threshold": 0.90,
                    "capabilities": ["Diagnostic Analysis"],
                    "principles": ["Patient safety first", "HIPAA compliance"],
                    "max_retries": 2,
                    "timeout": 180,
                    "priority": "Critical"
                },
                {
                    "name": "Pathologist AI",
                    "role": "Pathologist",
                    "expertise": 0.93,
                    "confidence_threshold": 0.90,
                    "capabilities": ["Diagnostic Analysis"],
                    "principles": ["Thorough analysis", "HIPAA compliance"],
                    "max_retries": 2,
                    "timeout": 180,
                    "priority": "Critical"
                },
                {
                    "name": "Primary Care AI",
                    "role": "Primary Care Physician",
                    "expertise": 0.89,
                    "confidence_threshold": 0.85,
                    "capabilities": ["Diagnostic Analysis"],
                    "principles": ["Holistic patient care", "HIPAA compliance"],
                    "max_retries": 3,
                    "timeout": 120,
                    "priority": "High"
                }
            ]
            st.session_state.agents.extend(healthcare_agents)
            st.success("✅ Loaded 3 healthcare diagnostic agents")
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 Agent Statistics")
    st.metric("Total Agents", len(st.session_state.agents))
    
    if st.session_state.agents:
        avg_expertise = sum(a['expertise'] for a in st.session_state.agents) / len(st.session_state.agents)
        st.metric("Avg Expertise", f"{avg_expertise:.2f}")
        
        critical_count = sum(1 for a in st.session_state.agents if a['priority'] == 'Critical')
        st.metric("Critical Priority", critical_count)
    
    st.divider()
    
    st.markdown("### 💡 Tips")
    st.info("""
    **Best Practices:**
    - Set confidence thresholds based on task criticality
    - Higher expertise = more weight in collective decisions
    - Define clear constitutional principles
    - Use templates as starting points
    """)
