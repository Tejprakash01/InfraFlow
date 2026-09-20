import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api/client';
import { FolderGit2, MapPin, Calendar, Building2, Users, FileText, CheckCircle2, ShieldAlert } from 'lucide-react';

export const ProjectDetail = () => {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getProjectDetail(id)
      .then((res) => setProject(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <div className="p-8 text-slate-500">Loading Project Details...</div>;
  }

  if (!project) {
    return <div className="p-8 text-rose-600">Project Not Found</div>;
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="glass-card p-6 rounded-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="font-mono text-xs font-bold text-blue-600 bg-blue-50 border border-blue-200 px-2.5 py-1 rounded-md">
              {project.project_code}
            </span>
            <span className="badge-green">{project.status}</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900">{project.name}</h1>
          <p className="text-xs text-slate-500 mt-1 flex items-center gap-1.5">
            <MapPin className="w-3.5 h-3.5 text-slate-400" /> {project.location}
          </p>
        </div>

        <div className="flex gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs">
          <div>
            <span className="text-slate-500 block">Contract Value</span>
            <span className="font-bold text-emerald-600 text-base">₹{(project.contract_value / 10000000).toFixed(2)} Cr</span>
          </div>
          <div className="border-l border-slate-200 pl-4">
            <span className="text-slate-500 block">Physical Progress</span>
            <span className="font-bold text-blue-600 text-base">{project.physical_progress_pct}%</span>
          </div>
        </div>
      </div>

      {/* Stakeholders & Organization Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-5 rounded-2xl">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-2">
            <Building2 className="w-4 h-4 text-blue-600" /> Government Authority & PIU
          </div>
          <div className="font-bold text-slate-900 text-sm">{project.authority_name}</div>
          <div className="text-xs text-slate-500 mt-1">{project.piu_name}</div>
        </div>

        <div className="glass-card p-5 rounded-2xl">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-2">
            <Building2 className="w-4 h-4 text-emerald-600" /> Contractor Organization
          </div>
          <div className="font-bold text-slate-900 text-sm">{project.contractor_name || 'Unassigned'}</div>
        </div>

        <div className="glass-card p-5 rounded-2xl">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-2">
            <Building2 className="w-4 h-4 text-amber-600" /> Independent Consultant
          </div>
          <div className="font-bold text-slate-900 text-sm">{project.consultant_name || 'Unassigned'}</div>
        </div>
      </div>

      {/* Work Packages Table */}
      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-lg font-bold text-slate-900 mb-4">Work Packages & Execution Status</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase">
                <th className="py-3 px-4">Package Name</th>
                <th className="py-3 px-4">Start Date</th>
                <th className="py-3 px-4">Target Finish</th>
                <th className="py-3 px-4">Planned %</th>
                <th className="py-3 px-4">Actual %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {project.work_packages?.map((wp) => (
                <tr key={wp.id} className="hover:bg-slate-50 transition">
                  <td className="py-3 px-4 font-semibold text-slate-900">{wp.name}</td>
                  <td className="py-3 px-4 text-xs text-slate-500">{wp.start_date}</td>
                  <td className="py-3 px-4 text-xs text-slate-500">{wp.end_date}</td>
                  <td className="py-3 px-4 text-xs font-mono text-slate-600">{wp.planned_progress_pct}%</td>
                  <td className="py-3 px-4 text-xs font-mono font-bold text-blue-600">{wp.actual_progress_pct}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
