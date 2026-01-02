# GRC AI Toolkit

A comprehensive Python toolkit for building AI-powered Governance, Risk, and Compliance (GRC) applications.

## Features

### 🤖 LLM Integration
- **Multi-provider support**: OpenAI (GPT-4, GPT-4 Turbo), Anthropic (Claude Sonnet 4, Claude Opus 4)
- **Automatic fallback**: Seamlessly switch between providers on failure
- **Cost tracking**: Monitor token usage and API costs
- **Response caching**: Reduce costs with intelligent caching
- **Pre-built prompts**: GRC-specific prompt templates

### 🔧 Agent Framework
- **BaseAgent**: Abstract base class for custom agents
- **AgentOrchestrator**: Multi-agent workflow coordination
- **Pre-built agents**: Research, Analysis, Generation, Review agents
- **Specialized agents**: Policy Drafting, Risk Assessment agents

### 📊 Data Processing
- **Document processing**: PDF, Word, Text, CSV, HTML support
- **Vector stores**: FAISS and ChromaDB for RAG
- **Text chunking**: Optimized for LLM context windows
- **Export utilities**: Markdown, Word, PDF, HTML export

### 🎨 UI Components
- **Streamlit components**: Reusable UI widgets
- **GRC forms**: Pre-built forms for common GRC tasks
- **Layout templates**: Standardized page layouts
- **Dashboard components**: Metrics, charts, and visualizations

### 🧪 Sample Data
- **Data generators**: Realistic GRC sample data
- **Risk data**: Risk assessments and scenarios
- **Policy data**: Policy documents and metadata
- **Incident data**: Security incident reports
- **Vendor data**: Third-party risk management data
- **Compliance data**: Controls and gap analysis

## Installation

### Prerequisites

- **Python 3.10, 3.11, or 3.12** (3.11 or 3.12 recommended)
- OpenAI and/or Anthropic API keys

### Install from Source

```bash
# Navigate to toolkit directory
cd grc_ai_toolkit

# Install in development mode (recommended for development)
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"

# Or install with all optional dependencies
pip install -e ".[all]"
```

### Quick Install

```bash
# Just the core package
pip install .
```

### Dependencies

All dependencies are managed in `pyproject.toml`:
- **Core**: LangChain 1.0+, OpenAI, Anthropic
- **Optional dev**: pytest, black, ruff, mypy
- **Optional local-llm**: transformers, torch

## Quick Start

### 1. Set up environment variables

Create a `.env` file:

```env
# LLM Configuration
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional: Model selection
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
```

### 2. Use LLM Manager

```python
from grc_ai_toolkit.llm import LLMManager, LLMConfig

# Initialize with default config (reads from .env)
llm_manager = LLMManager()

# Generate text
response = llm_manager.generate(
    prompt="Create a data privacy policy outline",
    system_message="You are a GRC policy expert."
)

print(response)

# Check usage stats
stats = llm_manager.get_stats()
print(f"Total cost: ${stats['total_cost']}")
```

### 3. Use Pre-built Prompts

```python
from grc_ai_toolkit.llm import PromptLibrary

# Get a prompt template
template = PromptLibrary.POLICY_GENERATOR

# Format with variables
prompt = template.format(
    policy_type="Information Security",
    framework="SOC 2",
    industry="Technology/SaaS",
    requirements="Include incident response procedures",
    target_audience="All Employees"
)

# Generate policy
policy = llm_manager.generate(
    prompt=prompt,
    system_message=template.system_message
)
```

### 4. Use Agents

```python
from grc_ai_toolkit.agents import ResearchAgent, GenerationAgent
from grc_ai_toolkit.agents import AgentOrchestrator

# Create agents
research_agent = ResearchAgent(llm_manager)
generation_agent = GenerationAgent(llm_manager)

# Create workflow
orchestrator = AgentOrchestrator(name="Policy Creation")

orchestrator.add_step(
    "research",
    research_agent,
    "Research best practices for {topic}"
)

orchestrator.add_step(
    "generate",
    generation_agent,
    "Generate policy based on: {research}",
    depends_on=["research"]
)

# Execute
result = orchestrator.execute(context={"topic": "data encryption"})
print(result.results["generate"])
```

### 5. Process Documents

```python
from grc_ai_toolkit.data import DocumentProcessor, VectorStore, VectorStoreConfig

# Process documents
processor = DocumentProcessor()
chunks = processor.process_document("path/to/policy.pdf")

# Create vector store for RAG
config = VectorStoreConfig(k=2)  # k=2 is optimal per research
vector_store = VectorStore(config)
vector_store.create_from_documents(chunks)

# Search
results = vector_store.search("What is our data retention policy?")
for doc in results:
    print(doc.page_content)
```

### 6. Build Streamlit UI

```python
import streamlit as st
from grc_ai_toolkit.ui import StreamlitComponents, GRCFormBuilder

st.title("GRC Policy Generator")

# Use pre-built form
form_data = GRCFormBuilder.policy_generation_form()

if form_data:
    # Generate policy using form data
    with st.spinner("Generating policy..."):
        policy = llm_manager.generate(...)

    # Display results
    st.markdown(policy)

    # Download button
    StreamlitComponents.download_button(
        "Download Policy",
        policy,
        "policy.md",
        mime="text/markdown"
    )
```

### 7. Generate Sample Data

```python
from grc_ai_toolkit.sample_data import RiskDataGenerator

# Generate sample risks
risks = RiskDataGenerator.generate_risks(count=50)

# Use in development/testing
import pandas as pd
df = pd.DataFrame(risks)
print(df.head())
```

## Architecture

```
grc_ai_toolkit/
├── llm/                    # LLM integration layer
│   ├── manager.py         # Unified LLM manager
│   ├── config.py          # Configuration classes
│   ├── prompts.py         # Prompt templates
│   └── utils.py           # Utility functions
│
├── agents/                 # AI agent framework
│   ├── base.py            # BaseAgent class
│   ├── orchestrator.py    # Multi-agent orchestration
│   └── templates.py       # Pre-built agent templates
│
├── data/                   # Data processing
│   ├── processor.py       # Document processing
│   ├── vector_store.py    # RAG vector stores
│   └── exporters.py       # Export utilities
│
├── ui/                     # Streamlit components
│   ├── components.py      # Reusable UI widgets
│   ├── layouts.py         # Layout templates
│   └── forms.py           # GRC-specific forms
│
└── sample_data/           # Sample data generators
    └── generators.py      # Data generation utilities
```

## Use Cases

This toolkit supports building:

1. **Policy Generation Tools**: AI-assisted policy document creation
2. **Risk Management Systems**: Risk assessment and scenario analysis
3. **Compliance Automation**: Gap analysis and control mapping
4. **Incident Management**: Report generation and analysis
5. **Vendor Risk Management**: Third-party assessment automation

## API Documentation

### LLM Manager

```python
class LLMManager:
    def __init__(self, config: Optional[LLMConfig] = None)
    def generate(self, prompt: str, system_message: Optional[str] = None, **kwargs) -> str
    def get_stats(self) -> Dict[str, Any]
    def reset_stats(self) -> None
```

### Agents

```python
class BaseAgent:
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str
    def reset_state(self) -> None
    def get_state_summary(self) -> Dict[str, Any]

class AgentOrchestrator:
    def add_step(self, step_name: str, agent: BaseAgent, task_template: str, ...)
    def execute(self, context: Optional[Dict[str, Any]] = None) -> WorkflowResult
    def visualize(self) -> str
```

### Document Processing

```python
class DocumentProcessor:
    def load_document(self, file_path: Union[str, Path]) -> List[Document]
    def process_document(self, file_path: Union[str, Path], ...) -> List[Document]
    def extract_text(self, file_path: Union[str, Path]) -> str
    def get_document_stats(self, file_path: Union[str, Path]) -> Dict[str, Any]
```

### Vector Store

```python
class VectorStore:
    def create_from_documents(self, documents: List[Document]) -> None
    def search(self, query: str, k: Optional[int] = None, ...) -> List[Document]
    def save(self, path: Optional[str] = None) -> None
    def load(self, path: Optional[str] = None) -> None
```

## Testing

Run tests:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=grc_ai_toolkit --cov-report=html

# Run specific test file
pytest tests/test_llm.py
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Email: support@grc-toolkit.example.com

## Acknowledgments

- Built with LangChain 1.0
- Follows 2025 best practices for AI applications
- Inspired by OCEG GRC framework

---

**Version**: 1.0.0
**Last Updated**: December 2025
