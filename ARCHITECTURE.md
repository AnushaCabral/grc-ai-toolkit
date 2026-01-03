# GRC AI Tools - Architecture

## System Overview

**Monorepo containing:**
- Shared foundation library (`grc_ai_toolkit`)
- 5 specialized GRC tools (specifications + implementations)

## Architecture Layers

### Layer 1: Shared Foundation (`grc_ai_toolkit/`)

**Purpose:** Reusable components for all tools

**Components:**

- **LLM Integration** (`llm/`)
  - Unified interface for OpenAI, Anthropic, and Groq
  - Automatic fallback mechanisms
  - Token management and cost tracking
  - Response caching (LRU cache)

- **Agent Framework** (`agents/`)
  - Multi-agent orchestration
  - TypedDict-based state management (LangChain 1.0)
  - Pre-built agent templates
  - Workflow dependency management

- **Data Processing** (`data/`)
  - RAG with FAISS (in-memory) and ChromaDB (persistent)
  - Multi-format document loader (PDF, DOCX, TXT, CSV, HTML)
  - Semantic search with k=2 (research-optimized)
  - Export capabilities (Markdown, Word, PDF, HTML)

- **UI Components** (`ui/`)
  - Streamlit widget library
  - Reusable page layouts
  - GRC-specific forms
  - Consistent styling

- **Sample Data** (`sample_data/`)
  - Test data generators
  - Realistic GRC scenarios
  - Development and testing utilities

### Layer 2: Tool Applications (Future)

Each tool uses the shared foundation:

1. **GRC Content Creator** - AI-powered policy and procedure document generation
2. **TPRM Platform** - Third-party risk management and vendor assessment
3. **Compliance Monitor** - Automated regulatory compliance tracking
4. **Risk Analyzer** - Risk assessment and predictive analytics
5. **Audit Assistant** - AI-powered document review and evidence analysis

## Technology Stack

### Core Technologies

- **Python 3.10+** - Primary programming language
- **LangChain 1.0+** - Agent framework and orchestration
- **Streamlit** - Interactive web UI
- **FastAPI** - REST API backend (future)

### LLM Providers

- **OpenAI** - GPT-4, GPT-3.5-turbo
- **Anthropic** - Claude Sonnet 4.5
- **Groq** - Fast inference engine

### Vector Stores

- **FAISS** - In-memory vector search (local development)
- **ChromaDB** - Persistent vector database (production)

### Testing & Quality

- **pytest** - Unit and integration testing
- **pytest-cov** - Code coverage tracking
- **black** - Code formatting
- **ruff** - Fast Python linter
- **mypy** - Static type checking

## Design Principles

### 1. Shared Foundation
- All tools import from common `grc_ai_toolkit` library
- Changes to foundation immediately available to all tools
- No version mismatch issues

### 2. Modular Design
- Tools are independent applications
- Can be deployed separately or together
- Shared components via library imports

### 3. Multi-LLM Support
- Provider-agnostic design
- Easy to switch between OpenAI, Anthropic, Groq
- Automatic fallback on failures

### 4. Test-Driven Development
- Comprehensive test coverage (>80% target)
- Mock-based unit tests (no API calls)
- Integration tests for end-to-end workflows

### 5. Monorepo Structure
- Single repository for all components
- Unified version control
- Simplified CI/CD pipeline

## Deployment Model

### Development Environment

```
grc-ai-toolkit/
├── .venv/                   # Virtual environment
├── grc_ai_toolkit/          # Foundation library
└── tool1_*/                 # Tool implementations
```

**Setup:**
```bash
cd grc-ai-toolkit
python -m venv .venv
.venv\Scripts\activate
pip install -e grc_ai_toolkit/
```

### Production Deployment (Future)

**Option A: Monolithic Deployment**
- Deploy all tools together
- Single server/container
- Shared resources

**Option B: Separate Deployments**
- Each tool as independent service
- Foundation library installed in each
- Horizontal scaling

**Option C: Hybrid Approach**
- Shared foundation as Python package
- Tools deployed separately
- Best of both worlds

## Data Flow

### Basic Flow

1. **User Input** → Streamlit UI
2. **UI** → Agent Framework
3. **Agent** → LLM Provider (OpenAI/Anthropic/Groq)
4. **LLM Response** → RAG Pipeline (optional)
5. **Results** → UI Display

### RAG-Enhanced Flow

1. **User Query** → Document Processor
2. **Documents** → Text Chunking
3. **Chunks** → Vector Embeddings
4. **Embeddings** → Vector Store (FAISS/ChromaDB)
5. **Query** → Semantic Search (k=2)
6. **Retrieved Context** → LLM Prompt
7. **LLM Response** → UI Display

## Security

### API Key Management
- All keys stored in `.env` file (gitignored)
- Loaded via `python-dotenv`
- Never hardcoded in source
- Validation on startup

### Data Protection
- Sensitive tracking data in `.private/` folder (gitignored)
- No business-sensitive data in repository
- Local-only project status and planning

### Access Control
- API keys per user/environment
- No shared credentials
- Environment-specific configuration

## Performance Considerations

### LLM Optimization
- Response caching (LRU cache)
- Token counting for cost tracking
- Retry logic with exponential backoff
- Automatic fallback providers

### Vector Search
- k=2 for semantic search (research-proven optimal)
- Chunk size = 1000 tokens
- Chunk overlap = 200 tokens
- Efficient similarity algorithms

### Cost Control
- Track all API calls
- Monitor token usage
- Use caching to reduce calls
- Temperature tuning (0.3-0.7)

## Scalability

### Current State (Single User)
- Local development environment
- In-memory vector stores
- File-based data storage

### Future State (Multi-User)
- PostgreSQL for structured data
- Persistent vector databases (ChromaDB/Pinecone)
- Distributed caching (Redis)
- Load balancing across LLM providers

## Monitoring & Observability

### Current (Development)
- Console logging
- Pytest test results
- Coverage reports

### Future (Production)
- Structured logging
- Application metrics (Prometheus)
- Error tracking (Sentry)
- LLM usage dashboards

## Development Workflow

### Adding a New Tool

1. Create tool directory: `tool{N}_{name}/`
2. Import foundation: `from grc_ai_toolkit import ...`
3. Implement UI using Streamlit components
4. Use agent framework for orchestration
5. Add tests in `tests/`
6. Update documentation

### Modifying Foundation

1. Make changes in `grc_ai_toolkit/`
2. Run tests: `pytest`
3. Update version if needed
4. Changes immediately available to all tools

## Future Enhancements

### Phase 1 (Current)
- ✅ Foundation library complete
- ✅ Testing infrastructure
- ✅ Documentation

### Phase 2 (Next)
- Implement Tool 1 (GRC Content Creator)
- CI/CD pipeline (GitHub Actions)
- Documentation site

### Phase 3 (Future)
- Implement Tools 2-5
- Multi-user support
- Cloud deployment
- API endpoints

## References

- **Installation:** See `grc_ai_toolkit/INSTALL.md` or `INSTALL_UV.md`
- **Developer Guide:** See `grc_ai_toolkit/CLAUDE.md`
- **Consolidation:** See `CONSOLIDATION.md`
- **Tool 1 Spec:** See `tool1_grc_content_creator_spec.md`

---

**Last Updated:** January 2026
**Status:** Foundation Complete, Tools In Planning
