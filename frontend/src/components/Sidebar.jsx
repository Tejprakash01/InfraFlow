import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Inbox, LayoutDashboard, FolderGit2, FileCheck, Receipt,
  ClipboardCheck, ShieldAlert, PieChart, Users, HardHat,
  ShieldCheck, FileText
} from 'lucide-react';

export const Sidebar = () => {
  const { user } = useAuth();
  const isContractor = user?.is_contractor_user;
  const isAdmin = user?.role === 'HQ_ADMIN' || user?.is_superuser || user?.role === 'PROJECT_DIRECTOR';

  const govLinks = [
    ...(isAdmin ? [{ to: '/admin', label: 'Admin Portal', icon: ShieldCheck }] : []),
    { to: '/work-desk', label: 'My Work Desk', icon: Inbox },
    { to: '/executive-dashboard', label: 'Executive Dashboard', icon: LayoutDashboard },
    { to: '/projects', label: 'Projects', icon: FolderGit2 },
    { to: '/documents', label: 'Official Documents', icon: FileText },
    { to: '/files', label: 'Government Files', icon: FileCheck },
    { to: '/bills', label: 'RA Bills & Payments', icon: Receipt },
    { to: '/rfis', label: 'RFIs & Inspections', icon: ClipboardCheck },
    { to: '/ncrs', label: 'NCRs & Quality', icon: ShieldAlert },
  ];

  const contractorLinks = [
    { to: '/contractor/dashboard', label: 'Contractor Portal', icon: HardHat },
    { to: '/projects', label: 'Assigned Projects', icon: FolderGit2 },
    { to: '/documents', label: 'Project Documents', icon: FileText },
    { to: '/bills', label: 'Submitted Bills', icon: Receipt },
    { to: '/rfis', label: 'Site RFIs', icon: ClipboardCheck },
    { to: '/ncrs', label: 'Quality NCRs', icon: ShieldAlert },
  ];

  const links = isContractor ? contractorLinks : govLinks;

  return (
    <aside className="w-64 bg-white border-r border-slate-200 min-h-[calc(100vh-61px)] p-4 flex flex-col justify-between shadow-sm">
      <div className="space-y-1">
        <div className="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
          Navigation
        </div>
        {links.map((link) => {
          const Icon = link.icon;
          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-lg font-medium text-sm transition duration-150 ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{link.label}</span>
            </NavLink>
          );
        })}
      </div>

      <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-500">
        <div className="font-semibold text-slate-700 mb-1">InfraFlow v1.0 MVP</div>
        <div>NHAI/PWD Operations Core</div>
      </div>
    </aside>
  );
};
