import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Shield, Bell, User as UserIcon, LogOut, FileText, ChevronRight } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="glass-nav sticky top-0 z-40 px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center font-bold text-white shadow-sm shadow-blue-500/20">
            IF
          </div>
          <div>
            <span className="font-extrabold text-lg text-slate-900 tracking-wide">Infra<span className="text-blue-600">Flow</span></span>
            <span className="hidden sm:inline-block ml-2 text-xs font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">GOVT OPS</span>
          </div>
        </Link>
      </div>

      {user && (
        <div className="flex items-center gap-4">
          <div className="hidden md:flex items-center gap-2 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200 text-xs">
            <span className="text-slate-500">Org:</span>
            <span className="font-semibold text-slate-700">{user.organization_name || 'National Infra Authority'}</span>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <div className="font-semibold text-sm text-slate-900">{user.first_name} {user.last_name}</div>
              <div className="text-xs text-blue-600 font-medium">{user.role_display}</div>
            </div>

            <button
              onClick={handleLogout}
              className="p-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-600 hover:text-slate-900 border border-slate-200 transition shadow-sm"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
