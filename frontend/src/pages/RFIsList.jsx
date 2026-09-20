import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { ClipboardCheck, MapPin, CheckCircle2 } from 'lucide-react';

export const RFIsList = () => {
  const [rfis, setRfis] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getRFIs()
      .then((res) => setRfis(res.data.results || res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-slate-500">Loading Request for Inspections (RFIs)...</div>;

  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
          <ClipboardCheck className="w-7 h-7 text-blue-600" />
          Request For Inspection (RFI) Register
        </h1>
        <p className="text-sm text-slate-500">Site Work Inspection Verification Portal</p>
      </div>

      <div className="glass-card rounded-2xl p-6">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase">
                <th className="py-3 px-4">RFI Number</th>
                <th className="py-3 px-4">Location</th>
                <th className="py-3 px-4">Description</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Requested By</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {rfis.map((r) => (
                <tr key={r.id} className="hover:bg-slate-50 transition">
                  <td className="py-3.5 px-4 font-mono font-bold text-blue-600">{r.rfi_number}</td>
                  <td className="py-3.5 px-4 text-slate-900 font-medium flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" /> {r.location}
                  </td>
                  <td className="py-3.5 px-4 text-slate-600 text-xs max-w-xs truncate">{r.description}</td>
                  <td className="py-3.5 px-4">
                    <span className={r.status === 'APPROVED' ? 'badge-green' : 'badge-blue'}>{r.status}</span>
                  </td>
                  <td className="py-3.5 px-4 text-right text-xs text-slate-500">{r.created_by_name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
