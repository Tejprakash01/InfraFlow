import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const client = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  login: (username, password) => client.post('/auth/login/', { username, password }),
  getProfile: () => client.get('/auth/me/'),
  getWorkDesk: () => client.get('/files/files/work_desk/'),
  getProjects: () => client.get('/projects/projects/'),
  getProjectDetail: (id) => client.get(`/projects/projects/${id}/`),
  getFiles: () => client.get('/files/files/'),
  getFileDetail: (id) => client.get(`/files/files/${id}/`),
  addFileNote: (id, content, recommendation) => client.post(`/files/files/${id}/add_note/`, { content, recommendation }),
  forwardFile: (id, payload) => client.post(`/files/files/${id}/forward/`, payload),
  approveFile: (id, remarks, decision_type = 'APPROVED') => client.post(`/files/files/${id}/approve/`, { remarks, decision_type }),
  rejectFile: (id, remarks) => client.post(`/files/files/${id}/approve/`, { remarks, decision_type: 'REJECTED' }),
  getBills: () => client.get('/billing/bills/'),
  getExecutiveDashboard: () => client.get('/reports/dashboard/executive/'),
  getContractorDashboard: () => client.get('/reports/dashboard/contractor/'),
  getRFIs: () => client.get('/quality/rfis/'),
  getNCRs: () => client.get('/quality/ncrs/'),
  getUsers: () => client.get('/auth/users/'),
  getOrganizations: () => client.get('/organizations/organizations/'),
  getDepartments: () => client.get('/organizations/departments/'),
  getOffices: () => client.get('/organizations/offices/'),
  getAuditLogs: () => client.get('/audit/logs/'),
  getNotifications: () => client.get('/notifications/notifications/'),
  getDocuments: () => client.get('/documents/documents/'),
  uploadDocument: (formData) => client.post('/documents/documents/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  createBill: (data) => client.post('/billing/bills/', data),
  createFile: (data) => client.post('/files/files/', data),
  createProject: (data) => client.post('/projects/projects/', data),
  createRFI: (data) => client.post('/quality/rfis/', data),
  createNCR: (data) => client.post('/quality/ncrs/', data),
  getWorkflows: () => client.get('/workflows/definitions/'),
  getSLAs: () => client.get('/workflows/sla-policies/'),
};

export default client;
