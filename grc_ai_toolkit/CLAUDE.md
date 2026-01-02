# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GRC AI Toolkit is a foundational Python library for building AI-powered Governance, Risk, and Compliance (GRC) applications. It provides reusable components across five domains: LLM integration, agent framework, data processing, UI components, and sample data generation.

**Target Use Case**: This is a shared foundation module designed to be imported by multiple GRC tool applications (policy generators, risk assessments, compliance automation, etc.).

## Development Commands

### Environment Setup

```bash
# Modern approach with uv (recommended - 10-100x faster)
uv venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
uv pip install -e ".[dev]"

# Traditional approach with pip
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -e ".[dev]"
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=grc_ai_toolkit --cov-report=html

# Run specific test file
pytest tests/test_llm.py

# Run tests with specific marker
pytest -m unit  # Fast unit tests only
pytest -m integration  # Integration tests (requires API keys)

# Run single test
pytest tests/test_llm.py::TestLLMManager::test_generate_simple_prompt
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy grc_ai_toolkit

# Run all quality checks
black . && ruff check . && mypy grc_ai_toolkit && pytest
```

### Environment Configuration

Required `.env` file (copy from `.env.example`):
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
```

## Architecture Overview

### Core Design Patterns

**1. Multi-Provider LLM Abstraction**
- `LLMManager` provides unified interface for OpenAI, Anthropic, and local models
- Automatic fallback: If primary provider fails, switches to fallback provider
- Built-in retry logic with exponential backoff (configurable max_retries)
- Cost tracking happens automatically via tiktoken-based token counting
- Response caching uses LRU cache to reduce API costs

**2. Agent Framework (LangChain 1.0 Patterns)**
- `BaseAgent` uses TypedDict-based state management (not Pydantic classes)
- `AgentState` TypedDict tracks: messages, current_task, context, iteration_count, status, result
- All agents must implement `execute(task, context)` abstract method
- `AgentOrchestrator` coordinates multi-agent workflows with dependency graphs
- Workflow execution uses topological sort for dependency resolution

**3. RAG (Retrieval-Augmented Generation) Architecture**
- `VectorStore` supports both FAISS (in-memory) and ChromaDB (persistent)
- **Critical**: Use k=2 for semantic search (research-proven optimal balance)
- Document chunking uses `RecursiveCharacterTextSplitter` with overlap
- Default chunk_size=1000, chunk_overlap=200 (tuned for LLM context windows)

### Module Responsibilities

**llm/**: LLM provider abstraction layer
- `manager.py`: Core LLMManager class with retry/fallback logic
- `config.py`: Configuration classes and pricing tables (updated Dec 2025)
- `prompts.py`: 6 pre-built GRC prompt templates (policy, risk, compliance, etc.)
- `utils.py`: Token counting (tiktoken) and cost estimation utilities

**agents/**: AI agent framework
- `base.py`: BaseAgent abstract class and AgentConfig dataclass
- `orchestrator.py`: Multi-agent workflow coordination with dependency management
- `templates.py`: Pre-built agents (Research, Analysis, Generation, Review, PolicyDrafting, RiskAssessment)

**data/**: Document processing and vector storage
- `processor.py`: Multi-format document loader (PDF, DOCX, TXT, CSV, HTML)
- `vector_store.py`: FAISS/ChromaDB wrapper for RAG
- `exporters.py`: Export to Markdown, Word, PDF, HTML, Text

**ui/**: Streamlit UI components
- `components.py`: Reusable widgets (metric_card, status_badge, file_uploader, etc.)
- `layouts.py`: Page layout templates (dashboard, wizard, form layouts)
- `forms.py`: GRC-specific forms (policy generation, risk assessment, etc.)

**sample_data/**: Data generators for testing
- `generators.py`: Realistic sample data for risks, policies, incidents, vendors, controls

## Key Implementation Details

### LLM Manager Workflow

1. Config resolution: `LLMConfig.from_env()` reads environment variables
2. Provider initialization: Creates both primary and fallback LLM instances
3. Message building: Converts prompts to LangChain message format (SystemMessage, HumanMessage)
4. Generation with retry:
   - Try primary LLM up to max_retries times with exponential backoff
   - On total failure, attempt fallback LLM if configured
   - Track tokens/cost if `enable_cost_tracking=True`
5. Cache check/save: LRU cache keyed by MD5 hash of message content

### Agent Orchestration Workflow

1. Add workflow steps: `orchestrator.add_step(name, agent, task_template, depends_on=[])`
2. Topological sort: Determine execution order based on dependencies (Kahn's algorithm)
3. Sequential execution:
   - For each step: check condition, verify dependencies satisfied, build task from template
   - Execute agent with retry logic (configurable max_retries)
   - Store result in workflow results dict
4. Return `WorkflowResult` with success status, results, errors, execution_order

### Document Processing Pipeline

1. Load: `DocumentProcessor.load_document()` selects loader by file extension
2. Split: `RecursiveCharacterTextSplitter` with separators `["\n\n", "\n", ". ", " ", ""]`
3. Vector store: Embed with sentence-transformers or OpenAI, store in FAISS/ChromaDB
4. Search: Similarity search with k=2 (optimal per 2025 research)

## Testing Strategy

- **Unit tests**: Fast tests with mocked LLMs (no API calls)
- **Integration tests**: Use `@pytest.mark.integration` and `@pytest.mark.skip()` for CI
- Mock pattern: `@patch('grc_ai_toolkit.llm.manager.ChatOpenAI')` for LLM mocking
- Coverage target: >80% (configured in pyproject.toml)

## Important Constraints

### API Key Management
- **Never hardcode API keys** - always use environment variables
- Load with `python-dotenv`: `load_dotenv()` before creating LLMManager
- Validation: LLMConfig.__post_init__() raises ValueError if provider key missing

### Cost Control
- All LLM calls are tracked via `LLMManager.total_tokens` and `total_cost`
- Use `get_stats()` to monitor usage
- Cache responses when possible (`enable_caching=True` by default)
- Consider using `temperature=0.3-0.5` for deterministic outputs vs `0.7` for creative

### Python Version Compatibility
- Supports Python 3.10-3.14 (recommend 3.11 or 3.12 for stability)
- NumPy version is flexible to support both <2.0 (Py 3.10-3.12) and >=2.0 (Py 3.13-3.14)
- All dependencies managed in `pyproject.toml` with strict version bounds

### LangChain 1.0 Patterns
- Use TypedDict for agent state (not Pydantic BaseModel)
- Use `create_agent` pattern from LangChain 1.0 when building custom agents
- Prefer `with_structured_output()` API for formatted responses
- MemorySaver for conversation memory (if implementing chat agents)

## Common Workflows

### Adding a New Agent Template

1. Create agent class inheriting from `BaseAgent` in `agents/templates.py`
2. Override `execute(task, context)` method
3. Define multi-step process if needed (see PolicyDraftingAgent example)
4. Export in `agents/__init__.py`
5. Add tests in `tests/test_agents.py` (if creating test file)

### Adding a New Prompt Template

1. Add to `PromptLibrary` class in `llm/prompts.py`
2. Define as class attribute: `PromptTemplate(name, template, input_variables, system_message)`
3. Add to `get_template()` method's template_map
4. Add to `list_templates()` return list
5. Test with `template.format(**vars)` to ensure all variables present

### Adding a New Sample Data Generator

1. Create generator class in `sample_data/generators.py`
2. Implement static method `generate_item(id)` and `generate_items(count)`
3. Add to `generate_sample_dataset()` function's generators dict
4. Export in `sample_data/__init__.py`
5. Add tests in `tests/test_sample_data.py`

## Error Handling Patterns

- **LLM failures**: Handled by retry logic in `_generate_with_retry()` (max 3 attempts by default)
- **Missing config**: `LLMConfig.__post_init__()` validates and raises ValueError with clear message
- **Document processing**: `DocumentProcessor` raises ValueError for unsupported file types
- **Agent failures**: Status set to "failed", error stored in state.result

## Performance Considerations

- **Vector search k=2**: Research-proven optimal balance (don't increase unnecessarily)
- **Chunk size 1000**: Tuned for GPT-4 context windows, adjust if using different models
- **Caching**: Enabled by default, use `enable_caching=False` only if fresh responses required
- **Parallel execution**: Use `asyncio` for parallel agent execution (not implemented yet, but planned)
