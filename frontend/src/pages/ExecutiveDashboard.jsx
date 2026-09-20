import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { LayoutDashboard, TrendingUp, AlertOctagon, DollarSign, FolderGit2, CheckCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export const ExecutiveDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getExecutiveDashboard()
      .then((res) => setData(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-8 text-slate-500">Loading Executive Portfolio Dashboard...</div>;
  }

  const chartData = data?.projects_summary || [];

  return (
    <div className="p-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
          <LayoutDashboard className="w-7 h-7 text-blue-600" />
          Regional Executive Portfolio Dashboard
        </h1>
        <p className="text-sm text-slate-500">Authority Level Infrastructure Progress & Administrative SLA Bottlenecks</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-5 rounded-2xl">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Portfolio Projects</div>
          <div className="text-3xl font-extrabold text-slate-900 mt-1">{data?.total_projects || 0}</div>
        </div>
        <div className="glass-card p-5 rounded-2xl">
          <div className="text-xs font-semibold text-emerald-600 uppercase tracking-wider">Total Contract Value</div>
          <div className="text-2xl font-extrabold text-emerald-600 mt-1">₹{(data?.total_contract_value / 10000000).toFixed(2)} Cr</div>
        </div>
        <div className="glass-card p-5 rounded-2xl">
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-wider">Avg Physical Progress</div>
          <div className="text-3xl font-extrabold text-blue-600 mt-1">{data?.avg_physical_progress_pct}%</div>
        </div>
        <div className="glass-card p-5 rounded-2xl border-rose-200">
          <div className="text-xs font-semibold text-rose-600 uppercase tracking-wider">SLA Overdue Files</div>
          <div className="text-3xl font-extrabold text-rose-600 mt-1">{data?.overdue_files_count || 0}</div>
        </div>
      </div>

      {/* Recharts Chart: Physical vs Financial Progress */}
      <div className="glass-card p-6 rounded-2xl space-y-4">
        <h2 className="text-lg font-bold text-slate-900">Project Progress Comparison (Physical vs Financial %)</h2>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="code" stroke="#64748b" />
              <YAxis stroke="#64748b" unit="%" />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', color: '#1e293b', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }} />
              <Bar dataKey="physical_progress_pct" name="Physical Progress %" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="financial_progress_pct" name="Financial Progress %" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
