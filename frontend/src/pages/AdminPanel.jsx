import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { 
  ShieldCheck, Users, Building2, FolderGit2, FileText, 
  Receipt, Workflow, History, Bell, Plus, CheckCircle2, 
  ExternalLink, Search, RefreshCw, Key
} from 'lucide-react';

export const AdminPanel = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);

  // Data states
  const [users, setUsers] = useState([]);
  const [organizations, setOrganizations] = useState([]);
  const [projects, setProjects] = useState([]);
  const [workflows, setWorkflows] = useState([]);
  const [slas, setSlas] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [notifications, setNotifications] = useState([]);

  const loadAllAdminData = () => {
    setLoading(true);
    Promise.allSettled([
      api.getUsers(),
      api.getOrganizations(),
      api.getProjects(),
      api.getWorkflows(),
      api.getSLAs(),
      api.getAuditLogs(),
      api.getNotifications()
    ])
      .then(([uRes, oRes, pRes, wRes, sRes, aRes, nRes]) => {
        if (uRes.status === 'fulfilled') setUsers(uRes.value.data?.results || uRes.value.data || []);
        if (oRes.status === 'fulfilled') setOrganizations(oRes.value.data?.results || oRes.value.data || []);
        if (pRes.status === 'fulfilled') setProjects(pRes.value.data?.results || pRes.value.data || []);
        if (wRes.status === 'fulfilled') setWorkflows(wRes.value.data?.results || wRes.value.data || []);
        if (sRes.status === 'fulfilled') setSlas(sRes.value.data?.results || sRes.value.data || []);
        if (aRes.status === 'fulfilled') setAuditLogs(aRes.value.data?.results || aRes.value.data || []);
        if (nRes.status === 'fulfilled') setNotifications(nRes.value.data?.results || nRes.value.data || []);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadAllAdminData();
  }, []);

  const stats = [
    { label: 'Registered Personnel', value: users.length, icon: Users, color: 'text-blue-600', bg: 'bg-blue-50' },
    { label: 'Authorized Entities', value: organizations.length, icon: Building2, color: 'text-purple-600', bg: 'bg-purple-50' },
    { label: 'Infrastructure Projects', value: projects.length, icon: FolderGit2, color: 'text-emerald-600', bg: 'bg-emerald-50' },
    { label: 'Workflow Definitions', value: workflows.length, icon: Workflow, color: 'text-amber-600', bg: 'bg-amber-50' },
    { label: 'SLA Guardrail Policies', value: slas.length, icon: ShieldCheck, color: 'text-cyan-600', bg: 'bg-cyan-50' },
    { label: 'Security Audit Records', value: auditLogs.length, icon: History, color: 'text-rose-600', bg: 'bg-rose-50' },
  ];

  return (
    <div className="p-8 space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
            <ShieldCheck className="w-8 h-8 text-blue-600" />
            InfraFlow Master Administration Portal
          </h1>
          <p className="text-sm text-slate-500">
            System Governance, RBAC Hierarchies, Workflow Engines, SLAs & Immutable Audit Trails
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={loadAllAdminData}
            className="btn-secondary text-xs flex items-center gap-2"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh Data
          </button>
          <a
            href="http://localhost:8000/admin/"
            target="_blank"
            rel="noreferrer"
            className="btn-primary text-xs flex items-center gap-2 shadow-lg shadow-blue-500/20"
          >
            <Key className="w-3.5 h-3.5" /> Open Django Core Admin <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {stats.map((s, idx) => {
          const Icon = s.icon;
          return (
            <div key={idx} className="glass-card p-4 rounded-2xl flex flex-col justify-between">
              <div className={`p-2.5 rounded-xl w-fit ${s.bg} mb-3`}>
                <Icon className={`w-5 h-5 ${s.color}`} />
              </div>
              <div>
                <div className="text-2xl font-bold text-slate-900">{loading ? '...' : s.value}</div>
                <div className="text-[11px] text-slate-500 mt-0.5">{s.label}</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Tab Navigation */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-3 overflow-x-auto scrollbar-none">
        {[
          { id: 'overview', label: 'System Overview' },
          { id: 'users', label: `Users & Roles (${users.length})` },
          { id: 'organizations', label: `Organizations & PIUs (${organizations.length})` },
          { id: 'projects', label: `Active Projects (${projects.length})` },
          { id: 'workflows', label: `Workflow Definitions (${workflows.length})` },
          { id: 'audit', label: `Security Audit Logs (${auditLogs.length})` },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition ${
              activeTab === tab.id
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20'
                : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* TAB 1: SYSTEM OVERVIEW */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass-card p-6 rounded-2xl space-y-4">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Building2 className="w-5 h-5 text-purple-600" />
              National Authority Hierarchy Tree
            </h2>
            <div className="space-y-3">
              {organizations.map((org) => (
                <div key={org.id} className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between">
                  <div>
                    <div className="font-semibold text-sm text-slate-800">{org.name}</div>
                    <div className="text-xs text-slate-500 font-mono mt-0.5">Code: {org.code}</div>
                  </div>
                  <span className="text-[10px] font-mono font-bold px-2 py-1 rounded bg-blue-50 text-blue-600 border border-blue-200">
                    {org.node_type}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="glass-card p-6 rounded-2xl space-y-4">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-cyan-600" />
              Configured SLA & Escalation Rules
            </h2>
            <div className="space-y-3">
              {slas.map((s) => (
                <div key={s.id} className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-sm text-slate-800">{s.name}</span>
                    <span className="badge-blue text-[10px]">Escalate to: {s.escalation_target_role}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-3 text-xs text-slate-500 pt-2 border-t border-slate-200">
                    <div>Warning Threshold: <strong className="text-amber-600">{s.warning_threshold_hours} hrs</strong></div>
                    <div>Hard Breach Escalate: <strong className="text-rose-600">{s.escalation_threshold_hours} hrs</strong></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: USERS */}
      {activeTab === 'users' && (
        <div className="glass-card rounded-2xl p-6">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase">
                  <th className="py-3 px-4">Officer Name</th>
                  <th className="py-3 px-4">Username & Email</th>
                  <th className="py-3 px-4">Designation & Role</th>
                  <th className="py-3 px-4">Department / Org</th>
                  <th className="py-3 px-4 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50 transition">
                    <td className="py-3 px-4 font-bold text-slate-900">
                      {u.first_name} {u.last_name}
                    </td>
                    <td className="py-3 px-4 text-xs font-mono text-slate-500">
                      <div>@{u.username}</div>
                      <div className="text-slate-400">{u.email}</div>
                    </td>
                    <td className="py-3 px-4">
                      <div className="text-xs text-slate-600 font-semibold">{u.designation_title || 'Officer'}</div>
                      <span className="text-[10px] font-mono text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200 inline-block mt-0.5">
                        {u.role}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-xs text-slate-600">
                      {u.organization_name || 'Authority'}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <span className="badge-green text-xs">Active</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 3: ORGANIZATIONS */}
      {activeTab === 'organizations' && (
        <div className="glass-card rounded-2xl p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {organizations.map((org) => (
              <div key={org.id} className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3">
                <div className="flex justify-between items-start">
                  <span className="font-mono text-xs font-bold text-blue-600 bg-blue-50 border border-blue-200 px-2.5 py-1 rounded">
                    {org.code}
                  </span>
                  <span className="badge-green text-[10px]">Active</span>
                </div>
                <h3 className="font-bold text-slate-900 text-sm">{org.name}</h3>
                <div className="text-xs text-slate-500 pt-2 border-t border-slate-200">
                  Node Type: <span className="text-slate-700 font-semibold">{org.node_type}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 4: PROJECTS */}
      {activeTab === 'projects' && (
        <div className="glass-card rounded-2xl p-6">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase">
                  <th className="py-3 px-4">Code</th>
                  <th className="py-3 px-4">Project Title</th>
                  <th className="py-3 px-4">Contract Value</th>
                  <th className="py-3 px-4">Physical / Financial</th>
                  <th className="py-3 px-4">Completion Date</th>
                  <th className="py-3 px-4 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                {projects.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50 transition">
                    <td className="py-3 px-4 font-mono font-bold text-blue-600 text-xs">{p.project_code}</td>
                    <td className="py-3 px-4 font-bold text-slate-900 text-sm">{p.name}</td>
                    <td className="py-3 px-4 text-slate-600">₹{(p.contract_value / 10000000).toFixed(2)} Cr</td>
                    <td className="py-3 px-4 text-xs">
                      <span className="text-blue-600 font-bold">{p.physical_progress_pct}%</span> / <span className="text-emerald-600 font-bold">{p.financial_progress_pct}%</span>
                    </td>
                    <td className="py-3 px-4 text-xs text-slate-500">{p.scheduled_completion_date}</td>
                    <td className="py-3 px-4 text-right">
                      <span className="badge-green text-xs">{p.status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 5: WORKFLOWS */}
      {activeTab === 'workflows' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {workflows.map((wf) => (
            <div key={wf.id} className="glass-card p-6 rounded-2xl space-y-4">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-[10px] font-mono text-purple-600 bg-purple-50 border border-purple-200 px-2 py-0.5 rounded">
                    {wf.code}
                  </span>
                  <h3 className="font-bold text-slate-900 text-base mt-2">{wf.name}</h3>
                </div>
                <span className="badge-green text-xs">Active</span>
              </div>
              <p className="text-xs text-slate-500">{wf.description || 'Configurable multi-tier scrutiny flow.'}</p>
            </div>
          ))}
        </div>
      )}

      {/* TAB 6: AUDIT LOGS */}
      {activeTab === 'audit' && (
        <div className="glass-card rounded-2xl p-6">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase">
                  <th className="py-3 px-4">Timestamp</th>
                  <th className="py-3 px-4">Action</th>
                  <th className="py-3 px-4">Entity Type & ID</th>
                  <th className="py-3 px-4">Actor</th>
                  <th className="py-3 px-4 text-right">Client IP</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                {auditLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50 transition">
                    <td className="py-3 px-4 text-xs font-mono text-slate-500">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-xs font-bold text-blue-600 font-mono">{log.action}</span>
                    </td>
                    <td className="py-3 px-4 text-xs text-slate-600">
                      {log.entity_type} #{log.entity_id?.slice(0, 8)}
                    </td>
                    <td className="py-3 px-4 text-xs text-slate-500">{log.actor_name || 'System Official'}</td>
                    <td className="py-3 px-4 text-right text-xs font-mono text-slate-400">{log.ip_address || '127.0.0.1'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
