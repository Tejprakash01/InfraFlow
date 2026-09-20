import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { 
  FileText, Upload, Plus, CheckCircle2, Clock, 
  FolderGit2, Tag, User, ShieldCheck, Download, AlertCircle 
} from 'lucide-react';

export const DocumentManager = () => {
  const { user } = useAuth();
  const [documents, setDocuments] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState('');
  const [filterCategory, setFilterCategory] = useState('ALL');

  // Form State
  const [formData, setFormData] = useState({
    title: '',
    project: '',
    category: 'CORRESPONDENCE',
    comments: '',
    file: null,
  });

  const categories = [
    { value: 'ALL', label: 'All Documents' },
    { value: 'CONTRACT', label: 'Contract Documents' },
    { value: 'DRAWING', label: 'Engineering Drawings' },
    { value: 'WORK_PROGRAMME', label: 'Work Programmes' },
    { value: 'TEST_REPORT', label: 'Quality Test Reports' },
    { value: 'MEASUREMENT', label: 'Measurement Sheets' },
    { value: 'BILL', label: 'Bill Attachments' },
    { value: 'INSPECTION', label: 'Site Inspection Reports' },
    { value: 'CORRESPONDENCE', label: 'Official Correspondence' },
  ];

  const loadData = () => {
    setLoading(true);
    Promise.all([
      api.getDocuments(),
      api.getProjects(),
    ])
      .then(([docRes, projRes]) => {
        setDocuments(docRes.data?.results || docRes.data || []);
        const projList = projRes.data?.results || projRes.data || [];
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

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFormData({ ...formData, file: e.target.files[0] });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.title || !formData.project) {
      alert('Please provide a title and select a project.');
      return;
    }

    setUploading(true);
    const data = new FormData();
    data.append('title', formData.title);
    data.append('project', formData.project);
    data.append('category', formData.category);
    data.append('comments', formData.comments);
    if (formData.file) {
      data.append('file', formData.file);
    }

    try {
      await api.uploadDocument(data);
      setUploadSuccess('Document successfully uploaded & registered to official record!');
      setShowUploadModal(false);
      setFormData({
        title: '',
        project: projects[0]?.id || '',
        category: 'CORRESPONDENCE',
        comments: '',
        file: null,
      });
      loadData();
      setTimeout(() => setUploadSuccess(''), 4000);
    } catch (err) {
      console.error(err);
      alert('Failed to upload document. Please check fields and try again.');
    } finally {
      setUploading(false);
    }
  };

  const filteredDocs = filterCategory === 'ALL' 
    ? documents 
    : documents.filter(d => d.category === filterCategory);

  return (
    <div className="p-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
            <FileText className="w-7 h-7 text-blue-600" />
            Official Project Document Repository
          </h1>
          <p className="text-sm text-slate-500">
            Secure DMS for Contracts, Working Drawings, Test Certificates & Measurement Records
          </p>
        </div>

        <button
          onClick={() => setShowUploadModal(true)}
          className="btn-primary flex items-center gap-2 text-sm shadow-lg shadow-blue-500/20"
        >
          <Upload className="w-4 h-4" />
          Upload Official Document
        </button>
      </div>

      {uploadSuccess && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-3 text-emerald-700 text-sm">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{uploadSuccess}</span>
        </div>
      )}

      {/* Category Filters */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        {categories.map((c) => (
          <button
            key={c.value}
            onClick={() => setFilterCategory(c.value)}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
              filterCategory === c.value
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-slate-100 text-slate-500 hover:text-slate-900 hover:bg-slate-200'
            }`}
          >
            {c.label}
          </button>
        ))}
      </div>

      {/* Document Grid / Table */}
      {loading ? (
        <div className="p-12 text-center text-slate-500">Loading Documents...</div>
      ) : filteredDocs.length === 0 ? (
        <div className="glass-card p-12 text-center rounded-2xl">
          <FileText className="w-12 h-12 text-slate-400 mx-auto mb-3" />
          <h3 className="text-lg font-semibold text-slate-600">No Documents in this Category</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
            Upload contract drawings, test certificates or DPRs to build the permanent project audit trail.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDocs.map((doc) => (
            <div key={doc.id} className="glass-card p-5 rounded-2xl flex flex-col justify-between hover:border-blue-300 transition">
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="text-[10px] font-mono font-bold text-blue-600 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded">
                    {doc.category}
                  </span>
                  <span className="text-[10px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded font-mono">
                    v{doc.current_version_number || 1}
                  </span>
                </div>

                <h3 className="font-bold text-slate-900 text-sm line-clamp-2 mb-2">{doc.title}</h3>
                
                <div className="space-y-1.5 text-xs text-slate-500 mt-3 pt-3 border-t border-slate-200">
                  <div className="flex items-center gap-2">
                    <User className="w-3.5 h-3.5 text-slate-400" />
                    <span>Uploaded by: <strong className="text-slate-700">{doc.uploader_name || 'Official Officer'}</strong></span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="w-3.5 h-3.5 text-slate-400" />
                    <span>Date: {new Date(doc.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 flex items-center justify-between border-t border-slate-200">
                <span className="text-xs flex items-center gap-1 text-emerald-600">
                  <ShieldCheck className="w-4 h-4" /> Verified Record
                </span>
                <span className="text-xs text-blue-600 hover:underline cursor-pointer flex items-center gap-1 font-medium">
                  <Download className="w-3.5 h-3.5" /> View File
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Upload Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-black/30 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white max-w-lg w-full p-6 rounded-2xl border border-slate-200 shadow-2xl space-y-5">
            <div className="flex justify-between items-center pb-3 border-b border-slate-200">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Upload className="w-5 h-5 text-blue-600" />
                Upload Official Project Document
              </h2>
              <button 
                onClick={() => setShowUploadModal(false)}
                className="text-slate-400 hover:text-slate-700 text-xl font-bold"
              >
                &times;
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  Document Title *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Approved Alignment Drawing km 12+000"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-sm text-slate-800 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    Infrastructure Project *
                  </label>
                  <select
                    value={formData.project}
                    onChange={(e) => setFormData({ ...formData, project: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
                  >
                    {projects.map((p) => (
                      <option key={p.id} value={p.id}>{p.project_code} - {p.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">
                    Document Category *
                  </label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
                  >
                    {categories.filter(c => c.value !== 'ALL').map((c) => (
                      <option key={c.value} value={c.value}>{c.label}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  File Attachment (PDF, DWG, XLSX, ZIP)
                </label>
                <input
                  type="file"
                  onChange={handleFileChange}
                  className="w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer bg-slate-50 border border-slate-200 rounded-xl p-2"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  Submission Remarks / Scrutiny Notes
                </label>
                <textarea
                  rows="3"
                  placeholder="Mention revision notes, circular references or technical compliance..."
                  value={formData.comments}
                  onChange={(e) => setFormData({ ...formData, comments: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
                ></textarea>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-200">
                <button
                  type="button"
                  onClick={() => setShowUploadModal(false)}
                  className="btn-secondary text-xs"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={uploading}
                  className="btn-primary text-xs flex items-center gap-2"
                >
                  {uploading ? 'Uploading...' : 'Confirm & Upload'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
