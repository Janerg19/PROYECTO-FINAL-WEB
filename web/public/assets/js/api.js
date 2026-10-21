/* ============================================================
   API CLIENT
   Cliente fetch con manejo de token y errores
   ============================================================ */

const API_BASE = '/api';

let token = localStorage.getItem('riul_token');

export const setToken = (newToken) => {
  token = newToken;
  if (newToken) {
    localStorage.setItem('riul_token', newToken);
  } else {
    localStorage.removeItem('riul_token');
  }
};

export const getToken = () => token;

export const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Error desconocido' }));
    throw error;
  }

  return response.json();
};

// Auth
export const authAPI = {
  register: (data) => apiCall('/auth/register', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  login: (data) => apiCall('/auth/login', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  getMe: () => apiCall('/auth/me'),
};

// Publicaciones
export const publicacionesAPI = {
  getAll: () => apiCall('/publicaciones'),
  create: (data) => apiCall('/publicaciones', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  comentar: (data) => apiCall('/publicaciones/comentar', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  reaccionar: (data) => apiCall('/publicaciones/reaccionar', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  compartir: (data) => apiCall('/publicaciones/compartir', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
};

// Semilleros
export const semillerosAPI = {
  getAll: () => apiCall('/semilleros'),
  getById: (id) => apiCall(`/semilleros/${id}`),
  solicitarVinculacion: (data) => apiCall('/semilleros/solicitar-vinculacion', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  getIntegrantes: (id) => apiCall(`/semilleros/${id}/integrantes`),
  resolverVinculacion: (data) => apiCall('/semilleros/resolver-vinculacion', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
};

// Logros
export const logrosAPI = {
  getPendientes: () => apiCall('/logros/pendientes'),
  enviar: (data) => apiCall('/logros', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  getMisLogros: () => apiCall('/logros/mis-logros'),
  aprobar: (id) => apiCall(`/logros/${id}/aprobar`, { method: 'POST' }),
  rechazar: (id) => apiCall(`/logros/${id}/rechazar`, { method: 'POST' }),
};

// Admin
export const adminAPI = {
  getCuentasPendientes: () => apiCall('/admin/cuentas-pendientes'),
  aprobarCuenta: (id) => apiCall(`/admin/cuentas/${id}/aprobar`, { method: 'POST' }),
  rechazarCuenta: (id) => apiCall(`/admin/cuentas/${id}/rechazar`, { method: 'POST' }),
  getFacultades: () => apiCall('/admin/facultades'),
  getProgramas: (params) => apiCall(`/admin/programas?${new URLSearchParams(params)}`),
};

// Ranking
export const rankingAPI = {
  getSemilleros: () => apiCall('/ranking/semilleros'),
  getInvestigadores: () => apiCall('/ranking/investigadores'),
  getKPIs: () => apiCall('/ranking/kpis'),
  getIndicadoresFacultad: () => apiCall('/ranking/indicadores-facultad'),
  getHojaVida: (id) => apiCall(`/ranking/hoja-vida/${id}`),
};
