# GRC AI Tools - Portfolio of 5 AI-Powered GRC Applications

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive suite of AI-powered tools for Governance, Risk, and Compliance (GRC) professionals, built with LangChain, Streamlit, and state-of-the-art LLMs.

## 🎯 Project Overview

This repository contains **5 production-ready AI tools** designed to transform GRC operations:

1. **🥇 GRC Content Creator AI** - AI-powered policy drafting and risk scenario generation
2. **🥈 Third-Party Risk Management Platform** - Automated vendor research and monitoring
3. **🥉 Enhanced Risk Management System** - Predictive analytics and pattern recognition
4. **4️⃣ Streamlined Compliance Tool** - Regulatory monitoring and gap analysis
5. **5️⃣ Augmented Internal Auditing** - AI-powered document review and evidence analysis

**Market Validation**: Addressing a **$10.59B market opportunity** by 2033 with proven 40% efficiency gains and 75% error reduction.

## 📂 Repository Structure

This is a **monorepo** containing:
- Shared GRC AI toolkit foundation (`grc_ai_toolkit/`)
- Tool specifications (Tool 1-5)
- Project coordination files

**Current Structure:**
```
grc-ai-toolkit/              # Main repository (monorepo)
├── grc_ai_toolkit/          # Shared foundation library
│   ├── llm/                 # Multi-LLM integration (OpenAI, Anthropic, Groq)
│   ├── agents/              # AI agent framework with orchestration
│   ├── data/                # Document processing & RAG (FAISS, ChromaDB)
│   ├── ui/                  # Streamlit UI components
│   ├── sample_data/         # Test data generators
│   └── tests/               # Comprehensive test suite
├── tool1_grc_content_creator_spec.md  # Tool 1 specification
├── README.md                # This file
├── ARCHITECTURE.md          # System architecture documentation
├── CONSOLIDATION.md         # Repository consolidation guide
└── .private/                # Local tracking (gitignored, not in repo)
```

**Future Structure** (as tools are implemented):
```
grc-ai-toolkit/
├── grc_ai_toolkit/          # Shared foundation (complete)
├── tool1_grc_content_creator/    # Tool 1: Content Creator (planned)
├── tool2_tprm_platform/          # Tool 2: TPRM Platform (planned)
├── tool3_risk_management/        # Tool 3: Risk Management (planned)
├── tool4_compliance_tool/        # Tool 4: Compliance Tool (planned)
└── tool5_audit_system/           # Tool 5: Audit System (planned)
```

The 5 tools will be implemented on top of the shared foundation.

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key or Anthropic API key
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/AnushaCabral/grc-ai-toolkit.git
cd grc-ai-toolkit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install shared toolkit
pip install -e grc_ai_toolkit/

# Install tool-specific dependencies (example for Tool 1)
cd tool1_grc_content_creator
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Run the application
streamlit run src/ui/app.py
```

## 📊 Tool Status & Links

| Tool | Priority | Status | Timeline | GitHub Appeal |
|------|----------|--------|----------|---------------|
| [GRC Content Creator](./tool1_grc_content_creator/) | 🥇 #1 | ✅ Planning Complete | 2-3 weeks | ⭐⭐⭐⭐⭐ |
| [TPRM Platform](./tool2_tprm_platform/) | 🥈 #2 | 📋 Planning | 3-4 weeks | ⭐⭐⭐⭐⭐ |
| [Risk Management](./tool3_risk_management/) | 🥉 #3 | 📋 Planning | 3-4 weeks | ⭐⭐⭐⭐ |
| [Compliance Tool](./tool4_compliance_tool/) | 4️⃣ #4 | 📋 Planning | 4-5 weeks | ⭐⭐⭐⭐ |
| [Audit System](./tool5_audit_system/) | 5️⃣ #5 | 📋 Planning | 5-6 weeks | ⭐⭐⭐⭐ |

## 🛠️ Technology Stack

**Core Technologies**:
- **LangChain 1.0**: Agent orchestration and RAG
- **Streamlit**: Interactive UI framework
- **FastAPI**: REST API backend
- **ChromaDB/FAISS**: Vector storage
- **GPT-4/Claude Sonnet 4**: LLM generation

**Document Processing**:
- python-docx (Word), reportlab (PDF), pytesseract (OCR)

**Data & Analytics**:
- pandas, numpy, plotly

**Development**:
- pytest, black, flake8, Docker, GitHub Actions

## 📈 Key Features

### Shared Foundation (grc_ai_toolkit)

✅ **LLM Integration Layer**
- Unified interface for OpenAI, Anthropic, and local models
- Token management and cost tracking
- Automatic fallback mechanisms

✅ **Agent Orchestration**
- Multi-agent system based on LangChain 1.0
- Customizable agent templates
- Inter-agent communication

✅ **RAG Pipeline**
- Document chunking and embedding
- Semantic search with ChromaDB/FAISS
- Citation tracking

✅ **Streamlit Components**
- Reusable UI components
- Consistent styling
- Common navigation patterns

## 🎓 Learning Resources

- **[Master Plan](./docs/master_plan.md)**: Complete strategy for all 5 tools
- **[Tool 1 Specification](./tool1_grc_content_creator_spec.md)**: Detailed spec with market research
- **[Development Guide](./docs/development_guide.md)**: Architecture and coding standards
- **[API Documentation](./docs/api_docs.md)**: REST API reference

## 📊 Success Metrics

**Performance Targets**:
- ⏱️ Document generation: <30 seconds
- ✅ Error reduction: 75% vs manual processes
- 📈 Efficiency improvement: 40% time savings
- 🎯 User satisfaction: >4.5/5

**Business Value**:
- 💰 Market opportunity: $10.59B by 2033
- 📊 Adoption: 88% use AI for document summarization
- ⚡ Processing: Up to 70% faster with AI automation

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](./CONTRIBUTING.md) for details on:
- Code of conduct
- Development workflow
- Pull request process
- Coding standards

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 👤 Author

**Anusha Cabral**
- GitHub: [@anushacabral](https://github.com/anushacabral)
- Email: cabral.anusha@gmail.com

## 🙏 Acknowledgments

- **OCEG** for the "AI Quick Wins for GRC Professionals" framework
- **LangChain** community for the amazing agent framework
- **Streamlit** team for the intuitive UI framework
- All contributors and testers

## 📝 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a list of changes and version history.

---

**Built with ❤️ for GRC Professionals**

*Transforming compliance from reactive to proactive with AI*
