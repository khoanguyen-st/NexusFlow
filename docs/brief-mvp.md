# NexusFlow AI - MVP Brief (3 Weeks)

**Version:** MVP Core | **Timeline:** 3 weeks | **Team:** 2 Interns

---

## 🎯 MVP Goal

Build an AI system that analyses a codebase and automatically generates an implementation plan for developers.

**Core Value Proposition:** User pastes task description → AI analyses code context → Returns detailed plan

---

## 1. Functional Requirements

### A. Code Indexing & Search

| Feature | Description | Priority |
|---------|-------------|----------|
| Local folder indexing | Scan and index code from a local folder | P0 |
| File embedding | Create vector embedding for each file | P0 |
| Semantic search | Find related files using pgvector | P0 |
| File type filter | Support filtering by extension (.py, .ts, .js, etc.) | P1 |

### B. AI Plan Generation

| Feature | Description | Priority |
|---------|-------------|----------|
| Task analysis | Receive task description, find relevant context | P0 |
| Plan generation | Produce JSON plan with affected files, steps, reusable components | P0 |
| Multiple LLM support | Support OpenAI / Gemini (config via env) | P1 |

### C. Developer Dashboard

| Feature | Description | Priority |
|---------|-------------|----------|
| Project setup | Upload/configure project folder path | P0 |
| Task input | Form for entering task description | P0 |
| Plan display | Show AI‑generated implementation plan | P0 |
| History | View previously generated plans | P1 |

---

## 2. Non‑Functional Requirements

| Requirement | Target |
|-------------|--------|
| Response time | Plan generation < 30 seconds |
| Codebase size | Support projects ≤ 200 files |
| Deployment | Fully Docker‑Compose based |
| Auth | Simple API key (no JWT) |
| Documentation | README with setup guide + demo video |

---

## 3. Tech Stack

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              Vite + TypeScript + TailwindCSS            │
└─────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                      │
│           Python 3.11 + LangChain + Pydantic            │
└─────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL + pgvector                       │
│                  Vector Database                         │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Task Assignment

### AI/Python

| Week | Tasks |
|------|-------|
| 1 | Setup FastAPI, implement file indexing, pgvector embedding |
| 2 | LLM integration, prompt engineering, plan generation API |
| 3 | Testing accuracy, optimise prompts, write API docs |

**Deliverables:**
- `/api/index` – Index project folder
- `/api/search` – Semantic search
- `/api/generate-plan` – Generate implementation plan

---

### FullStack

| Week | Tasks |
|------|-------|
| 1 | Docker Compose setup, PostgreSQL + pgvector, React skeleton |
| 2 | Dashboard UI components, API integration, plan display |
| 3 | Polish UI/UX, README, demo video recording |

**Deliverables:**
- Docker Compose (one‑command setup)
- Dashboard UI with project config + task input + plan view
- Complete README.md

---

### **Collaboration Tasks** (Both)

| Task | Timeline |
|------|----------|
| API contract definition | Days 2‑3, Week 1 |
| Integration testing | Week 2 |
| End‑to‑end testing | Week 3 |
| Demo preparation | End of Week 3 |

---

## 5. Milestones

### ✅ Week 1: Foundation
- [ ] Docker Compose runs (PostgreSQL + pgvector)
- [ ] FastAPI `/health` endpoint works
- [ ] React app renders
- [ ] File indexing API completed

### ✅ Week 2: Core Features
- [ ] Semantic search works
- [ ] Plan generation API completed
- [ ] Dashboard displays AI plan
- [ ] Basic error handling

### ✅ Week 3: Polish & Delivery
- [ ] Test with 2‑3 sample repos
- [ ] Accuracy measurement (target: 70%)
- [ ] Complete README.md
- [ ] Demo video (3‑5 minutes)

---

## 6. Definition of Done

1. ✅ `docker compose up` runs the entire system
2. ✅ User can input a task and receive a plan in < 30 s
3. ✅ AI returns a plan with at least: affected files + implementation steps
4. ✅ Accuracy ≥ 60 % on sample repos (reduced from 70 % for MVP)
5. ✅ README contains setup guide, screenshots, and demo video

---

## 7. Out of Scope (MVP)

The following features will **NOT** be implemented in the MVP:
- ❌ GitHub integration (only local folder)
- ❌ MCP servers
- ❌ Agentic reasoning (auto‑discover additional context)
- ❌ Real‑time Socket.io
- ❌ JWT authentication
- ❌ AWS deployment
- ❌ Knowledge base upload
- ❌ Interactive plan editing

---

## 8. API Contract (Draft)

### Index Project
```
POST /api/index
Content-Type: application/json

{
  "project_path": "/path/to/project",
  "extensions": [".py", ".ts", ".js"]
}
```

### Search
```
POST /api/search
Content-Type: application/json

{
  "query": "user authentication",
  "top_k": 10
}
```

### Generate Plan
```
POST /api/generate-plan
Content-Type: application/json

{
  "task": "Add forgot password feature to the auth module",
  "project_id": "uuid-here"
}
```

### Response Format
```json
{
  "plan": {
    "summary": "Implement forgot password flow",
    "affected_files": [
      {"path": "src/auth/routes.py", "action": "modify"},
      {"path": "src/auth/email.py", "action": "create"}
    ],
    "steps": [
      {"order": 1, "description": "Create email service", "file": "src/auth/email.py"},
      {"order": 2, "description": "Add reset password endpoint", "file": "src/auth/routes.py"}
    ],
    "reusable_components": [
      {"name": "send_email()", "location": "src/utils/mailer.py"}
    ]
  },
  "context_used": ["src/auth/routes.py", "src/models/user.py"],
  "confidence": 0.85
}
```

---

## 9. Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM API rate limit | Slower development | Use caching, mock responses |
| Embedding cost | High expense | Limit file size, batch processing |
| Integration issues | Timeline delays | Daily sync meetings, clear API contract |
| Low accuracy | Failure to meet DoD | Iterative prompt improvement |

---

**Document created:** 2026-01-11
**Last updated:** 2026-01-11
**Owner:** Khoa Nguyen (Mentor)
