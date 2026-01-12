# NexusFlow AI

AI-powered code analysis and implementation planning for developers.

## 🚀 Overview

NexusFlow AI is a smart task management system that automatically analyzes your codebase and generates detailed implementation plans. It uses vector embeddings and LLM to understand your code context and provide actionable steps for new features.

## ✨ Features

- **Code Indexing**: Automatically scan and index your codebase with vector embeddings
- **Semantic Search**: Find relevant files using natural language queries
- **AI Plan Generation**: Get detailed implementation plans with affected files and steps
- **Modern Dashboard**: Beautiful UI to manage projects and view plans

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, Python 3.11, LangChain |
| Frontend | React 18, TypeScript, Tailwind CSS |
| Database | PostgreSQL with pgvector |
| AI | OpenAI / Gemini |
| Deployment | Docker Compose |

## 📋 Prerequisites

- Docker & Docker Compose
- OpenAI API key (or Gemini API key)

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-org/nexusflow-ai.git
cd nexusflow-ai
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
OPENAI_API_KEY=sk-your-api-key-here
# Or use Gemini
# LLM_PROVIDER=gemini
# GEMINI_API_KEY=your-gemini-key
```

### 3. Start the application

```bash
docker compose up --build
```

### 4. Access the app

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
nexusflow-ai/
├── docker-compose.yml      # Container orchestration
├── .env.example            # Environment template
│
├── backend/                # FastAPI backend
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py         # FastAPI app entry
│       ├── config.py       # Settings
│       ├── database.py     # DB connection
│       ├── schemas.py      # Pydantic models
│       ├── models/         # SQLAlchemy models
│       ├── routers/        # API endpoints
│       └── services/       # Business logic
│           ├── indexer.py  # File indexing
│           ├── embedder.py # Vector embeddings
│           ├── searcher.py # Semantic search
│           └── planner.py  # AI plan generation
│
├── frontend/               # React frontend
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── App.tsx
│       ├── components/
│       ├── pages/
│       └── services/
│
└── docs/                   # Documentation
    ├── brief-mvp.md
    └── task.md
```

## 🔌 API Endpoints

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | List all projects |
| POST | `/api/projects` | Create a project |
| GET | `/api/projects/{id}` | Get project details |
| DELETE | `/api/projects/{id}` | Delete a project |
| POST | `/api/projects/{id}/index` | Start indexing |

### Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/search` | Semantic search |

### Plans

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/plans/generate` | Generate implementation plan |
| GET | `/api/plans/{id}` | Get plan details |
| GET | `/api/plans/project/{id}` | List plans by project |

## 🔧 Development

### Backend only

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend only

```bash
cd frontend
npm install
npm run dev
```

## 📊 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Database user | nexusflow |
| `POSTGRES_PASSWORD` | Database password | nexusflow123 |
| `POSTGRES_DB` | Database name | nexusflow |
| `LLM_PROVIDER` | LLM provider (openai/gemini) | openai |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `GEMINI_API_KEY` | Gemini API key | - |

## 📝 License

MIT License

---

Built with ❤️ by NexusFlow Team
