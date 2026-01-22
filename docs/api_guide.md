# API Setup Guide

> **📖 Complete guide for setting up backend and frontend APIs**

This guide will help you implement all API endpoints and connect frontend to backend.

---

## 🎯 Overview

You need to implement:
1. **Backend API endpoints** (FastAPI routers)
2. **Frontend API client** (Axios wrapper)
3. **Connect them together**

---

## 📂 Backend API Endpoints (FastAPI)

### Location: `backend/app/routers/`

### Step 1: Understand FastAPI Basics

FastAPI uses **decorators** to define endpoints:

```python
@router.get("/endpoint")           # GET request
@router.post("/endpoint")          # POST request
@router.put("/endpoint")           # PUT request
@router.delete("/endpoint")        # DELETE request
```

**Path parameters**: `@router.get("/items/{item_id}")`
**Query parameters**: Function arguments
**Request body**: Pydantic models

### Step 2: Projects API (`projects.py`)

Implement these endpoints:

#### 1. List all projects
```python
@router.get("", response_model=list[ProjectResponse])
async def list_projects(db: AsyncSession = Depends(get_db)):
    """
    GET /api/projects
    Returns: List of all projects
    """
    from sqlalchemy import select
    from app.models import Project
    
    result = await db.execute(
        select(Project).order_by(Project.created_at.desc())
    )
    projects = result.scalars().all()
    return projects
```

#### 2. Create new project
```python
@router.post("", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /api/projects
    Body: { name, path, description? }
    Returns: Created project
    """
    from app.models import Project
    
    new_project = Project(
        name=project.name,
        path=project.path,
        description=project.description,
        status="pending",
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project
```

#### 3. Get project by ID
```python
@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    GET /api/projects/{id}
    Returns: Single project or 404
    """
    from sqlalchemy import select
    from app.models import Project
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project
```

#### 4. Delete project
```python
@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    DELETE /api/projects/{id}
    Returns: Success message
    """
    from sqlalchemy import select
    from app.models import Project
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await db.delete(project)
    await db.commit()
    
    return {"message": "Project deleted successfully"}
```

#### 5. Index project (Background task)
```python
@router.post("/{project_id}/index", response_model=IndexResponse)
async def index_project(
    project_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /api/projects/{id}/index
    Starts indexing in background
    Returns: Status message
    """
    from sqlalchemy import select
    from app.models import Project
    from app.services.indexer import IndexerService
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update status
    project.status = "indexing"
    await db.commit()
    
    # Run in background
    indexer = IndexerService()
    background_tasks.add_task(indexer.index_project, project_id, project.path)
    
    return IndexResponse(
        project_id=project_id,
        status="indexing",
        files_indexed=0,
        message="Indexing started in background",
    )
```

### Step 3: Search API (`search.py`)

```python
@router.post("", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /api/search
    Body: { project_id, query, top_k? }
    Returns: List of similar files
    """
    from app.services.searcher import SearcherService
    
    searcher = SearcherService(db)
    
    try:
        results = await searcher.search(
            project_id=request.project_id,
            query=request.query,
            top_k=request.top_k,
        )
        
        return SearchResponse(
            query=request.query,
            results=results,
            total=len(results),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Step 4: Plans API (`plans.py`)

#### 1. Generate plan
```python
@router.post("/generate", response_model=PlanResponse)
async def generate_plan(
    request: PlanGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /api/plans/generate
    Body: { project_id, task }
    Returns: Generated implementation plan
    """
    from app.services.planner import PlannerService
    
    planner = PlannerService(db)
    
    try:
        plan = await planner.generate_plan(
            project_id=request.project_id,
            task=request.task,
        )
        return plan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### 2. Get plan by ID
```python
@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    GET /api/plans/{id}
    Returns: Plan details
    """
    from sqlalchemy import select
    from app.models import Plan
    
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    from app.schemas import PlanData
    return PlanResponse(
        id=plan.id,
        project_id=plan.project_id,
        task_description=plan.task_description,
        plan=PlanData(**plan.plan_data),
        context_used=plan.context_files or [],
        confidence=plan.confidence or 0.0,
        created_at=plan.created_at,
    )
```

#### 3. List plans for project
```python
@router.get("/project/{project_id}", response_model=list[PlanResponse])
async def list_project_plans(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    GET /api/plans/project/{project_id}
    Returns: All plans for a project
    """
    from sqlalchemy import select
    from app.models import Plan
    from app.schemas import PlanData
    
    result = await db.execute(
        select(Plan)
        .where(Plan.project_id == project_id)
        .order_by(Plan.created_at.desc())
    )
    plans = result.scalars().all()
    
    return [
        PlanResponse(
            id=p.id,
            project_id=p.project_id,
            task_description=p.task_description,
            plan=PlanData(**p.plan_data),
            context_used=p.context_files or [],
            confidence=p.confidence or 0.0,
            created_at=p.created_at,
        )
        for p in plans
    ]
```

---

## 🎨 Frontend API Client (Axios)

### Location: `frontend/src/services/api.ts`

### Step 1: Setup Axios Instance

```typescript
import axios from 'axios'

// Get API URL from environment or use default
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance with base config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
```

### Step 2: Define TypeScript Interfaces

These should match your Pydantic models from backend:

```typescript
export interface Project {
  id: string
  name: string
  path: string
  description: string | null
  status: string
  file_count: number
  indexed_at: string | null
  created_at: string
  updated_at: string
}

export interface SearchResult {
  file_path: string
  file_name: string
  content: string
  similarity: number
}

export interface Plan {
  id: string
  project_id: string
  task_description: string
  plan: {
    summary: string
    affected_files: AffectedFile[]
    steps: ImplementationStep[]
    reusable_components: ReusableComponent[]
  }
  context_used: string[]
  confidence: number
  created_at: string
}
```

### Step 3: Create API Functions

Group related endpoints together:

```typescript
// Projects API
export const projectsApi = {
  // List all projects
  list: () => api.get<Project[]>('/api/projects'),
  
  // Get project by ID
  get: (id: string) => api.get<Project>(`/api/projects/${id}`),
  
  // Create new project
  create: (data: { name: string; path: string; description?: string }) =>
    api.post<Project>('/api/projects', data),
  
  // Delete project
  delete: (id: string) => api.delete(`/api/projects/${id}`),
  
  // Start indexing
  index: (id: string) => api.post(`/api/projects/${id}/index`),
}

// Search API
export const searchApi = {
  search: (data: { project_id: string; query: string; top_k?: number }) =>
    api.post<{ query: string; results: SearchResult[]; total: number }>(
      '/api/search',
      data
    ),
}

// Plans API
export const plansApi = {
  generate: (data: { project_id: string; task: string }) =>
    api.post<Plan>('/api/plans/generate', data),
  
  get: (id: string) => api.get<Plan>(`/api/plans/${id}`),
  
  listByProject: (projectId: string) =>
    api.get<Plan[]>(`/api/plans/project/${projectId}`),
}
```

---

## 🔗 Using APIs in React Components

### Example: Loading Projects

```typescript
import { useState, useEffect } from 'react'
import { projectsApi, Project } from '../services/api'

function Projects() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    try {
      const response = await projectsApi.list()
      setProjects(response.data)
    } catch (error) {
      console.error('Failed to load projects:', error)
    } finally {
      setLoading(false)
    }
  }

  // ... rest of component
}
```

### Example: Creating a Project

```typescript
const handleCreate = async (e: React.FormEvent) => {
  e.preventDefault()
  try {
    await projectsApi.create({
      name: formData.name,
      path: formData.path,
      description: formData.description,
    })
    loadProjects() // Reload list
  } catch (error) {
    console.error('Failed to create project:', error)
  }
}
```

### Example: Generating a Plan

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  setLoading(true)
  
  try {
    const response = await plansApi.generate({
      project_id: projectId,
      task: task,
    })
    navigate(`/plan/${response.data.id}`)
  } catch (error) {
    console.error('Failed to generate plan:', error)
  } finally {
    setLoading(false)
  }
}
```

---

## 🧪 Testing Your APIs

### 1. Backend Testing (FastAPI Docs)

Visit http://localhost:8000/docs

You'll see an interactive API documentation where you can:
- See all endpoints
- Try them out directly
- View request/response schemas

**Test flow:**
1. POST `/api/projects` - Create a project
2. POST `/api/projects/{id}/index` - Start indexing
3. POST `/api/search` - Search for files
4. POST `/api/plans/generate` - Generate a plan

### 2. Frontend Testing (Browser)

Visit http://localhost:5173

Test the complete user flow:
1. Create a project
2. Click "Index" button
3. Wait for indexing to complete
4. Click "Generate Plan"
5. Enter task description
6. View generated plan

### 3. Network Debugging

Open browser DevTools → Network tab to:
- See all API requests
- Check request/response data
- Debug errors

---

## 💡 Common Patterns

### Error Handling

**Backend:**
```python
if not project:
    raise HTTPException(status_code=404, detail="Project not found")
```

**Frontend:**
```typescript
try {
  const response = await projectsApi.get(id)
  return response.data
} catch (error) {
  if (axios.isAxiosError(error)) {
    console.error('API Error:', error.response?.data)
  }
}
```

### Loading States

```typescript
const [loading, setLoading] = useState(false)

const fetchData = async () => {
  setLoading(true)
  try {
    const response = await api.list()
    setData(response.data)
  } finally {
    setLoading(false)
  }
}
```

### Background Tasks

FastAPI background tasks run after response is sent:

```python
background_tasks.add_task(function_name, arg1, arg2)
```

---

## ✅ Checklist

- [ ] Uncomment and implement all router endpoints in `backend/app/routers/`
- [ ] Test each endpoint in FastAPI docs
- [ ] Uncomment and configure axios in `frontend/src/services/api.ts`
- [ ] Uncomment all API functions (projectsApi, searchApi, plansApi)
- [ ] Test API calls from browser DevTools
- [ ] Implement error handling in both frontend and backend
- [ ] Add loading states in UI components
- [ ] Test end-to-end flow: Create → Index → Search → Generate Plan

---

## 📚 Resources

- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **SQLAlchemy Async**: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- **Axios Documentation**: https://axios-http.com/docs/intro
- **React Hooks**: https://react.dev/reference/react
- **TypeScript**: https://www.typescriptlang.org/docs/

---

**Good luck! 🚀 Remember to uncomment the code and implement step by step!**
