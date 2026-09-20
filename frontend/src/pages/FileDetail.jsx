import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import {
  FileCheck, User, Calendar, Send, CheckCircle2, XCircle, MessageSquare,
  Clock, ShieldAlert, ArrowRight, CornerUpRight, Plus, Check
} from 'lucide-react';

export const FileDetail = () => {
  const { id } = useParams();
  const { user: currentUser } = useAuth();
  const [file, setFile] = useState(null);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('notes');

  // Modals & form state
  const [showForwardModal, setShowForwardModal] = useState(false);
  const [showApproveModal, setShowApproveModal] = useState(false);
  const [showRejectModal, setShowRejectModal] = useState(false);
  
  const [forwardRecipient, setForwardRecipient] = useState('');
  const [forwardAction, setForwardAction] = useState('FORWARD');
  const [forwardRemarks, setForwardRemarks] = useState('');
  const [forwardNote, setForwardNote] = useState('');
  const [recommendation, setRecommendation] = useState('RECOMMEND_APPROVAL');
  
  const [approveRemarks, setApproveRemarks] = useState('');
  const [rejectRemarks, setRejectRemarks] = useState('');
  const [rejectReason, setRejectReason] = useState('Technical / Measurement Non-Compliance');

  const [newNoteContent, setNewNoteContent] = useState('');
  const [submittingNote, setSubmittingNote] = useState(false);

  const fetchFile = () => {
    api.getFileDetail(id)
      .then((res) => setFile(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchFile();
    api.getUsers().then((res) => setUsers(res.data.results || res.data)).catch(() => {});
  }, [id]);

  const handleAddNote = async (e) => {
    e.preventDefault();
    if (!newNoteContent) return;
    setSubmittingNote(true);
    try {
      await api.addFileNote(id, newNoteContent, recommendation);
      setNewNoteContent('');
      fetchFile();
    } catch (err) {
      alert('Failed to add note');
    } finally {
      setSubmittingNote(false);
    }
  };

  const handleForwardSubmit = async (e) => {
    e.preventDefault();
    if (!forwardRecipient) return alert('Select recipient user');
    try {
      await api.forwardFile(id, {
        to_user_id: forwardRecipient,
        action: forwardAction,
        remarks: forwardRemarks,
        note_content: forwardNote,
        recommendation: recommendation
      });
      setShowForwardModal(false);
      fetchFile();
    } catch (err) {
      alert('Failed to forward file');
    }
  };

  const handleApproveSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.approveFile(id, approveRemarks);
      setShowApproveModal(false);
      fetchFile();
    } catch (err) {
      alert('Failed to record approval decision');
    }
  };

  const handleRejectSubmit = async (e) => {
    e.preventDefault();
    if (!rejectRemarks.trim()) return alert('Please enter review remarks for rejection');
    try {
      const fullRemarks = `[REJECTION REVIEW - ${rejectReason.toUpperCase()}]: ${rejectRemarks}`;
      await api.rejectFile(id, fullRemarks);
      setShowRejectModal(false);
      setRejectRemarks('');
      fetchFile();
    } catch (err) {
      alert('Failed to record rejection decision');
    }
  };

  if (loading) return <div className="p-8 text-slate-500">Loading Official Government File...</div>;
  if (!file) return <div className="p-8 text-rose-600">File Record Not Found</div>;

  const isCurrentHolder = currentUser?.id === file.current_holder;

  return (
    <div className="p-8 space-y-6">
      {/* File Header Card */}
      <div className="glass-card p-6 rounded-2xl space-y-4">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-200 pb-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className="font-mono text-sm font-extrabold text-blue-600 bg-blue-50 border border-blue-200 px-3 py-1 rounded-md">
                {file.file_number}
              </span>
              <span className={file.is_overdue ? 'badge-red' : 'badge-green'}>
                {file.is_overdue ? 'OVERDUE SLA' : file.status}
              </span>
              <span className={file.priority === 'URGENT' || file.priority === 'HIGH' ? 'badge-amber' : 'badge-blue'}>
                {file.priority}
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-900">{file.subject}</h1>
            <p className="text-xs text-slate-500 mt-1">Project: <span className="text-slate-700 font-semibold">{file.project_name}</span> ({file.project_code})</p>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-3">
            {isCurrentHolder && file.status !== 'APPROVED' && file.status !== 'REJECTED' && (
              <>
                <button
                  onClick={() => setShowForwardModal(true)}
                  className="btn-primary text-xs py-2.5"
                >
                  <Send className="w-4 h-4" /> Forward File
                </button>

                <button
                  onClick={() => setShowApproveModal(true)}
                  className="bg-emerald-600 hover:bg-emerald-500 text-white font-medium px-4 py-2.5 rounded-lg text-xs flex items-center gap-2 shadow-lg shadow-emerald-600/20"
                >
                  <CheckCircle2 className="w-4 h-4" /> Approve & Sanction
                </button>

                <button
                  onClick={() => setShowRejectModal(true)}
                  className="bg-rose-600 hover:bg-rose-500 text-white font-medium px-4 py-2.5 rounded-lg text-xs flex items-center gap-2 shadow-lg shadow-rose-600/20 transition"
                >
                  <XCircle className="w-4 h-4" /> Reject with Review
                </button>
              </>
            )}
          </div>
        </div>

        {/* Current Holder Details */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs bg-slate-50 p-4 rounded-xl border border-slate-200">
          <div>
            <span className="text-slate-500 block">Current Holder Officer</span>
            <span className="font-bold text-slate-800 text-sm">{file.current_holder_name}</span>
            <span className="text-slate-500 block">{file.current_holder_designation}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Originator Officer</span>
            <span className="font-bold text-slate-800 text-sm">{file.originator_name}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Confidentiality Level</span>
            <span className="font-bold text-blue-600 text-sm">{file.confidentiality}</span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-200 text-sm font-semibold text-slate-500 gap-6">
        <button
          onClick={() => setActiveTab('notes')}
          className={`pb-3 px-1 border-b-2 transition ${activeTab === 'notes' ? 'border-blue-600 text-blue-600' : 'border-transparent hover:text-slate-900'}`}
        >
          Note Sheets ({file.notes?.length || 0})
        </button>
        <button
          onClick={() => setActiveTab('movements')}
          className={`pb-3 px-1 border-b-2 transition ${activeTab === 'movements' ? 'border-blue-600 text-blue-600' : 'border-transparent hover:text-slate-900'}`}
        >
          Movement Log ({file.movements?.length || 0})
        </button>
        <button
          onClick={() => setActiveTab('decisions')}
          className={`pb-3 px-1 border-b-2 transition ${activeTab === 'decisions' ? 'border-blue-600 text-blue-600' : 'border-transparent hover:text-slate-900'}`}
        >
          Decisions & Sanctions ({file.decisions?.length || 0})
        </button>
      </div>

      {/* Tab Content: Note Sheets */}
      {activeTab === 'notes' && (
        <div className="space-y-6">
          {file.notes?.length === 0 ? (
            <div className="glass-card p-8 text-center text-slate-500">No notes written on this file yet.</div>
          ) : (
            file.notes?.map((note) => (
              <div key={note.id} className="glass-card p-6 rounded-2xl space-y-3 relative">
                <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="w-7 h-7 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center font-bold text-xs">
                      #{note.note_number}
                    </span>
                    <div>
                      <span className="font-bold text-slate-900 text-sm">{note.author_full_name}</span>
                      <span className="text-xs text-slate-500 ml-2">({note.author_designation})</span>
                    </div>
                  </div>
                  <span className="text-xs text-slate-500">{new Date(note.created_at).toLocaleString()}</span>
                </div>

                <div className="text-sm text-slate-700 whitespace-pre-wrap leading-relaxed">
                  {note.content}
                </div>

                {note.recommendation !== 'NEUTRAL' && (
                  <div className="bg-blue-50 border border-blue-200 p-2.5 rounded-lg text-xs text-blue-700 font-medium">
                    Recommendation: {note.recommendation.replace('_', ' ')}
                  </div>
                )}
              </div>
            ))
          )}

          {/* Add Note Form for Current Holder */}
          {isCurrentHolder && (
            <div className="glass-card p-6 rounded-2xl space-y-4">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <MessageSquare className="w-5 h-5 text-blue-600" /> Write Note Sheet Entry
              </h3>
              <form onSubmit={handleAddNote} className="space-y-4">
                <textarea
                  value={newNoteContent}
                  onChange={(e) => setNewNoteContent(e.target.value)}
                  placeholder="Enter official observation, examination remarks, or recommendation..."
                  rows={4}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-800 focus:outline-none focus:border-blue-500 transition"
                  required
                />
                <div className="flex justify-between items-center">
                  <select
                    value={recommendation}
                    onChange={(e) => setRecommendation(e.target.value)}
                    className="bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-700"
                  >
                    <option value="RECOMMEND_APPROVAL">Recommend Approval</option>
                    <option value="RECOMMEND_REJECTION">Recommend Rejection</option>
                    <option value="RECOMMEND_MODIFICATION">Recommend Modification</option>
                    <option value="NEUTRAL">For Information / Neutral</option>
                  </select>

                  <button
                    type="submit"
                    disabled={submittingNote}
                    className="btn-primary text-xs py-2"
                  >
                    <Plus className="w-4 h-4" /> Save Note Draft
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      )}

      {/* Tab Content: Movement Log */}
      {activeTab === 'movements' && (
        <div className="glass-card p-6 rounded-2xl space-y-6">
          <h3 className="text-base font-bold text-slate-900 mb-4">Official File Movement Audit Trail</h3>
          <div className="space-y-4 relative before:absolute before:left-4 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200">
            {file.movements?.map((m) => (
              <div key={m.id} className="relative pl-10 space-y-1">
                <div className="absolute left-2.5 top-1.5 w-3 h-3 bg-blue-500 rounded-full ring-4 ring-white"></div>
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-slate-900 text-sm">{m.action}</span>
                  <span className="text-slate-500">{new Date(m.timestamp).toLocaleString()}</span>
                </div>
                <div className="text-xs text-slate-600">
                  <span className="font-semibold text-blue-600">{m.from_user_name}</span> &rarr; <span className="font-semibold text-blue-600">{m.to_user_name}</span>
                </div>
                {m.remarks && <div className="text-xs text-slate-500 italic bg-slate-50 p-2 rounded mt-1">{m.remarks}</div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab Content: Decisions & Approvals */}
      {activeTab === 'decisions' && (
        <div className="glass-card p-6 rounded-2xl space-y-4">
          <h3 className="text-base font-bold text-slate-900">Competent Authority Decisions</h3>
          {file.decisions?.length === 0 ? (
            <div className="text-sm text-slate-500 py-6 text-center">No final approval or rejection decisions recorded yet.</div>
          ) : (
            file.decisions?.map((d) => {
              const isRejected = d.decision_type === 'REJECTED';
              return (
                <div key={d.id} className={`p-4 rounded-xl space-y-2 ${isRejected ? 'bg-rose-50 border border-rose-200' : 'bg-emerald-50 border border-emerald-200'}`}>
                  <div className="flex items-center justify-between">
                    <span className={`font-bold text-sm flex items-center gap-2 ${isRejected ? 'text-rose-700' : 'text-emerald-700'}`}>
                      {isRejected ? <XCircle className="w-5 h-5 text-rose-600" /> : <CheckCircle2 className="w-5 h-5 text-emerald-600" />}
                      {d.decision_type}
                    </span>
                    <span className="text-xs text-slate-500">{new Date(d.timestamp).toLocaleString()}</span>
                  </div>
                  <div className="text-xs text-slate-600">Decision By: <span className="font-semibold text-slate-900">{d.decision_by_name}</span></div>
                  <div className="text-sm text-slate-700 whitespace-pre-wrap">{d.remarks}</div>
                </div>
              );
            })
          )}
        </div>
      )}

      {/* Forward File Modal */}
      {showForwardModal && (
        <div className="fixed inset-0 z-50 bg-black/30 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white p-6 rounded-2xl max-w-lg w-full space-y-4 border border-slate-200 shadow-2xl">
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Send className="w-5 h-5 text-blue-600" /> Forward Government File
            </h3>
            <form onSubmit={handleForwardSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-500 mb-1 uppercase">Target Recipient Officer</label>
                <select
                  value={forwardRecipient}
                  onChange={(e) => setForwardRecipient(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm text-slate-800"
                  required
                >
                  <option value="">Select Officer...</option>
                  {users.map((u) => (
                    <option key={u.id} value={u.id}>{u.first_name} {u.last_name} ({u.role_display})</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-500 mb-1 uppercase">Action Type</label>
                <input
                  type="text"
                  value={forwardAction}
                  onChange={(e) => setForwardAction(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm text-slate-800"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-500 mb-1 uppercase">Optional Forwarding Note Sheet Entry</label>
                <textarea
                  value={forwardNote}
                  onChange={(e) => setForwardNote(e.target.value)}
                  rows={3}
                  placeholder="Attach official note entry with forwarding..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm text-slate-800"
                />
              </div>

              <div className="flex justify-end gap-3 pt-2">
                <button type="button" onClick={() => setShowForwardModal(false)} className="btn-secondary text-xs">Cancel</button>
                <button type="submit" className="btn-primary text-xs">Confirm & Forward</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Approve Sanction Modal */}
      {showApproveModal && (
        <div className="fixed inset-0 z-50 bg-black/30 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white p-6 rounded-2xl max-w-lg w-full space-y-4 border border-emerald-200 shadow-2xl">
            <h3 className="text-lg font-bold text-emerald-700 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5" /> Official Approval & Sanction
            </h3>
            <form onSubmit={handleApproveSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-500 mb-1 uppercase">Sanction Remarks / Order</label>
                <textarea
                  value={approveRemarks}
                  onChange={(e) => setApproveRemarks(e.target.value)}
                  rows={4}
                  placeholder="Enter official sanction decision remarks..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm text-slate-800"
                  required
                />
              </div>

              <div className="flex justify-end gap-3 pt-2">
                <button type="button" onClick={() => setShowApproveModal(false)} className="btn-secondary text-xs">Cancel</button>
                <button type="submit" className="bg-emerald-600 hover:bg-emerald-500 text-white font-medium px-4 py-2 rounded-lg text-xs">
                  Issue Official Approval
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Reject Sanction Modal */}
      {showRejectModal && (
        <div className="fixed inset-0 z-50 bg-black/30 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white p-6 rounded-2xl max-w-lg w-full space-y-4 border border-rose-200 shadow-2xl">
            <h3 className="text-lg font-bold text-rose-700 flex items-center gap-2">
              <XCircle className="w-5 h-5 text-rose-600" /> Official File Rejection & Review
            </h3>
            <p className="text-xs text-slate-500">
              Official review objections and non-compliance grounds will be registered into the audit log and the file marked as Rejected.
            </p>
            <form onSubmit={handleRejectSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1 uppercase">Rejection Grounds / Category *</label>
                <select
                  value={rejectReason}
                  onChange={(e) => setRejectReason(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm text-slate-800 focus:outline-none focus:border-rose-500"
                >
                  <option value="Technical / Measurement Non-Compliance">Technical / Measurement Non-Compliance</option>
                  <option value="Financial / Tax Scrutiny Discrepancy">Financial / Tax Scrutiny Discrepancy</option>
                  <option value="Incomplete Documentation / Missing Drawings">Incomplete Documentation / Missing Drawings</option>
                  <option value="Quality Test / Specification Failure">Quality Test / Specification Failure</option>
                  <option value="Budget / Fund Allocation Exhausted">Budget / Fund Allocation Exhausted</option>
                  <option value="Administrative / Competent Authority Disapproval">Administrative / Competent Authority Disapproval</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1 uppercase">Department Review Remarks & Justification *</label>
                <textarea
                  value={rejectRemarks}
                  onChange={(e) => setRejectRemarks(e.target.value)}
                  rows={4}
                  placeholder="Enter specific departmental review objections, observed discrepancies, or non-compliance clauses..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm text-slate-800 focus:outline-none focus:border-rose-500"
                  required
                />
              </div>

              <div className="flex justify-end gap-3 pt-2">
                <button type="button" onClick={() => setShowRejectModal(false)} className="btn-secondary text-xs">Cancel</button>
                <button type="submit" className="bg-rose-600 hover:bg-rose-500 text-white font-medium px-4 py-2 rounded-lg text-xs shadow-lg shadow-rose-600/20">
                  Confirm Official Rejection
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
