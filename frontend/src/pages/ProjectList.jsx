import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { Link } from 'react-router-dom';
import { FolderGit2, MapPin, Calendar, ArrowUpRight, DollarSign } from 'lucide-react';

export const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getProjects()
      .then((res) => {
        const data = res.data?.results || res.data || [];
        setProjects(Array.isArray(data) ? data : []);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-8 text-slate-500">Loading Infrastructure Projects...</div>;
  }

  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
          <FolderGit2 className="w-7 h-7 text-blue-600" />
          Infrastructure Projects
        </h1>
        <p className="text-sm text-slate-500">Active Highway Construction & Development Portfolio</p>
      </div>

      {projects.length === 0 ? (
        <div className="glass-card p-12 text-center rounded-2xl">
          <FolderGit2 className="w-12 h-12 text-slate-400 mx-auto mb-3" />
          <h3 className="text-lg font-semibold text-slate-600">No Projects Found</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
            There are no projects assigned to your current role or organization. Switch to an admin account or verify your organization assignment.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {projects.map((p) => (
            <div key={p.id} className="glass-card p-6 rounded-2xl flex flex-col justify-between hover:border-blue-300 transition">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-mono text-xs font-bold text-blue-600 bg-blue-50 border border-blue-200 px-2.5 py-1 rounded-md">
                    {p.project_code}
                  </span>
                  <span className={p.status === 'ACTIVE' ? 'badge-green' : 'badge-blue'}>
                    {p.status}
                  </span>
                </div>
                <h2 className="text-lg font-bold text-slate-900 mb-2">{p.name}</h2>
                <p className="text-xs text-slate-500 mb-4 flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" /> {p.location}
                </p>

                <div className="grid grid-cols-2 gap-4 bg-slate-50 p-3 rounded-xl mb-4 border border-slate-200 text-xs">
                  <div>
                    <span className="text-slate-500 block">Contract Value</span>
                    <span className="font-bold text-slate-800">₹{(p.contract_value / 10000000).toFixed(2)} Cr</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Completion Date</span>
                    <span className="font-bold text-slate-800">{p.scheduled_completion_date}</span>
                  </div>
                </div>

                {/* Progress Bars */}
                <div className="space-y-2 mb-4">
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-500">Physical Progress</span>
                      <span className="font-bold text-blue-600">{p.physical_progress_pct}%</span>
                    </div>
                    <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                      <div className="bg-blue-500 h-full rounded-full" style={{ width: `${p.physical_progress_pct}%` }}></div>
                    </div>
                  </div>
                </div>
              </div>

              <Link
                to={`/projects/${p.id}`}
                className="btn-secondary justify-center w-full text-xs py-2 mt-2"
              >
                View Full Project Details <ArrowUpRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
