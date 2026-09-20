import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { Login } from './pages/Login';
import { WorkDesk } from './pages/WorkDesk';
import { ExecutiveDashboard } from './pages/ExecutiveDashboard';
import { ProjectList } from './pages/ProjectList';
import { ProjectDetail } from './pages/ProjectDetail';
import { FileList } from './pages/FileList';
import { FileDetail } from './pages/FileDetail';
import { ContractorDashboard } from './pages/ContractorDashboard';
import { BillsList } from './pages/BillsList';
import { RFIsList } from './pages/RFIsList';
import { NCRsList } from './pages/NCRsList';
import { AdminPanel } from './pages/AdminPanel';
import { DocumentManager } from './pages/DocumentManager';

const ProtectedLayout = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="min-h-screen bg-slate-50 text-slate-500 flex items-center justify-center font-medium">Loading InfraFlow Operations System...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col text-slate-800">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 overflow-y-auto">
          <Routes>
            <Route path="/" element={<Navigate to={user.role === 'SUPER_ADMIN' || user.role === 'HQ_ADMIN' ? "/admin" : user.is_contractor_user ? "/contractor/dashboard" : "/work-desk"} replace />} />
            <Route path="/admin" element={<AdminPanel />} />
            <Route path="/work-desk" element={<WorkDesk />} />
            <Route path="/executive-dashboard" element={<ExecutiveDashboard />} />
            <Route path="/projects" element={<ProjectList />} />
            <Route path="/projects/:id" element={<ProjectDetail />} />
            <Route path="/documents" element={<DocumentManager />} />
            <Route path="/files" element={<FileList />} />
            <Route path="/files/:id" element={<FileDetail />} />
            <Route path="/contractor/dashboard" element={<ContractorDashboard />} />
            <Route path="/bills" element={<BillsList />} />
            <Route path="/rfis" element={<RFIsList />} />
            <Route path="/ncrs" element={<NCRsList />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/*" element={<ProtectedLayout />} />
    </Routes>
  );
}

export default App;
