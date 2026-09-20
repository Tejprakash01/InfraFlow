import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { HardHat, Receipt, ClipboardCheck, ShieldAlert, FolderGit2, ArrowUpRight, CheckCircle2, Clock } from 'lucide-react';

export const ContractorDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getContractorDashboard()
      .then((res) => setData(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-8 text-slate-500">Loading Contractor Portal...</div>;
  }

  const bills = data?.recent_bills || [];

  return (
    <div className="p-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
          <HardHat className="w-7 h-7 text-emerald-600" />
          Contractor Portal Dashboard
        </h1>
        <p className="text-sm text-slate-500">Submissions, RA Bills Tracking & Quality Compliance Portal</p>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-5 rounded-2xl">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Assigned Projects</div>
          <div className="text-3xl font-extrabold text-slate-900 mt-1">{data?.assigned_projects_count || 0}</div>
        </div>
        <div className="glass-card p-5 rounded-2xl">
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-wider">Submitted RA Bills</div>
          <div className="text-3xl font-extrabold text-blue-600 mt-1">{data?.total_bills_submitted || 0}</div>
        </div>
        <div className="glass-card p-5 rounded-2xl">
          <div className="text-xs font-semibold text-amber-600 uppercase tracking-wider">Pending Payment Sanction</div>
          <div className="text-3xl font-extrabold text-amber-600 mt-1">{data?.bills_pending_payment || 0}</div>
        </div>
        <div className="glass-card p-5 rounded-2xl border-emerald-200">
          <div className="text-xs font-semibold text-emerald-600 uppercase tracking-wider">Disbursed / Paid Bills</div>
          <div className="text-3xl font-extrabold text-emerald-600 mt-1">{data?.paid_bills_count || 0}</div>
        </div>
      </div>

      {/* Recent RA Bills Status Tracker */}
      <div className="glass-card rounded-2xl p-6 space-y-4">
        <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <Receipt className="w-5 h-5 text-blue-600" /> RA Bill Processing Status Tracker
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase">
                <th className="py-3 px-4">Bill Number</th>
                <th className="py-3 px-4">Project</th>
                <th className="py-3 px-4">Net Amount</th>
                <th className="py-3 px-4">Government Workflow Status</th>
                <th className="py-3 px-4 text-right">Submitted On</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {bills.map((b) => (
                <tr key={b.id} className="hover:bg-slate-50 transition">
                  <td className="py-3.5 px-4 font-mono font-bold text-blue-600">{b.bill_number}</td>
                  <td className="py-3.5 px-4 text-slate-900 font-medium">{b.project_name}</td>
                  <td className="py-3.5 px-4 font-bold text-emerald-600">₹{(b.net_amount / 100000).toFixed(2)} Lakh</td>
                  <td className="py-3.5 px-4">
                    <span className={b.status === 'PAID' ? 'badge-green' : 'badge-amber'}>
                      {b.status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right text-xs text-slate-500">
                    {new Date(b.submitted_at).toLocaleDateString()}
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
