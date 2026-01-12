# NexusFlow AI - Task Breakdown

> **Timeline:** 3 Weeks (15 working days)
> **Reference:** [brief-mvp.en.md](./brief-mvp.en.md)

---

## Week 1: Foundation (Day 1-5)

### 1.1 Project Setup & Infrastructure

- [ ] **Initialize monorepo structure**
  - Create `/backend` folder (FastAPI)
  - Create `/frontend` folder (React + Vite)
  - Create `/docker` folder for Docker configs
  - Set up `.gitignore`, `.env.example`

- [ ] **Docker Compose configuration**
  - Create `docker-compose.yml` with 3 services: `api`, `web`, `db`
  - Set up PostgreSQL container with pgvector extension
  - Configure volume mounts for persistent data
  - Verify `docker compose up` runs successfully

- [ ] **Database setup**
  - Create database schema for projects table
  - Create schema for file_embeddings table
  - Enable pgvector extension
  - Test vector operations (insert + similarity search)

### 1.2 Backend Foundation

- [ ] **FastAPI project structure**
  - Set up FastAPI app with uvicorn
  - Configure CORS middleware
  - Set up Pydantic models for request/response
  - Create `/health` endpoint
  - Set up environment variables handling

- [ ] **Database connection**
  - Set up SQLAlchemy / asyncpg connection
  - Create database models (Project, FileEmbedding)
  - Set up Alembic migrations (optional)
  - Test database CRUD operations

- [ ] **File Indexing Service**
  - Implement file scanner (walk directory)
  - Filter by extensions (.py, .ts, .js, .tsx, .jsx, .md)
  - Read file content with proper encoding handling
  - Implement chunking strategy (by file or by function)
  - Create `POST /api/index` endpoint

### 1.3 Frontend Foundation

- [ ] **React project setup**
  - Initialize Vite + React + TypeScript
  - Set up TailwindCSS
  - Configure path aliases (`@/components`, etc.)
  - Set up basic routing (react-router-dom)

- [ ] **UI Layout**
  - Create main layout component
  - Create sidebar navigation
  - Create header component
  - Set up dark/light theme (optional)

- [ ] **API client setup**
  - Create axios/fetch wrapper
  - Set up base URL from environment
  - Create API error handling
  - Set up loading states pattern

---

## Week 2: Core Features (Day 6-10)

### 2.1 Embedding & Vector Search

- [ ] **Embedding service**
  - Integrate OpenAI Embeddings API (text-embedding-3-small)
  - Implement batch embedding (multiple files at once)
  - Store embeddings in pgvector
  - Handle API rate limiting
  - Add embedding caching to avoid re-processing

- [ ] **Semantic search**
  - Implement vector similarity search
  - Create `POST /api/search` endpoint
  - Return top‑k results with similarity scores
  - Add metadata filtering (by project, by extension)

- [ ] **Indexing flow completion**
  - Connect file scanner → embedding → storage
  - Add progress tracking (files indexed / total)
  - Handle large projects (batch processing)
  - Add error handling for failed files

### 2.2 AI Plan Generation

- [ ] **LLM Integration**
  - Set up OpenAI / Gemini client
  - Create prompt templates
  - Implement structured output parsing (JSON)
  - Add retry logic for API failures

- [ ] **Plan generation service**
  - Implement context retrieval (search relevant files)
  - Build prompt with task + context
  - Parse LLM response into structured plan
  - Create `POST /api/generate-plan` endpoint

- [ ] **Plan schema**
  - Define Pydantic model for Plan response
  - Include: summary, affected_files, steps, reusable_components
  - Include: context_used, confidence score
  - Validate response format

### 2.3 Dashboard UI

- [ ] **Project Management Page**
  - Create project list view
  - Create "Add Project" form (path input)
  - Show indexing status per project
  - Add delete project functionality

- [ ] **Task Input Page**
  - Create task description textarea
  - Project selector dropdown
  - "Generate Plan" button
  - Loading state while generating

- [ ] **Plan Display Page**
  - Display plan summary
  - List affected files with action badges (create/modify/delete)
  - Display implementation steps as checklist
  - Show reusable components section
  - Display confidence score
  - Show context files used

---

## Week 3: Polish & Delivery (Day 11-15)

### 3.1 Integration & Testing

- [ ] **End‑to‑end flow testing**
  - Test: Add project → Index → Search → Generate plan
  - Fix integration bugs
  - Test with real codebases (2‑3 sample repos)

- [ ] **Error handling**
  - Add proper error messages in API
  - Display user‑friendly errors in UI
  - Handle edge cases (empty project, no results, etc.)
  - Add input validation

- [ ] **Performance optimization**
  - Optimize embedding batch size
  - Add request timeouts
  - Optimize database queries
  - Test response time < 30 s

### 3.2 Accuracy & Quality

- [ ] **Prompt engineering**
  - Iterate on system prompt
  - Test different context window sizes
  - Add few‑shot examples if needed
  - Document prompt versions

- [ ] **Accuracy testing**
  - Create test cases with expected outputs
  - Measure accuracy on sample repos (target: ≥60%)
  - Document results
  - Identify improvement areas

### 3.3 Documentation

- [ ] **README.md**
  - Project overview
  - Tech stack description
  - Prerequisites (Docker, API keys)
  - Quick start guide (`docker compose up`)
  - Environment variables reference
  - UI screenshots

- [ ] **API Documentation**
  - Enable FastAPI Swagger UI
  - Document all endpoints
  - Add request/response examples
  - Document error codes

- [ ] **Demo video**
  - Record 3‑5 minute walkthrough
  - Show: setup → index → generate plan
  - Upload to YouTube/Loom
  - Add link to README

### 3.4 Final Delivery

- [ ] **Code cleanup**
  - Remove debug logs
  - Add code comments where needed
  - Ensure consistent code style
  - Run linter (ruff, eslint)

- [ ] **Environment setup**
  - Verify `.env.example` is complete
  - Test fresh clone → setup → run
  - Document all required API keys

- [ ] **Final checklist**
  - All milestones achieved
  - Docker Compose works with single command
  - README is complete
  - Demo video is recorded
  - Code is pushed to main branch

---

## Appendix: File Structure (Reference)

```
 nexusflow-ai/
 ├── docker-compose.yml
 ├── .env.example
 ├── README.md
 │
 ├── backend/
 │   ├── Dockerfile
 │   ├── requirements.txt
 │   ├── app/
 │   │   ├── main.py
 │   │   ├── config.py
 │   │   ├── database.py
 │   │   ├── models/
 │   │   │   ├── project.py
 │   │   │   └── embedding.py
 │   │   ├── services/
 │   │   │   ├── indexer.py
 │   │   │   ├── embedder.py
 │   │   │   ├── searcher.py
 │   │   │   └── planner.py
 │   │   ├── routers/
 │   │   │   ├── index.py
 │   │   │   ├── search.py
 │   │   │   └── plan.py
 │   │   └── prompts/
 │   │       └── plan_generation.txt
 │   └── tests/
 │
 ├── frontend/
 │   ├── Dockerfile
 │   ├── package.json
 │   ├── src/
 │   │   ├── App.tsx
 │   │   ├── main.tsx
 │   │   ├── components/
 │   │   ├── pages/
 │   │   │   ├── Projects.tsx
 │   │   │   ├── TaskInput.tsx
 │   │   │   └── PlanView.tsx
 │   │   ├── services/
 │   │   │   └── api.ts
 │   │   └── styles/
 │   └── index.html
 │
 └── docs/
     ├── brief-mvp.en.md
     └── task.en.md
```
