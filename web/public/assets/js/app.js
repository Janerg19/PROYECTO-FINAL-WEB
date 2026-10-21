/* ============================================================
   APP JS - VERSIÓN CON API REAL
   ============================================================ */

/* ============================================================
   API CLIENT
   Cliente fetch con manejo de token y errores
   ============================================================ */

const API_BASE = '/api';

let token = localStorage.getItem('riul_token');

const setToken = (newToken) => {
  token = newToken;
  if (newToken) {
    localStorage.setItem('riul_token', newToken);
  } else {
    localStorage.removeItem('riul_token');
  }
};

const getToken = () => token;

const apiCall = async (endpoint, options = {}) => {
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
const authAPI = {
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
const publicacionesAPI = {
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
const semillerosAPI = {
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
const logrosAPI = {
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
const adminAPI = {
  getCuentasPendientes: () => apiCall('/admin/cuentas-pendientes'),
  aprobarCuenta: (id) => apiCall(`/admin/cuentas/${id}/aprobar`, { method: 'POST' }),
  rechazarCuenta: (id) => apiCall(`/admin/cuentas/${id}/rechazar`, { method: 'POST' }),
  getFacultades: () => apiCall('/admin/facultades'),
  getProgramas: (params) => apiCall(`/admin/programas?${new URLSearchParams(params)}`),
};

// Ranking
const rankingAPI = {
  getSemilleros: () => apiCall('/ranking/semilleros'),
  getInvestigadores: () => apiCall('/ranking/investigadores'),
  getKPIs: () => apiCall('/ranking/kpis'),
  getIndicadoresFacultad: () => apiCall('/ranking/indicadores-facultad'),
  getHojaVida: (id) => apiCall(`/ranking/hoja-vida/${id}`),
};

/* ============================================================
   STATE
   ============================================================ */
const state = {
  user: null,
  token: null,
  role: null,
  currentView: 'dashboard',
};

const NAV = [
  {id:'dashboard', label:'Dashboard', icon:'i-home', roles:['estudiante','docente','administrador','visitante']},
  {id:'perfil', label:'Mi perfil', icon:'i-user', roles:['estudiante','docente']},
  {id:'semillero', label:'Semillero', icon:'i-flask', roles:['docente']},
  {id:'publicaciones', label:'Publicaciones', icon:'i-doc', roles:['estudiante','docente','administrador','visitante']},
  {id:'eventos', label:'Eventos y convocatorias', icon:'i-cal', roles:['estudiante','docente','administrador','visitante']},
  {id:'gamificacion', label:'Gamificación', icon:'i-trophy', roles:['estudiante','docente']},
  {id:'admin', label:'Validaciones', icon:'i-shield', roles:['administrador']},
  {id:'ranking', label:'Ranking', icon:'i-chart', roles:['estudiante','docente','administrador','visitante']}
];

const ROLE_LABEL = {estudiante:'Estudiante investigador', docente:'Docente líder', administrador:'Administrador', visitante:'Visitante'};

/* ============================================================
   LOGIN
   ============================================================ */
function showRegister(){
  document.getElementById('login-step-in').style.display='none';
  document.getElementById('login-step-register').style.display='block';
}

function showLogin(){
  document.getElementById('login-step-in').style.display='block';
  document.getElementById('login-step-register').style.display='none';
}

async function submitRegister(){
  const nombres = document.getElementById('reg-nombres').value;
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;
  const programa = document.getElementById('reg-programa').value;

  if (!nombres || !email || !password) {
    toast('Por favor completa todos los campos obligatorios');
    return;
  }

  try {
    await authAPI.register({ nombres, apellidos: nombres, email, password, programa_id: 1 });
    toast('Solicitud enviada. Un administrador debe validarla.');
    showLogin();
    
    // Limpiar campos
    document.getElementById('reg-nombres').value = '';
    document.getElementById('reg-email').value = '';
    document.getElementById('reg-password').value = '';
    document.getElementById('reg-programa').value = '';
    document.getElementById('reg-documento').value = '';
  } catch (error) {
    toast(error.error || 'Error al registrar');
  }
}

async function login(){
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  try {
    const data = await authAPI.login({ email, password });
    state.token = data.token;
    state.user = data.usuario;
    state.role = data.usuario.rol;
    setToken(data.token);

    document.getElementById('view-login').style.display='none';
    document.getElementById('shell').classList.add('active');

    updateUserUI();
    loadDashboard();
    toast('Bienvenid@ a RIUL');
  } catch (error) {
    toast(error.error || 'Error al iniciar sesión');
  }
}

function logout(){
  state.token = null;
  state.user = null;
  state.role = null;
  setToken(null);

  document.getElementById('view-login').style.display='grid';
  document.getElementById('shell').classList.remove('active');
  showLogin();
}

function setRole(role){
  // Función vacía - el rol se determina automáticamente por el usuario
  console.log('Rol determinado automáticamente por el usuario:', role);
}

/* ============================================================
   UI HELPERS
   ============================================================ */
function updateUserUI(){
  if (!state.user) return;

  const av = document.getElementById('topbar-avatar');
  av.textContent = state.user.nombres[0] + state.user.apellidos[0];
  av.style.background = 'var(--ink)';

  document.getElementById('dash-title').textContent = `Bienvenid@, ${state.user.nombres}`;
  document.getElementById('kpi-xp').textContent = state.user.xp_total.toLocaleString();
  document.getElementById('kpi-level').textContent = `${state.user.nivel} / 5`;

  renderSidebar();
}

function renderSidebar(){
  const sb = document.getElementById('sidebar');
  sb.innerHTML = '';
  NAV.filter(n=>n.roles.includes(state.role)).forEach(n=>{
    const b = document.createElement('button');
    b.className = 'nav-item' + (n.id===state.currentView ? ' active':'');
    b.innerHTML = `<svg class="icon"><use href="#${n.icon}"/></svg>${n.label}`;
    b.onclick = ()=>showView(n.id);
    sb.appendChild(b);
  });
  const foot = document.createElement('div');
  foot.className = 'sidebar-footer small';
  foot.innerHTML = `Sesión activa como<br><b style="color:var(--ink)">${ROLE_LABEL[state.role]}</b>`;
  sb.appendChild(foot);
}

function showView(id){
  state.currentView = id;
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.getElementById('view-'+id).classList.add('active');
  renderSidebar();

  // Cargar datos según vista
  if (id === 'publicaciones') loadPublicaciones();
  if (id === 'ranking') loadRanking();
  if (id === 'admin') loadAdmin();
}

/* ============================================================
   DATA LOADING
   ============================================================ */
async function loadDashboard(){
  try {
    const kpis = await rankingAPI.getKPIs();
    // Actualizar KPIs si es necesario
  } catch (error) {
    console.error('Error loading dashboard:', error);
  }
}

async function loadPublicaciones(){
  try {
    const posts = await publicacionesAPI.getAll();
    renderFeed(posts);
  } catch (error) {
    console.error('Error loading publicaciones:', error);
  }
}

async function loadRanking(){
  try {
    const semilleros = await rankingAPI.getSemilleros();
    renderRankingTable(semilleros);
  } catch (error) {
    console.error('Error loading ranking:', error);
  }
}

async function loadAdmin(){
  try {
    const cuentas = await adminAPI.getCuentasPendientes();
    const logros = await logrosAPI.getPendientes();
    renderAdminTables(cuentas, logros);
  } catch (error) {
    console.error('Error loading admin:', error);
  }
}

/* ============================================================
   RENDER FUNCTIONS
   ============================================================ */
function renderFeed(posts){
  const feedHtml = posts.map(p => `
    <div class="post">
      <div class="post-head">
        <div class="avatar" style="width:32px;height:32px;font-size:12px;background:var(--ink)">${p.nombres[0]}</div>
        <div><div class="who">${p.nombres} ${p.apellidos}</div><div class="when">hace un momento</div></div>
        <span class="chip chip-accent" style="margin-left:auto">${p.categoria}</span>
      </div>
      <div style="font-weight:600;font-size:15px;margin-bottom:4px">${p.titulo}</div>
      <p class="small" style="margin:0 0 4px">${p.contenido}</p>
      <div class="post-actions">
        <span>♥ Reaccionar</span><span>💬 Comentar</span><span>↗ Compartir</span>
      </div>
    </div>
  `).join('');

  document.getElementById('feed-full').innerHTML = feedHtml;
  document.getElementById('dash-feed').innerHTML = feedHtml;
}

function renderRankingTable(semilleros){
  const html = semilleros.map((s, i) => `
    <tr>
      <td class="mono" style="font-weight:700;color:${i<3?'var(--rose)':'var(--ink)'}">${i+1}</td>
      <td class="flex gap12 center" style="border:none;padding-top:13px">
        <div class="avatar" style="width:26px;height:26px;font-size:10px;background:var(--ink-soft)">${s.semillero_nombre.slice(0,2)}</div>
        ${s.semillero_nombre}
      </td>
      <td>${s.facultad}</td>
      <td class="mono">${s.xp_total.toLocaleString()}</td>
      <td>${s.estrellas} ★</td>
    </tr>
  `).join('');

  document.getElementById('tabla-ranking').innerHTML = html;
}

function renderAdminTables(cuentas, logros){
  // Cuentas pendientes
  const cuentasHtml = cuentas.map(c => `
    <tr>
      <td>${c.nombres} ${c.apellidos}</td>
      <td class="mono" style="font-size:12.5px">${c.email}</td>
      <td><span class="chip chip-muted">${c.rol_solicitado}</span></td>
      <td class="small">carnet.pdf</td>
      <td class="flex gap8">
        <button class="btn btn-primary btn-sm" onclick="aprobarCuenta(${c.usuario_id})">Aprobar</button>
        <button class="btn btn-outline btn-sm" onclick="rechazarCuenta(${c.usuario_id})">Rechazar</button>
      </td>
    </tr>
  `).join('');

  document.getElementById('tabla-cuentas').innerHTML = cuentasHtml;
  document.getElementById('count-cuentas').textContent = `(${cuentas.length})`;
  document.getElementById('empty-cuentas').style.display = cuentas.length ? 'none' : 'block';

  // Logros pendientes
  const logrosHtml = logros.map(l => `
    <tr>
      <td>${l.nombres} ${l.apellidos}</td>
      <td><span class="chip chip-accent">${l.tipo}</span></td>
      <td class="small">${l.titulo}</td>
      <td class="flex gap8">
        <button class="btn btn-primary btn-sm" onclick="aprobarLogro(${l.logro_id})">Aprobar</button>
        <button class="btn btn-outline btn-sm" onclick="rechazarLogro(${l.logro_id})">Rechazar</button>
      </td>
    </tr>
  `).join('');

  document.getElementById('tabla-logros').innerHTML = logrosHtml;
  document.getElementById('count-logros').textContent = `(${logros.length})`;
  document.getElementById('empty-logros').style.display = logros.length ? 'none' : 'block';
}

/* ============================================================
   ACTIONS
   ============================================================ */
function openModal(id){
  document.getElementById(id).classList.add('active');
}

function closeModal(id){
  document.getElementById(id).classList.remove('active');
}

async function submitPost(){
  const categoria = document.querySelector('#post-cat-picker button.sel')?.dataset.cat || 'Logro';
  const titulo = document.getElementById('post-title').value.trim();
  const contenido = document.getElementById('post-body').value.trim();

  if (!titulo) {
    toast('Escribe un título para tu publicación');
    return;
  }

  try {
    await publicacionesAPI.create({
      categoria_id: 1, // Simplificado: asume Logro = 1
      titulo,
      contenido,
    });
    document.getElementById('post-title').value = '';
    document.getElementById('post-body').value = '';
    closeModal('modal-post');
    loadPublicaciones();
    toast('Publicación creada');
  } catch (error) {
    toast(error.error || 'Error al crear publicación');
  }
}

async function submitLogro(){
  const tipo = document.getElementById('logro-tipo').value;
  const titulo = document.getElementById('logro-titulo').value.trim();

  if (!titulo) {
    toast('Describe el logro antes de enviarlo');
    return;
  }

  try {
    await logrosAPI.enviar({ tipo, titulo, descripcion: '' });
    document.getElementById('logro-titulo').value = '';
    toast('Logro enviado a validación del administrador');
  } catch (error) {
    toast(error.error || 'Error al enviar logro');
  }
}

async function aprobarCuenta(id){
  try {
    await adminAPI.aprobarCuenta(id);
    loadAdmin();
    toast('Cuenta aprobada');
  } catch (error) {
    toast(error.error || 'Error al aprobar cuenta');
  }
}

async function rechazarCuenta(id){
  try {
    await adminAPI.rechazarCuenta(id);
    loadAdmin();
    toast('Cuenta rechazada');
  } catch (error) {
    toast(error.error || 'Error al rechazar cuenta');
  }
}

async function aprobarLogro(id){
  try {
    await logrosAPI.aprobar(id);
    loadAdmin();
    toast('Logro aprobado, XP asignado');
  } catch (error) {
    toast(error.error || 'Error al aprobar logro');
  }
}

async function rechazarLogro(id){
  try {
    await logrosAPI.rechazar(id);
    loadAdmin();
    toast('Logro rechazado');
  } catch (error) {
    toast(error.error || 'Error al rechazar logro');
  }
}

function toast(msg){
  const wrap = document.getElementById('toast-wrap');
  const t = document.createElement('div');
  t.className='toast';
  t.innerHTML = `<span class="dot"></span>${msg}`;
  wrap.appendChild(t);
  setTimeout(()=>{
    t.style.opacity='0';
    t.style.transform='translateY(10px)';
    t.style.transition='.3s';
    setTimeout(()=>t.remove(),300);
  }, 2600);
}

// Exponer funciones al window para que funcionen los onclick del HTML
window.login = login;
window.logout = logout;
window.showRegister = showRegister;
window.showLogin = showLogin;
window.submitRegister = submitRegister;
window.submitPost = submitPost;
window.submitLogro = submitLogro;
window.aprobarCuenta = aprobarCuenta;
window.rechazarCuenta = rechazarCuenta;
window.aprobarLogro = aprobarLogro;
window.rechazarLogro = rechazarLogro;
window.openModal = openModal;
window.closeModal = closeModal;
window.setRole = setRole;

/* ============================================================
   INIT
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  // Verificar si hay token guardado
  const savedToken = getToken();
  if (savedToken) {
    state.token = savedToken;
    authAPI.getMe()
      .then(data => {
        state.user = data.usuario;
        state.role = data.usuario.rol;
        document.getElementById('view-login').style.display='none';
        document.getElementById('shell').classList.add('active');
        updateUserUI();
        loadDashboard();
      })
      .catch(() => {
        setToken(null);
      });
  }
});
