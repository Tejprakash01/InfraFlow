import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { Receipt, Plus, CheckCircle2, Clock, AlertTriangle, ShieldCheck, DollarSign } from 'lucide-react';

export const BillsList = () => {
  const { user } = useAuth();
  const [bills, setBills] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const [formData, setFormData] = useState({
    project: '',
    bill_period_start: '2026-03-01',
    bill_period_end: '2026-03-31',
    gross_amount: '',
    deductions_amount: '0.00',
    net_amount: '0.00',
  });

  const loadData = () => {
    setLoading(true);
    Promise.all([
      api.getBills(),
      api.getProjects()
    ])
      .then(([billRes, projRes]) => {
        setBills(billRes.data.results || billRes.data || []);
        const projList = projRes.data.results || projRes.data || [];
        setProjects(projList);
        if (projList.length > 0 && !formData.project) {
          setFormData(prev => ({ ...prev, project: projList[0].id }));
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAmountChange = (gross, deductions) => {
    const g = parseFloat(gross) || 0;
    const d = parseFloat(deductions) || 0;
    const net = Math.max(0, g - d);
    setFormData(prev => ({
      ...prev,
      gross_amount: gross,
      deductions_amount: deductions,
      net_amount: net.toFixed(2)
    }));
  };

  const handleCreateBill = async (e) => {
    e.preventDefault();
    if (!formData.project || !formData.gross_amount) {
      alert('Please select project and enter gross amount');
      return;
    }

    setSubmitting(true);
    try {
      await api.createBill({
        project: formData.project,
        bill_period_start: formData.bill_period_start,
        bill_period_end: formData.bill_period_end,
        gross_amount: parseFloat(formData.gross_amount),
        deductions_amount: parseFloat(formData.deductions_amount) || 0,
        net_amount: parseFloat(formData.net_amount)
      });
      setSuccessMsg('Running Account Bill submitted and linked to Government File workflow!');
      setShowCreateModal(false);
      setFormData({
        project: projects[0]?.id || '',
        bill_period_start: '2026-04-01',
        bill_period_end: '2026-04-30',
        gross_amount: '',
        deductions_amount: '0.00',
        net_amount: '0.00'
      });
      loadData();
      setTimeout(() => setSuccessMsg(''), 4000);
    } catch (err) {
      console.error(err);
      let errorDetail = 'Please verify input values.';
      if (err.response?.data) {
        if (typeof err.response.data === 'string') {
          errorDetail = err.response.status === 500 ? 'Internal Server Error (500). Please retry.' : err.response.data;
        } else if (typeof err.response.data === 'object') {
          errorDetail = Object.entries(err.response.data)
            .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`)
            .join(' | ');
        }
      }
      alert(`Failed to submit bill: ${errorDetail}`);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="p-8 text-slate-500">Loading RA Bills...</div>;

  return (
    <div className="p-8 space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
            <Receipt className="w-7 h-7 text-blue-600" />
            Running Account (RA) Bills & Payment Sanctions
          </h1>
          <p className="text-sm text-slate-500">11-Step Billing Verification & Financial Scrutiny System</p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="btn-primary flex items-center gap-2 text-sm shadow-lg shadow-blue-500/20"
        >
          <Plus className="w-4 h-4" />
          Submit New RA Bill
        </button>
      </div>

      {successMsg && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-3 text-emerald-700 text-sm">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      <div className="glass-card rounded-2xl p-6">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase">
                <th className="py-3 px-4">Bill Number</th>
                <th className="py-3 px-4">Linked Government File</th>
                <th className="py-3 px-4">Bill Period</th>
                <th className="py-3 px-4">Gross Amount</th>
                <th className="py-3 px-4">Deductions</th>
                <th className="py-3 px-4">Net Sanctioned</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Submitted By</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {bills.map((b) => (
                <tr key={b.id} className="hover:bg-slate-50 transition">
                  <td className="py-3.5 px-4 font-mono font-bold text-blue-600">{b.bill_number}</td>
                  <td className="py-3.5 px-4 font-mono text-xs text-slate-600">{b.file_number || 'FILE-BILL-0001'}</td>
                  <td className="py-3.5 px-4 text-xs text-slate-500">
                    {b.bill_period_start} to {b.bill_period_end}
                  </td>
                  <td className="py-3.5 px-4 text-slate-700">₹{(parseFloat(b.gross_amount) / 100000).toFixed(2)} L</td>
                  <td className="py-3.5 px-4 text-rose-600">₹{(parseFloat(b.deductions_amount) / 100000).toFixed(2)} L</td>
                  <td className="py-3.5 px-4 font-bold text-emerald-600">₹{(parseFloat(b.net_amount) / 100000).toFixed(2)} L</td>
                  <td className="py-3.5 px-4">
                    <span className={b.status === 'PAID' ? 'badge-green' : b.status === 'SUBMITTED' ? 'badge-blue' : 'badge-amber'}>
                      {b.status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right text-xs text-slate-500">{b.submitted_by_name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal for Submitting New Bill */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/30 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white max-w-lg w-full p-6 rounded-2xl border border-slate-200 shadow-2xl space-y-5">
            <div className="flex justify-between items-center pb-3 border-b border-slate-200">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Receipt className="w-5 h-5 text-blue-600" />
                Submit New Running Account (RA) Bill
              </h2>
              <button 
                onClick={() => setShowCreateModal(false)}
                className="text-slate-400 hover:text-slate-700 text-xl font-bold"
              >
                &times;
              </button>
            </div>

            <form onSubmit={handleCreateBill} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  Project *
                </label>
                <select
                  value={formData.project}
                  onChange={(e) => setFormData({ ...formData, project: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
                >
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>{p.project_code} - {p.name}</option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    Bill Period Start *
                  </label>
                  <input
                    type="date"
                    value={formData.bill_period_start}
                    onChange={(e) => setFormData({ ...formData, bill_period_start: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    Bill Period End *
                  </label>
                  <input
                    type="date"
                    value={formData.bill_period_end}
                    onChange={(e) => setFormData({ ...formData, bill_period_end: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    Gross Executed Amount (₹) *
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    placeholder="e.g. 75000000"
                    value={formData.gross_amount}
                    onChange={(e) => handleAmountChange(e.target.value, formData.deductions_amount)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    Total Statutory Deductions (₹)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    placeholder="TDS, Retention, Cess"
                    value={formData.deductions_amount}
                    onChange={(e) => handleAmountChange(formData.gross_amount, e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex justify-between items-center text-xs">
                <span className="text-slate-500">Net Claimed Amount:</span>
                <span className="text-base font-bold text-emerald-600">
                  ₹{Number(formData.net_amount).toLocaleString('en-IN')}
                </span>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-200">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="btn-secondary text-xs"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="btn-primary text-xs flex items-center gap-2"
                >
                  {submitting ? 'Submitting...' : 'Submit RA Bill for Scrutiny'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

