import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { Link } from 'react-router-dom';
import { Inbox, AlertTriangle, Flame, FileText, ArrowUpRight, Clock, ShieldAlert, CheckCircle2 } from 'lucide-react';

export const WorkDesk = () => {
  const [deskData, setDeskData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getWorkDesk()
      .then((res) => setDeskData(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-8 text-slate-500">Loading Government Work Desk...</div>;
  }

  const files = deskData?.files || [];

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
          <Inbox className="w-7 h-7 text-blue-600" />
          Government Work Desk
        </h1>
        <p className="text-sm text-slate-500">Central File Inbox & Pending Official Actions</p>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-5 rounded-2xl flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Awaiting My Action</div>
            <div className="text-3xl font-extrabold text-slate-900 mt-1">{deskData?.awaiting_action_count || 0}</div>
          </div>
          <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center">
            <FileText className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl flex items-center justify-between border-rose-200">
          <div>
            <div className="text-xs font-semibold text-rose-600 uppercase tracking-wider flex items-center gap-1">
              <AlertTriangle className="w-3.5 h-3.5" /> Overdue SLA Files
            </div>
            <div className="text-3xl font-extrabold text-rose-600 mt-1">{deskData?.overdue_count || 0}</div>
          </div>
          <div className="w-12 h-12 bg-rose-50 text-rose-600 rounded-xl flex items-center justify-center">
            <ShieldAlert className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-amber-600 uppercase tracking-wider">High / Urgent Priority</div>
            <div className="text-3xl font-extrabold text-amber-600 mt-1">{deskData?.high_priority_count || 0}</div>
          </div>
          <div className="w-12 h-12 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center">
            <Flame className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-emerald-600 uppercase tracking-wider">Completed / Approved</div>
            <div className="text-3xl font-extrabold text-emerald-600 mt-1">12</div>
          </div>
          <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center">
            <CheckCircle2 className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Files Table */}
      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-lg font-bold text-slate-900 mb-4">Files Requiring Attention</h2>
        {files.length === 0 ? (
          <div className="py-12 text-center text-slate-500">No files currently awaiting action on your desk.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  <th className="py-3 px-4">File Number</th>
                  <th className="py-3 px-4">Subject</th>
                  <th className="py-3 px-4">Project</th>
                  <th className="py-3 px-4">Priority</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Current Holder</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                {files.map((file) => (
                  <tr key={file.id} className="hover:bg-slate-50 transition">
                    <td className="py-3.5 px-4 font-mono font-semibold text-blue-600">{file.file_number}</td>
                    <td className="py-3.5 px-4 font-medium text-slate-900 max-w-xs truncate">{file.subject}</td>
                    <td className="py-3.5 px-4 text-slate-600 text-xs">{file.project_code}</td>
                    <td className="py-3.5 px-4">
                      <span className={file.priority === 'URGENT' || file.priority === 'HIGH' ? 'badge-amber' : 'badge-blue'}>
                        {file.priority}
                      </span>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={file.is_overdue ? 'badge-red' : 'badge-green'}>
                        {file.is_overdue ? 'OVERDUE' : file.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-xs text-slate-600">
                      {file.current_holder_name} ({file.current_holder_designation})
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <Link
                        to={`/files/${file.id}`}
                        className="inline-flex items-center gap-1 text-xs font-semibold text-blue-600 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-lg border border-blue-200 transition"
                      >
                        Open File <ArrowUpRight className="w-3.5 h-3.5" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
