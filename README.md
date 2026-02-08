# CoHumAIn: Explainable Multi-Agent Systems Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cohumain.streamlit.app)
[![Paper](https://img.shields.io/badge/paper-XAI--2026-red)](https://github.com/CoHumAInLabs/CoHumAIn-Framework/blob/main/paper/cohumain_paper.pdf)

**Collective Human and Machine Intelligence (CoHumAIn)** is a domain-agnostic framework that provides transparent, safe, and human-centered explainability for multi-agent AI systems. Designed for high-stakes domains like **finance**, **healthcare**, and **software engineering**.

🎯 **Solving the Multi-Agent Transparency Crisis**: While 82% of developers use AI agents and 41% of code is AI-generated, only 3.8% trust AI outputs enough to ship without review. CoHumAIn bridges this trust gap.

---

## 🌟 Key Features

### 🔍 Window of Transparency for Regulated Industries
- **Real-time Explainability**: Understand agent decisions as they happen
- **Compliance-Ready**: Built for GDPR, EU AI Act, FDA, SEC requirements
- **Audit Trail**: Complete decision provenance and responsibility tracking
- **Safety Monitoring**: Detect misalignment and coordination failures

### 🎯 Four Core Mechanisms

1. **📊 Hierarchical Explanation Generation**
   - Level 1: Individual agent reasoning (extends ReAct)
   - Level 2: Coordination decisions (NOVEL - delegation, conflict resolution)
   - Level 3: Collective behavior (NOVEL - emergent attribution, temporal causality)

2. **🛡️ Safety-Aware Attribution**
   - Trace outcomes to responsible agents
   - Detect constitutional violations and emergent risks
   - Automatic intervention triggers for high-stakes decisions

3. **👥 Cognitive-Aligned Interfaces**
   - Stakeholder-adaptive explanations (end users, developers, auditors, regulators)
   - Progressive disclosure with drill-down capability
   - Evidence-based reasoning (Evaluative AI paradigm)

4. **⚖️ Trust Calibration**
   - Collective confidence aggregation
   - Task-human matching (in/on/out-of-the-loop automation)
   - Historical calibration learning

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/CoHumAInLabs/CoHumAIn-Framework.git
cd CoHumAIn-Framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (Anthropic, OpenAI, etc.)
```

### Run Streamlit App

```bash
streamlit run app/Home.py
```

Visit `http://localhost:8501` to access the **Window of Transparency** interface!

### Python API Usage

```python
from cohumain import CoHumAInFramework, Agent
from cohumain.agents import CodeGenerator, SecurityAnalyst

# Initialize framework
framework = CoHumAInFramework(
    safety_mode="strict",
    explanation_level="all",
    stakeholder="developer"
)

# Create agent team
generator = CodeGenerator(name="CodeGen", confidence_threshold=0.85)
security = SecurityAnalyst(name="SecAnalyst", confidence_threshold=0.95)

framework.add_agents([generator, security])

# Execute task with full transparency
result = framework.execute_task(
    task="Implement user authentication with bcrypt",
    human_in_loop=True
)

# Access hierarchical explanations
print(result.level1_explanations)  # Individual agent reasoning
print(result.level2_explanations)  # Coordination decisions
print(result.level3_explanation)   # Collective attribution

# Check safety status
if result.requires_human_review:
    print(f"Intervention needed: {result.intervention_reason}")
```

---

## 📱 Streamlit App Features

### 🏠 Home Dashboard
- System overview and health monitoring
- Active agent teams
- Recent decisions and explanations
- Trust calibration metrics

### 🤖 Agent Configuration
- Define custom agents with roles and capabilities
- Set constitutional principles
- Configure confidence thresholds
- Assign expertise weights

### 🔄 Multi-Agent Workflow
- Visual coordination graph
- Real-time execution monitoring
- Delegation decision tracking
- Conflict resolution visualization

### 📊 Explanation Explorer
- Three-level hierarchical explanations
- Interactive timeline view
- Attribution analysis with responsibility breakdown
- Counterfactual "what-if" scenarios

### 🛡️ Safety Dashboard
- Constitutional compliance monitoring
- Misalignment detection alerts
- Intervention trigger logs
- Safety metric trends

### ⚙️ Trust Calibration
- Collective confidence visualization
- Automation level recommendations
- Calibration curve analysis
- Historical accuracy tracking

### 📋 Audit & Compliance
- Complete decision provenance
- Regulatory compliance reports (GDPR, EU AI Act)
- Exportable audit trails (JSON, CSV, PDF)
- Stakeholder-specific views

---

## 🏭 Industry Examples

### 💰 Finance: Trading Agent Team

```python
from cohumain.examples.finance import (
    MarketAnalyst, RiskManager, TradeExecutor, ComplianceOfficer
)

# Create regulated trading team
trading_team = CoHumAInFramework(
    domain="finance",
    regulatory_framework="SEC",
    risk_tolerance="conservative"
)

trading_team.add_agents([
    MarketAnalyst(expertise=0.92),
    RiskManager(expertise=0.96),
    TradeExecutor(expertise=0.88),
    ComplianceOfficer(expertise=0.99)
])

# Execute with full transparency
trade_result = trading_team.execute_task(
    task="Analyze AAPL for portfolio rebalancing",
    human_in_loop=True  # Required for high-stakes decisions
)

# Generate compliance report
report = trading_team.generate_compliance_report(
    standard="SEC Rule 15c3-5",
    format="pdf"
)
```

### 🏥 Healthcare: Diagnostic Agent Team

```python
from cohumain.examples.healthcare import (
    Radiologist, Pathologist, Geneticist, PrimaryCarePhysician
)

# Create HIPAA-compliant diagnostic team
diagnostic_team = CoHumAInFramework(
    domain="healthcare",
    regulatory_framework="HIPAA+FDA",
    safety_mode="maximum"
)

diagnostic_team.add_agents([
    Radiologist(expertise=0.94),
    Pathologist(expertise=0.93),
    Geneticist(expertise=0.91),
    PrimaryCarePhysician(expertise=0.89)
])

# Execute diagnosis with full attribution
diagnosis = diagnostic_team.execute_task(
    task="Evaluate patient case for suspected lymphoma",
    patient_id="encrypted_id_12345",
    human_in_loop=True  # Always required for medical decisions
)

# Access clinical decision support
print(diagnosis.evidence_summary)
print(diagnosis.specialist_disagreements)
print(diagnosis.recommended_next_steps)
```

### 💻 Software Engineering: Code Review Team

See full example in `examples/software/authentication_scenario.py`

---

## 🏗️ Architecture

```
CoHumAIn Framework
│
├── Agent Layer (Individual Reasoning)
│   ├── ReAct-based reasoning traces
│   ├── Constitutional alignment
│   └── Confidence quantification
│
├── Coordination Layer (Inter-Agent Logic)
│   ├── Delegation manager
│   ├── Conflict resolver
│   └── Information flow controller
│
├── Explanation Layer (Transparency Mechanisms)
│   ├── Hierarchical explanation generator
│   ├── Safety-aware attributor
│   ├── Cognitive interface adapter
│   └── Trust calibrator
│
└── Human Interface Layer (Stakeholder Views)
    ├── Developer console
    ├── End user dashboard
    ├── Auditor reports
    └── Regulator compliance views
```

---

## 📚 Documentation

- **[Getting Started Guide](docs/getting_started.md)** - Installation and first steps
- **[Framework Documentation](docs/framework.md)** - Core concepts and API reference
- **[Industry Guides](docs/industries/)** - Finance, healthcare, software engineering
- **[Safety & Compliance](docs/safety.md)** - Regulatory requirements and best practices
- **[Evaluation Methodology](docs/evaluation.md)** - Metrics and validation
- **[API Reference](docs/api/)** - Complete Python API documentation
- **[Research Paper](paper/cohumain_paper.pdf)** - XAI-2026 submission

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test suites
pytest tests/test_explanation.py
pytest tests/test_safety.py
pytest tests/test_coordination.py

# Run with coverage
pytest --cov=src/cohumain tests/
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run linting
black src/ tests/
flake8 src/ tests/
mypy src/
```

---

## 📊 Evaluation Results

From our study with 60 professional developers:

| Metric | Without CoHumAIn | With CoHumAIn | Improvement |
|--------|------------------|---------------|-------------|
| Appropriate Reliance | 64% | 89% | +39% |
| Error Detection Rate | 52% | 81% | +56% |
| Time to Diagnosis | 4.2 min | 1.8 min | -57% |
| Trust Calibration | 0.68 | 0.92 | +35% |
| User Satisfaction | 3.2/5 | 4.6/5 | +44% |

See full evaluation in [docs/evaluation.md](docs/evaluation.md)

---

## 🎓 Citation

If you use CoHumAIn in your research, please cite:

```bibtex
@inproceedings{joshi2026cohumain,
  title={CoHumAIn: A Framework for Explainable Multi-Agent Systems with Safe Human Collaboration},
  author={Joshi, Himanshu and Shukla, Shivani},
  booktitle={International Workshop on Explainable Artificial Intelligence (XAI)},
  year={2026},
  organization={Springer}
}
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Built on [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- Inspired by [ReAct](https://arxiv.org/abs/2210.03629) and [Constitutional AI](https://arxiv.org/abs/2212.08073)
- Powered by [Anthropic Claude](https://www.anthropic.com/claude) and [OpenAI](https://openai.com/)
- UI built with [Streamlit](https://streamlit.io/)

---

## 📞 Contact & Support

- **Website**: [https://cohumain.ai](https://cohumain.ai)
- **Email**: info@cohumain.ai
- **Issues**: [GitHub Issues](https://github.com/CoHumAInLabs/CoHumAIn-Framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CoHumAInLabs/CoHumAIn-Framework/discussions)
- **Twitter**: [@CoHumAInLabs](https://twitter.com/CoHumAInLabs)

---

## 🗺️ Roadmap

### v1.0 (Q2 2026) - Initial Release ✅
- Core framework implementation
- Streamlit app with Window of Transparency
- Software engineering examples
- Basic safety mechanisms

### v1.1 (Q3 2026)
- Healthcare domain implementation
- Finance domain implementation
- HIPAA compliance features
- SEC/FDA regulatory reports

### v1.2 (Q4 2026)
- Advanced mechanistic interpretability
- Multi-language support
- Mobile app for monitoring
- Enterprise deployment guides

### v2.0 (2027)
- Federated multi-agent systems
- Cross-organizational transparency
- Advanced formal verification
- AI safety certifications

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CoHumAInLabs/CoHumAIn-Framework&type=Date)](https://star-history.com/#CoHumAInLabs/CoHumAIn-Framework&Date)

---

## 🌍 Community

Join our community of researchers and practitioners building transparent, safe, and human-centered multi-agent systems!

- [Discord Server](https://discord.gg/cohumain) - Real-time discussion
- [Monthly Webinars](https://cohumain.ai/webinars) - Framework deep-dives
- [Newsletter](https://cohumain.ai/newsletter) - Latest research and updates

---

**Built with ❤️ by the CoHumAIn Labs team**

*Making multi-agent AI systems transparent, safe, and trustworthy for everyone.*
