import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Shield, KeyRound, UserCheck, ArrowRight, Building2, HardHat, ShieldCheck } from 'lucide-react';

export const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    if (e) e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const user = await login(username, password);
      if (user.role === 'SUPER_ADMIN' || user.role === 'HQ_ADMIN') {
        navigate('/admin');
      } else if (user.is_contractor_user) {
        navigate('/contractor/dashboard');
      } else {
        navigate('/work-desk');
      }
    } catch (err) {
      setError('Invalid username or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loginAsDemo = async (demoUsername) => {
    setUsername(demoUsername);
    setPassword('DemoPass123!');
    setLoading(true);
    setError('');
    try {
      const user = await login(demoUsername, 'DemoPass123!');
      if (user.role === 'SUPER_ADMIN' || user.role === 'HQ_ADMIN') {
        navigate('/admin');
      } else if (user.is_contractor_user) {
        navigate('/contractor/dashboard');
      } else {
        navigate('/work-desk');
      }
    } catch (err) {
      setError('Failed to login with demo account. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col justify-center items-center p-4 relative overflow-hidden">
      <div className="w-full max-w-4xl grid md:grid-cols-2 gap-6 z-10">
        {/* Left Card: Login Form */}
        <div className="glass-card p-8 rounded-2xl flex flex-col justify-between shadow-lg">
          <div>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center font-bold text-white text-xl shadow-md shadow-blue-500/20">
                IF
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900">Infra<span className="text-blue-600">Flow</span></h1>
                <p className="text-xs text-slate-500">Government Infrastructure & Workflow Operations</p>
              </div>
            </div>

            {error && (
              <div className="mb-4 p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg font-medium">
                {error}
              </div>
            )}

            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase text-slate-600 mb-1">Username / Email</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. admin or project_director"
                  className="w-full bg-white border border-slate-300 rounded-xl px-4 py-2.5 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 transition"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase text-slate-600 mb-1">Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-white border border-slate-300 rounded-xl px-4 py-2.5 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 transition"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full btn-primary justify-center py-3 text-sm mt-2 font-semibold shadow-md"
              >
                {loading ? 'Authenticating...' : 'Sign In to Portal'}
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          </div>

          <div className="mt-8 pt-4 border-t border-slate-200 text-center text-xs text-slate-500">
            NHAI / PWD Standard Operations • Production & Demo Mode
          </div>
        </div>

        {/* Right Card: Quick 1-Click Role Presets */}
        <div className="glass-card p-8 rounded-2xl flex flex-col justify-between shadow-lg">
          <div>
            <h2 className="text-lg font-bold text-slate-900 mb-1 flex items-center gap-2">
              <UserCheck className="w-5 h-5 text-blue-600" />
              Quick Demo Login Presets
            </h2>
            <p className="text-xs text-slate-500 mb-5">Click any role to instant login as seeded demo account:</p>

            <div className="space-y-2.5">
              {/* Dedicated Super Admin Login */}
              <button
                onClick={() => loginAsDemo('admin')}
                className="w-full text-left p-3 rounded-xl bg-blue-50/70 hover:bg-blue-100/80 border border-blue-200 transition flex items-center justify-between group"
              >
                <div>
                  <div className="text-sm font-bold text-blue-900 flex items-center gap-1.5">
                    <ShieldCheck className="w-4 h-4 text-blue-600" /> System Super Admin
                  </div>
                  <div className="text-xs text-blue-700/80">Oversees all users, organizations, workflows & audit logs</div>
                </div>
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-600 text-white shadow-sm">
                  Super Admin
                </span>
              </button>

              <button
                onClick={() => loginAsDemo('project_director')}
                className="w-full text-left p-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 transition flex items-center justify-between group"
              >
                <div>
                  <div className="text-sm font-semibold text-slate-800 group-hover:text-blue-600">Project Director</div>
                  <div className="text-xs text-slate-500">Ahmedabad PIU • Approving Competent Authority</div>
                </div>
                <Building2 className="w-4 h-4 text-slate-400 group-hover:text-blue-600" />
              </button>

              <button
                onClick={() => loginAsDemo('authority_engineer')}
                className="w-full text-left p-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 transition flex items-center justify-between group"
              >
                <div>
                  <div className="text-sm font-semibold text-slate-800 group-hover:text-blue-600">Authority Engineer</div>
                  <div className="text-xs text-slate-500">Technical Scrutiny & Measurement Verification</div>
                </div>
                <Building2 className="w-4 h-4 text-slate-400 group-hover:text-blue-600" />
              </button>

              <button
                onClick={() => loginAsDemo('finance_officer')}
                className="w-full text-left p-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 transition flex items-center justify-between group"
              >
                <div>
                  <div className="text-sm font-semibold text-slate-800 group-hover:text-blue-600">Finance Officer</div>
                  <div className="text-xs text-slate-500">Ahmedabad PIU • Financial Scrutiny & Tax Deductions</div>
                </div>
                <Building2 className="w-4 h-4 text-slate-400 group-hover:text-blue-600" />
              </button>

              <button
                onClick={() => loginAsDemo('regional_officer')}
                className="w-full text-left p-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 transition flex items-center justify-between group"
              >
                <div>
                  <div className="text-sm font-semibold text-slate-800 group-hover:text-amber-600">Regional Officer</div>
                  <div className="text-xs text-slate-500">Gujarat Region • SLA Escalations & Bottlenecks</div>
                </div>
                <Shield className="w-4 h-4 text-slate-400 group-hover:text-amber-600" />
              </button>

              <button
                onClick={() => loginAsDemo('contractor_pm')}
                className="w-full text-left p-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 transition flex items-center justify-between group"
              >
                <div>
                  <div className="text-sm font-semibold text-slate-800 group-hover:text-emerald-600">Contractor Project Manager</div>
                  <div className="text-xs text-slate-500">ABC Infra Pvt Ltd • Upload Documents & Bills</div>
                </div>
                <HardHat className="w-4 h-4 text-slate-400 group-hover:text-emerald-600" />
              </button>
            </div>
          </div>

          <div className="mt-4 text-xs text-slate-500 bg-slate-50 p-2.5 rounded-lg border border-slate-200">
            Password for all demo accounts: <code className="text-blue-600 font-mono font-bold">DemoPass123!</code>
          </div>
        </div>
      </div>
    </div>
  );
};
