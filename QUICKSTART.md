# 🚀 QUICKSTART: Deploy CoHumAIn to GitHub & Streamlit

**Target Repository:** https://github.com/CoHumAInLabs/CoHumAIn-A-Framework-for-Explainable-Multi-Agent-Systems-with-Safe-Human-Collaboration

This guide gets your **Window of Transparency** app live in **under 30 minutes**.

---

## ⚡ Prerequisites (5 minutes)

```bash
# 1. Install requirements
python --version  # Must be 3.9+
git --version     # Must have git
```

```bash
# 2. Get API keys
# Anthropic: https://console.anthropic.com/
# OpenAI: https://platform.openai.com/api-keys
```

---

## 📥 Step 1: Get the Code (2 minutes)

### Option A: Download from Claude

All files are in the `/mnt/user-data/outputs/CoHumAIn_GitHub_Repo/` folder I created for you.

### Option B: Clone Existing Repo

```bash
git clone https://github.com/CoHumAInLabs/CoHumAIn-A-Framework-for-Explainable-Multi-Agent-Systems-with-Safe-Human-Collaboration.git

cd CoHumAIn-A-Framework-for-Explainable-Multi-Agent-Systems-with-Safe-Human-Collaboration
```

---

## 🔧 Step 2: Local Setup (5 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
```

**Edit `.env` file:**
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here
```

---

## 🧪 Step 3: Test Locally (3 minutes)

```bash
# Run the app
streamlit run app/Home.py
```

**Open:** http://localhost:8501

✅ **Expected:** Dashboard loads with 6 pages in sidebar  
✅ **Test:** Click through all pages  
✅ **Check:** No import errors  

---

## 📤 Step 4: Push to GitHub (5 minutes)

```bash
# Add all files
git add .

# Commit
git commit -m "🚀 Add CoHumAIn Window of Transparency app

Complete Streamlit app with:
- 6 interactive pages
- Real-time agent monitoring  
- Interrupt capability
- 3-level explanations
- Safety dashboard
- Trust calibration
- Audit trails"

# Push to GitHub
git push origin main
```

---

## ☁️ Step 5: Deploy to Streamlit Cloud (10 minutes)

### Method 1: Streamlit Cloud (Recommended)

1. Go to https://share.streamlit.io/
2. Click **"New app"**
3. **GitHub repo:** Select your repo
4. **Branch:** `main`
5. **Main file path:** `app/Home.py`
6. Click **"Advanced settings"**
7. **Add secrets:**
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   OPENAI_API_KEY = "sk-..."
   ```
8. Click **"Deploy!"**
9. Wait 2-3 minutes
10. Your app is live! 🎉

### Method 2: Deploy Button

Add this to your `README.md`:

```markdown
[![Deploy on Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
```

---

## 🎯 What You Get

### 6 Interactive Pages

#### 1️⃣ **Home Dashboard**
- System health metrics
- Active agents overview
- Recent activity feed
- Trust score tracking

#### 2️⃣ **Agent Configuration**
- Create custom agents
- Set constitutional principles
- Configure confidence thresholds
- Load industry templates (finance, healthcare, software)

#### 3️⃣ **Multi-Agent Workflow** ⭐ INTERRUPT CAPABILITY
- Visual coordination graph
- Real-time execution monitoring
- **🛑 INTERRUPT BUTTON** - Pause at any step
- View delegation decisions
- Inspect agent reasoning
- Approve/modify/escalate

#### 4️⃣ **Explanation Explorer** ⭐ 3-LEVEL TRANSPARENCY
- **Level 1:** Individual agent reasoning (Why did Agent X decide Y?)
- **Level 2:** Coordination decisions (How did agents collaborate?)
- **Level 3:** Collective outcomes (What did the team accomplish?)
- Interactive timeline view
- Attribution analysis

#### 5️⃣ **Safety Dashboard**
- Constitutional violation detection
- Misalignment alerts
- Intervention triggers
- Safety metric trends

#### 6️⃣ **Trust Calibration** ⭐ BUILD TRUST
- Calibration curve (predicted vs actual accuracy)
- Confidence-based automation levels
- Historical performance tracking
- Trust score by agent

---

## 🏭 Industry Examples Included

### 💰 Finance (SEC/MiFID II Compliant)
```python
python examples/finance/trading_team.py
```
- Market Analyst Agent
- Risk Manager Agent
- Compliance Officer Agent
- Trade Executor Agent

### 🏥 Healthcare (HIPAA Compliant)
```bash
# Create with Claude Code:
claude-code create "examples/healthcare/diagnostic_team.py"
```

### 💻 Software Engineering
```bash
# Create with Claude Code:
claude-code create "examples/software/authentication_scenario.py"
```

---

## 🔍 Window of Transparency Features

### 1. **Interrupt Agentic Flow**
```
User starts workflow → Agents execute → Low confidence detected → 
AUTOMATIC PAUSE → User reviews explanation → Approve OR Modify → Resume
```

### 2. **See Detailed Steps**
Every agent action includes:
- Thought process (reasoning trace)
- Action taken
- Observation (result)
- Confidence score
- Constitutional check

### 3. **Build Trust**
- Calibrated confidence (honest uncertainty)
- Attribution (who did what)
- Provenance (complete history)
- Validation (historical accuracy)

---

## 🛠️ Using Claude Code (Optional but Recommended)

Claude Code can help you extend the framework:

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Initialize in your repo
claude-code init

# Create missing pages
claude-code create "Create app/pages/4_🛡️_Safety_Dashboard.py with safety monitoring"

claude-code create "Create app/pages/5_⚖️_Trust_Calibration.py with trust metrics"

claude-code create "Create app/pages/6_📋_Audit_Compliance.py with audit trails"

# Create agent implementations
claude-code create "Create src/cohumain/agents/software.py with CodeGenerator, SecurityAnalyst classes"

# Create examples
claude-code create "Create examples/healthcare/diagnostic_team.py with HIPAA compliance"

# Create tests
claude-code create "Create tests/test_framework.py with pytest tests"
```

---

## 📊 Usage Example

```python
from cohumain import CoHumAInFramework, Agent

# Create framework
framework = CoHumAInFramework(
    domain="software",
    safety_mode="strict",
    stakeholder_type="developer"
)

# Add agents
framework.add_agents([
    Agent(name="Code Generator", role="Code Generator", expertise=0.85),
    Agent(name="Security Analyst", role="Security Analyst", expertise=0.95)
])

# Execute with transparency
result = framework.execute_task(
    task="Implement user authentication",
    human_in_loop=True  # Enable interrupt capability
)

# Access explanations
print(result['level1_explanations'])  # Individual reasoning
print(result['level2_explanations'])  # Coordination
print(result['level3_explanation'])   # Collective
```

---

## 🔒 For Regulated Industries

### Finance
```env
COHUMAIN_DOMAIN=finance
COHUMAIN_REGULATORY_FRAMEWORK=SEC
COHUMAIN_SAFETY_MODE=strict
```

### Healthcare
```env
COHUMAIN_DOMAIN=healthcare
COHUMAIN_REGULATORY_FRAMEWORK=HIPAA
COHUMAIN_SAFETY_MODE=maximum
ENABLE_AUDIT_LOGGING=true
```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] App loads at your Streamlit URL
- [ ] All 6 pages accessible
- [ ] Can create agents
- [ ] Workflow execution works
- [ ] Interrupt button functions
- [ ] Explanations display correctly
- [ ] Charts render properly
- [ ] No error messages
- [ ] Examples run successfully

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -e .
```

### Streamlit pages not showing
```bash
# Ensure pages are in app/pages/ with emoji prefixes
ls app/pages/
```

### API key errors
```bash
# Verify .env locally
cat .env

# Verify secrets in Streamlit Cloud
# Settings → Secrets → Add your keys
```

### Import errors
```bash
# Check all __init__.py files exist
find . -name "__init__.py"
```

---

## 📞 Support

- **GitHub Issues:** [Report bugs](https://github.com/CoHumAInLabs/CoHumAIn-Framework/issues)
- **Discussions:** [Ask questions](https://github.com/CoHumAInLabs/CoHumAIn-Framework/discussions)
- **Email:** support@cohumain.ai

---

## 🎉 You're Live!

Your Window of Transparency app is now helping users:

✅ **Interrupt** agentic workflows at any point  
✅ **Inspect** detailed agent reasoning  
✅ **Understand** coordination decisions  
✅ **Build trust** through transparency  
✅ **Comply** with regulations  
✅ **Ensure safety** in high-stakes domains  

**Share your deployment:**
- Tweet: "Just deployed CoHumAIn Window of Transparency! #ExplainableAI #MultiAgent"
- LinkedIn: Share with your network
- Reddit: r/MachineLearning, r/LLMDevs

---

## 🚀 Next Steps

1. **Customize** for your use case
2. **Add** domain-specific agents
3. **Integrate** with your systems
4. **Gather** user feedback
5. **Contribute** improvements back

**Star the repo:** ⭐ https://github.com/CoHumAInLabs/CoHumAIn-Framework

---

## 📚 Additional Resources

- **Full Setup Guide:** `SETUP_GUIDE.md`
- **Deployment Details:** `DEPLOYMENT_GUIDE.md`
- **API Documentation:** `docs/api_reference.md`
- **Research Paper:** `paper/cohumain_paper.pdf`

---

**Built with ❤️ by CoHumAIn Labs**  
**Making Multi-Agent AI Transparent, Safe, and Trustworthy**
