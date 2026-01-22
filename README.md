# NexusFlow AI - Intern Training Project

> **🎓 Educational Project for Interns**
> This is a starter template for building an AI-powered code analysis and implementation planning system.

## 📚 Learning Objectives

By completing this project, you will learn:

- Building full-stack applications with FastAPI and React
- Working with vector embeddings and pgvector
- Integrating LLM APIs (OpenAI/Gemini)
- Docker containerization
- Modern UI development with React and TailwindCSS

## 🎯 Your Mission

Build an AI system that:

1. **Indexes codebases** - Scans files and creates vector embeddings
2. **Semantic search** - Finds relevant code using natural language
3. **Generates plans** - Uses AI to create implementation plans for new features

## 🛠️ Tech Stack

| Layer      | Technology                                 |
| ---------- | ------------------------------------------ |
| Backend    | FastAPI, Python 3.11                       |
| Frontend   | React 18, TypeScript, Vite, Tailwind CSS   |
| Database   | PostgreSQL with pgvector                   |
| AI         | OpenAI API (text-embedding-3-small, GPT-4) |
| Deployment | Docker Compose                             |

## 📋 Prerequisites

- Docker & Docker Compose installed
- OpenAI API key (get it from https://platform.openai.com/)
- Basic knowledge of Python and React
- Text editor (VS Code recommended)

## 🚀 Getting Started

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd NexusFlow
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Start the Application

```bash
docker compose up --build
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📝 Task Breakdown

Your implementation tasks are detailed in [`docs/task.md`](docs/task.md). Follow the 3-week timeline:

**📖 Important Guides:**

- **API Setup**: See [`docs/api_guide.md`](docs/api_guide.md) for detailed API implementation guide
- **Task Breakdown**: See [`docs/task.md`](docs/task.md) for weekly tasks

### Week 1: Foundation (Days 1-5)

- ✅ Project structure (already done)
- ✅ Docker setup (already done)
- ✅ Database schema (already done)
- 🔨 **YOUR TASKS:**
  - **Setup API endpoints** - Uncomment code in `backend/app/routers/` (see api_guide.md)
  - **Setup frontend API client** - Uncomment code in `frontend/src/services/api.ts`
  - Implement file indexing service
  - Create embedding generation
  - Build basic UI components

### Week 2: Core Features (Days 6-10)

- 🔨 **YOUR TASKS:**
  - Complete vector search functionality
  - Integrate OpenAI LLM
  - Build plan generation service
  - Create dashboard pages

### Week 3: Polish & Delivery (Days 11-15)

- 🔨 **YOUR TASKS:**
  - End-to-end testing
  - Error handling
  - Performance optimization
  - Documentation

## 🗂️ Project Structure

```
NexusFlow/
├── backend/
│   └── app/
│       ├── main.py          # FastAPI entry point
│       ├── services/        # TODO: Implement these!
│       │   ├── indexer.py   # File scanning & indexing
│       │   ├── embedder.py  # Vector embeddings
│       │   ├── searcher.py  # Semantic search
│       │   └── planner.py   # AI plan generation
│       └── routers/         # API endpoints (partially done)
│
├── frontend/
│   └── src/
│       ├── pages/           # TODO: Complete these!
│       │   ├── Projects.tsx # Project management
│       │   ├── TaskInput.tsx # Task description input
│       │   └── PlanView.tsx  # Display generated plans
│       └── services/
│           └── api.ts       # API client (done)
│
├── docker/
│   └── init.sql            # Database schema (done)
├── docker-compose.yml      # Container setup (done)
└── docs/
    └── task.md            # 📖 YOUR GUIDE - Read this!
```

## 🔍 Where to Start?

1. **Read the task breakdown**: Open [`docs/task.md`](docs/task.md) and read through all tasks
2. **Look for TODOs**: Search for `TODO` comments in the codebase - these mark what needs implementation
3. **Start with Week 1**: Follow the sequential order in task.md
4. **Test frequently**: Use the API docs at http://localhost:8000/docs to test your endpoints

## 📖 Key Files to Understand

### Backend API Endpoints (Need to uncomment!)

- **`backend/app/routers/projects.py`** - TODO: Uncomment and implement CRUD endpoints
- **`backend/app/routers/search.py`** - TODO: Uncomment search endpoint
- **`backend/app/routers/plans.py`** - TODO: Uncomment plan generation endpoints

📘 **See [`docs/api_guide.md`](docs/api_guide.md) for complete API implementation guide!**

### Backend Services (Need to implement!)

- **`backend/app/services/indexer.py`** - TODO: Implement file scanning and indexing
- **`backend/app/services/embedder.py`** - TODO: Generate vector embeddings using OpenAI
- **`backend/app/services/searcher.py`** - TODO: Implement semantic search with pgvector
- **`backend/app/services/planner.py`** - TODO: Create LLM-powered plan generation

### Frontend (Need to implement!)

- **`frontend/src/services/api.ts`** - TODO: Uncomment axios setup and API functions
- **`frontend/src/pages/Projects.tsx`** - TODO: Build project management UI
- **`frontend/src/pages/TaskInput.tsx`** - TODO: Create task input form
- **`frontend/src/pages/PlanView.tsx`** - TODO: Display generated implementation plans

## 🔧 How to Start Implementing

### Step 1: Setup APIs First (Week 1, Day 1-2)

**Backend:**

1. Open `backend/app/routers/projects.py`
2. Uncomment the endpoint functions (they have examples in comments)
3. Add missing imports at the top
4. Test each endpoint at http://localhost:8000/docs

**Frontend:**

1. Open `frontend/src/services/api.ts`
2. Uncomment the axios setup
3. Uncomment all API functions (projectsApi, searchApi, plansApi)
4. Save and check for TypeScript errors

📖 **Follow the detailed guide in [`docs/api_guide.md`](docs/api_guide.md)**

### Step 2: Implement Services (Week 1-2)

Follow the TODO comments in:

- `backend/app/services/indexer.py`
- `backend/app/services/embedder.py`
- `backend/app/services/searcher.py`
- `backend/app/services/planner.py`

### Step 3: Build UI (Week 2)

Complete the React pages using the API functions you set up.

## 🧪 Testing Your Implementation

###**Read [`docs/api_guide.md`](docs/api_guide.md)** - Complete API setup guide with examples 2. Test Backend APIs

Visit http://localhost:8000/docs and try:

1. Create a project via `/api/projects`
2. Index a project via `/api/projects/{id}/index`
3. Search for files via `/api/search`
4. Generate a plan via `/api/plans/generate`

**Note:** Initially most endpoints will return 404 until you uncomment them!

### Test Frontend

Visit http://localhost:5173 and:

1. Create a new project
2. Click "Index" to scan files
3. Navigate to "Generate Plan"
4. Enter a task description
5. View the generated plan

## 💡 Tips & Resources

### Learning Resources

- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **React Docs**: https://react.dev/learn
- **OpenAI API**: https://platform.openai.com/docs/api-reference
- **pgvector Guide**: https://github.com/pgvector/pgvector

### Common Issues

- **API key not working**: Make sure `.env` file has correct `OPENAI_API_KEY`
- **Database errors**: Check if postgres container is running: `docker compose ps`
- **Port conflicts**: Make sure ports 5173, 8000, 5432 are available

### Getting Help

1. **Read [`docs/api_guide.md`](docs/api_guide.md)** - Complete API setup guide with examples
2. Check the TODO comments in code - they have hints
3. Review the API documentation at http://localhost:8000/docs
4. Look at the database schema in `docker/init.sql`
5. Ask your mentor when stuck!

## ✅ Completion Checklist

Track your progress:

**Week 1: Setup & Foundation**

- [ ] Uncommented all backend API endpoints
- [ ] Uncommented frontend API client
- [ ] All endpoints work in FastAPI docs
- [ ] Can create and list projects via API
- [ ] File indexing service implemented

**Week 2: Core Features**

- [ ] Vector embeddings generated
- [ ] Semantic search returns results
- [ ] LLM generates plans
- [ ] Frontend can call all APIs

**Week 3: Polish & Testing**

- [ ] UI fully functional
- [ ] Error handling complete
- [ ] Can demo end-to-end flow

## 🎓 What You'll Learn

By the end of this project, you will have hands-on experience with:

- ✅ REST API development with FastAPI
- ✅ Async Python programming
- ✅ Vector databases and embeddings
- ✅ LLM integration and prompt engineering
- ✅ Modern React with hooks and TypeScript
- ✅ Docker containerization
- ✅ Full-stack application architecture

## 📞 Support

If you get stuck:

1. **Start with the guides:**
   - [`docs/api_guide.md`](docs/api_guide.md) - Complete API implementation guide
   - [`docs/task.md`](docs/task.md) - Weekly task breakdown
2. Check TODO comments in the code
3. Test endpoints at http://localhost:8000/docs
4. Check browser DevTools Network tab for API errors
5. Ask your mentor for guidance

**Good luck! 🚀 You've got this!**

````

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
````

### Frontend only

```bash
cd frontend
npm install
npm run dev
```

## 📊 Environment Variables

| Variable            | Description                  | Default      |
| ------------------- | ---------------------------- | ------------ |
| `POSTGRES_USER`     | Database user                | nexusflow    |
| `POSTGRES_PASSWORD` | Database password            | nexusflow123 |
| `POSTGRES_DB`       | Database name                | nexusflow    |
| `LLM_PROVIDER`      | LLM provider (openai/gemini) | openai       |
| `OPENAI_API_KEY`    | OpenAI API key               | -            |
| `GEMINI_API_KEY`    | Gemini API key               | -            |

## 📝 License

MIT License

---

Built with ❤️ by NexusFlow Team
