import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Projects from './pages/Projects'
import TaskInput from './pages/TaskInput'
import PlanView from './pages/PlanView'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Projects />} />
        <Route path="/task/:projectId" element={<TaskInput />} />
        <Route path="/plan/:planId" element={<PlanView />} />
      </Routes>
    </Layout>
  )
}

export default App
