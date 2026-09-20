import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { Link } from 'react-router-dom';
import { FileCheck, ArrowUpRight, Flame, ShieldAlert, Clock } from 'lucide-react';

export const FileList = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getFiles()
      .then((res) => setFiles(res.data.results || res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-8 text-slate-500">Loading Government Files...</div>;
  }

  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
          <FileCheck className="w-7 h-7 text-blue-600" />
          Government Files Repository
        </h1>
        <p className="text-sm text-slate-500">Official Administrative & Technical Records System</p>
      </div>

      <div className="glass-card rounded-2xl p-6">
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
                    {file.current_holder_name}
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
      </div>
    </div>
  );
};
