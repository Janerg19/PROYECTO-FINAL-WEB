/* ============================================================
   STATE
   ============================================================ */
const state = {
  role: 'estudiante',
  loginRole: 'estudiante',
  xp: 1240,
  xpNext: 2000,
  level: 3,
  postCategory: 'Logro',
  posts: [
    {who:'Semillero RIUL-Dev', when:'hace 2 días', cat:'Logro', catClass:'chip-accent', color:'var(--accent-soft)', title:'Artículo aceptado en revista indexada', body:'El artículo sobre trazabilidad académica fue aceptado para publicación en la revista de la facultad.'},
    {who:'Laura Gómez', when:'hace 4 días', cat:'Proyecto', catClass:'chip-teal', color:'var(--teal-soft)', title:'Avance del prototipo de dashboard', body:'Compartimos capturas del dashboard institucional en su primera versión funcional.'},
    {who:'Semillero BioUL', when:'hace 6 días', cat:'Evento', catClass:'chip-rose', color:'var(--rose-soft)', title:'Participación en coloquio nacional', body:'Presentamos resultados preliminares del proyecto de bioinformática en el coloquio nacional de semilleros.'}
  ],
  pendingLogros: [
    {tipo:'Ponencia', titulo:'Congreso Nacional de Ingeniería de Software', estado:'Pendiente'}
  ],
  adminCuentas: [
    {nombre:'Camilo Rojas', correo:'camilo.rojas@unilibre.edu.co', rol:'Estudiante'},
    {nombre:'Ana Martínez', correo:'ana.martinez@unilibre.edu.co', rol:'Docente'},
    {nombre:'David Ruiz', correo:'david.ruiz@unilibre.edu.co', rol:'Estudiante'},
    {nombre:'Paula León', correo:'paula.leon@unilibre.edu.co', rol:'Estudiante'}
  ],
  adminLogros: [
    {estudiante:'Juan Torres', tipo:'Artículo', desc:'Optimización de consultas SQL en sistemas académicos'},
    {estudiante:'Sara Peña', tipo:'Patente', desc:'Sistema de monitoreo IoT para laboratorios'},
    {estudiante:'Iván Cárdenas', tipo:'Ponencia', desc:'Aprendizaje automático aplicado a deserción estudiantil'}
  ],
  ranking: [
    {nombre:'RIUL-Dev', facultad:'Ingeniería', xp:2180, nivel:5},
    {nombre:'BioUL', facultad:'Ciencias', xp:1990, nivel:4},
    {nombre:'Derecho Aplicado', facultad:'Derecho', xp:1870, nivel:4},
    {nombre:'EcoSemillero', facultad:'Economía', xp:1640, nivel:3},
    {nombre:'NeuroLab', facultad:'Psicología', xp:1520, nivel:3},
    {nombre:'DataMind', facultad:'Ingeniería', xp:1410, nivel:3},
    {nombre:'Salud Comunitaria', facultad:'Medicina', xp:1225, nivel:2},
    {nombre:'AgroInvestiga', facultad:'Ciencias Agrarias', xp:980, nivel:2}
  ],
  rankSort: {key:null, dir:1}
};

const NAV = [
  {id:'dashboard', label:'Dashboard', icon:'i-home', roles:['estudiante','docente','admin','visitante']},
  {id:'perfil', label:'Mi perfil', icon:'i-user', roles:['estudiante','docente']},
  {id:'semillero', label:'Semillero', icon:'i-flask', roles:['docente']},
  {id:'publicaciones', label:'Publicaciones', icon:'i-doc', roles:['estudiante','docente','admin','visitante']},
  {id:'eventos', label:'Eventos y convocatorias', icon:'i-cal', roles:['estudiante','docente','admin','visitante']},
  {id:'gamificacion', label:'Gamificación', icon:'i-trophy', roles:['estudiante','docente']},
  {id:'admin', label:'Validaciones', icon:'i-shield', roles:['admin']},
  {id:'ranking', label:'Ranking', icon:'i-chart', roles:['estudiante','docente','admin','visitante']}
];
const ROLE_LABEL = {estudiante:'Estudiante investigador', docente:'Docente líder', admin:'Administrador', visitante:'Visitante'};
const ROLE_INITIALS = {estudiante:'JD', docente:'AM', admin:'AD', visitante:'VS'};
const ROLE_COLOR = {estudiante:'var(--ink)', docente:'var(--teal)', admin:'var(--rose)', visitante:'var(--ink-soft)'};

let currentView = 'dashboard';

/* ============================================================
   LOGIN
   ============================================================ */
function pickLoginRole(btn, role){
  document.querySelectorAll('.role-pick button').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  state.loginRole = role;
}
function showRegister(){ document.getElementById('login-step-in').style.display='none'; document.getElementById('login-step-register').style.display='block'; }
function showLogin(){ document.getElementById('login-step-in').style.display='block'; document.getElementById('login-step-register').style.display='none'; }
function submitRegister(){ toast('Solicitud enviada. Un administrador debe validarla.'); showLogin(); }

function login(){
  state.role = state.loginRole;
  document.getElementById('view-login').style.display='none';
  document.getElementById('shell').classList.add('active');
  setRole(state.role);
  renderAll();
  toast('Bienvenida a RIUL, ' + ROLE_LABEL[state.role]);
}
function logout(){
  document.getElementById('view-login').style.display='grid';
  document.getElementById('shell').classList.remove('active');
  showLogin();
}

/* ============================================================
   ROLE + NAVIGATION
   ============================================================ */
function setRole(role){
  state.role = role;
  document.querySelectorAll('.role-switch button').forEach(b=>b.classList.remove('active'));
  document.getElementById('rs-'+role).classList.add('active');

  const av = document.getElementById('topbar-avatar');
  av.textContent = ROLE_INITIALS[role];
  av.style.background = ROLE_COLOR[role];

  renderSidebar();
  const allowed = NAV.filter(n=>n.roles.includes(role)).map(n=>n.id);
  if(!allowed.includes(currentView)) showView('dashboard');

  document.getElementById('btn-crear-pub').style.display = (role==='visitante') ? 'none' : 'inline-flex';
}

function renderSidebar(){
  const sb = document.getElementById('sidebar');
  sb.innerHTML = '';
  NAV.filter(n=>n.roles.includes(state.role)).forEach(n=>{
    const b = document.createElement('button');
    b.className = 'nav-item' + (n.id===currentView ? ' active':'');
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
  currentView = id;
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.getElementById('view-'+id).classList.add('active');
  renderSidebar();
}

/* ============================================================
   RENDER HELPERS
   ============================================================ */
function starsSvg(filled, total=5, size=16, activeColor='var(--accent)', emptyColor='var(--border)'){
  let html='';
  for(let i=0;i<total;i++){
    html += `<svg viewBox="0 0 24 24" style="width:${size}px;height:${size}px;fill:${i<filled?activeColor:emptyColor}"><use href="#i-star"/></svg>`;
  }
  return html;
}

function postCard(p){
  return `<div class="post">
    <div class="post-head">
      <div class="avatar" style="width:32px;height:32px;font-size:12px;background:var(--ink)">${p.who.slice(0,1)}</div>
      <div><div class="who">${p.who}</div><div class="when">${p.when}</div></div>
      <span class="chip ${p.catClass}" style="margin-left:auto">${p.cat}</span>
    </div>
    <div style="font-weight:600;font-size:15px;margin-bottom:4px">${p.title}</div>
    <p class="small" style="margin:0 0 4px">${p.body}</p>
    <div class="post-media" style="background:${p.color}"><svg class="icon" style="width:26px;height:26px;stroke:${'var(--ink-soft)'}"><use href="#i-doc"/></svg></div>
    <div class="post-actions">
      <span>♥ Reaccionar</span><span>💬 Comentar</span><span>↗ Compartir</span>
    </div>
  </div>`;
}

function renderFeed(){
  document.getElementById('feed-full').innerHTML = state.posts.map(postCard).join('');
  document.getElementById('dash-feed').innerHTML = state.posts.slice(0,2).map(postCard).join('');
}

function renderPerfil(){
  document.getElementById('perfil-stars').innerHTML = starsSvg(state.level);
  document.getElementById('gam-stars').innerHTML = starsSvg(state.level, 5, 18);
  document.getElementById('perfil-xp-label').textContent = `${state.xp.toLocaleString()} / ${state.xpNext.toLocaleString()} XP`;
  document.getElementById('gam-xp-label').textContent = `${state.xp.toLocaleString()} / ${state.xpNext.toLocaleString()}`;
  const pct = Math.min(100, Math.round((state.xp/state.xpNext)*100));
  document.getElementById('perfil-progress').style.width = pct+'%';
  document.getElementById('gam-progress').style.width = pct+'%';
  document.getElementById('kpi-xp').textContent = state.xp.toLocaleString();
  document.getElementById('kpi-level').textContent = state.level+' / 5';
  document.getElementById('hex-level').textContent = state.level;

  document.getElementById('hv-stats').innerHTML = [
    ['Artículos publicados','3'],['Ponencias','2'],['Proyectos','4'],['Eventos asistidos','9'],['Patentes','0']
  ].map(([l,v])=>`<div class="flex between" style="padding:9px 0;border-bottom:1px solid var(--border)"><span style="font-size:14px">${l}</span><span class="mono" style="font-weight:600">${v}</span></div>`).join('');

  document.getElementById('logros-pendientes').innerHTML = state.pendingLogros.length
    ? state.pendingLogros.map(l=>`<div class="flex between center" style="padding:8px 0"><span class="small">${l.titulo}</span><span class="chip chip-muted">${l.estado}</span></div>`).join('')
    : `<div class="small">No tienes logros pendientes de validación.</div>`;
}

function renderIntegrantes(){
  const roles = ['Líder','Estudiante','Estudiante','Estudiante','Estudiante','Estudiante'];
  const names = ['Andrea Molina','Camilo Rojas','Laura Gómez','David Ruiz','Paula León','Iván Cárdenas'];
  document.getElementById('integrantes-list').innerHTML = names.map((n,i)=>`
    <div class="flex between center" style="padding:10px 0;border-bottom:1px solid var(--border)">
      <div class="flex gap12 center"><div class="avatar" style="width:30px;height:30px;font-size:11px;background:var(--teal)">${n.split(' ').map(w=>w[0]).join('')}</div><span style="font-size:14px">${n}</span></div>
      <span class="chip ${roles[i]==='Líder'?'chip-accent':'chip-muted'}">${roles[i]}</span>
    </div>`).join('');
}

function renderEventos(){
  document.getElementById('eventos-list').innerHTML = [
    ['Coloquio de semilleros 2026','Auditorio principal · 10:00 a.m.', 'var(--rose)'],
    ['Taller de escritura científica','Bloque B · 2:00 p.m.', 'var(--teal)'],
    ['Feria de proyectos','Plazoleta central · 9:00 a.m.', 'var(--accent)']
  ].map(([t,s,c])=>`<div class="flex gap12" style="margin-bottom:16px"><span class="badge-dot" style="background:${c};margin-top:5px"></span><div><div style="font-weight:600;font-size:14.5px">${t}</div><div class="small">${s}</div></div></div>`).join('');
  document.getElementById('convocatorias-list').innerHTML = [
    ['Semilleros de investigación aplicada','Financiación 2026-II para proyectos en curso.'],
    ['Movilidad académica internacional','Apoyo para presentar resultados en congresos.']
  ].map(([t,s],i)=>`<div class="post" style="margin-bottom:14px"><div style="font-weight:600;font-size:14.5px">${t}</div><p class="small" style="margin:6px 0 12px">${s}</p><button class="btn btn-accent btn-sm" onclick="toast('Postulación enviada')">Postularse</button></div>`).join('');
}

function renderBadges(){
  const cols = ['var(--violet)','var(--accent)','var(--green)','var(--teal)','var(--rose)','var(--red)'];
  let html='';
  for(let i=0;i<8;i++){
    const active = i<6;
    html += `<div>
      <div class="avatar" style="width:56px;height:56px;margin:0 auto 8px;background:${active?cols[i]:'var(--border)'}">
        <svg class="icon" style="stroke:#fff;width:22px;height:22px"><use href="#i-trophy"/></svg>
      </div>
      <div class="small">${active?'Insignia '+(i+1):'Bloqueada'}</div>
    </div>`;
  }
  document.getElementById('badges-grid').innerHTML = html;

  document.getElementById('xp-history').innerHTML = [
    ['Artículo publicado','+150 XP'],['Ponencia presentada','+120 XP'],['Participación en evento','+40 XP'],
    ['Proyecto registrado','+80 XP'],['Patente registrada','+300 XP']
  ].map(([l,v])=>`<div class="flex between" style="padding:9px 0;border-bottom:1px solid var(--border)"><span style="font-size:14px">${l}</span><span class="mono" style="color:var(--accent-ink);font-weight:700">${v}</span></div>`).join('');
}

function renderAdmin(){
  const tc = document.getElementById('tabla-cuentas');
  tc.innerHTML = state.adminCuentas.map((c,i)=>`
    <tr id="cuenta-row-${i}">
      <td>${c.nombre}</td><td class="mono" style="font-size:12.5px">${c.correo}</td>
      <td><span class="chip chip-muted">${c.rol}</span></td>
      <td class="small">carnet.pdf</td>
      <td class="flex gap8"><button class="btn btn-primary btn-sm" onclick="resolveRow('adminCuentas',${i},'cuenta-row-${i}','Cuenta aprobada')">Aprobar</button><button class="btn btn-outline btn-sm" onclick="resolveRow('adminCuentas',${i},'cuenta-row-${i}','Cuenta rechazada')">Rechazar</button></td>
    </tr>`).join('');
  document.getElementById('count-cuentas').textContent = '('+state.adminCuentas.length+')';
  document.getElementById('empty-cuentas').style.display = state.adminCuentas.length ? 'none' : 'block';

  const tl = document.getElementById('tabla-logros');
  tl.innerHTML = state.adminLogros.map((l,i)=>`
    <tr id="logro-row-${i}">
      <td>${l.estudiante}</td><td><span class="chip chip-accent">${l.tipo}</span></td>
      <td class="small">${l.desc}</td>
      <td class="flex gap8"><button class="btn btn-primary btn-sm" onclick="resolveRow('adminLogros',${i},'logro-row-${i}','Logro aprobado, XP asignado')">Aprobar</button><button class="btn btn-outline btn-sm" onclick="resolveRow('adminLogros',${i},'logro-row-${i}','Logro rechazado')">Rechazar</button></td>
    </tr>`).join('');
  document.getElementById('count-logros').textContent = '('+state.adminLogros.length+')';
  document.getElementById('empty-logros').style.display = state.adminLogros.length ? 'none' : 'block';
}

function renderRanking(){
  let data = [...state.ranking];
  if(state.rankSort.key){
    data.sort((a,b)=>{
      const k = state.rankSort.key;
      if(typeof a[k]==='number') return (a[k]-b[k])*state.rankSort.dir;
      return a[k].localeCompare(b[k])*state.rankSort.dir;
    });
  }
  document.getElementById('tabla-ranking').innerHTML = data.map((r,i)=>`
    <tr>
      <td class="mono" style="font-weight:700;color:${i<3?'var(--rose)':'var(--ink)'}">${i+1}</td>
      <td class="flex gap12 center" style="border:none;padding-top:13px">
        <div class="avatar" style="width:26px;height:26px;font-size:10px;background:var(--ink-soft)">${r.nombre.slice(0,2)}</div>${r.nombre}
      </td>
      <td>${r.facultad}</td>
      <td class="mono">${r.xp.toLocaleString()}</td>
      <td>${starsSvg(r.nivel,5,13)}</td>
    </tr>`).join('');
}

function renderAll(){
  renderFeed(); renderPerfil(); renderIntegrantes(); renderEventos(); renderBadges(); renderAdmin(); renderRanking();
}

/* ============================================================
   ACTIONS
   ============================================================ */
function openModal(id){ document.getElementById(id).classList.add('active'); }
function closeModal(id){ document.getElementById(id).classList.remove('active'); }

function pickCat(btn){
  document.querySelectorAll('#post-cat-picker button').forEach(b=>b.classList.remove('sel'));
  btn.classList.add('sel');
  state.postCategory = btn.dataset.cat;
}

const CAT_STYLE = {Logro:'chip-accent', Proyecto:'chip-teal', Evento:'chip-rose', General:'chip-violet'};
const CAT_MEDIA = {Logro:'var(--accent-soft)', Proyecto:'var(--teal-soft)', Evento:'var(--rose-soft)', General:'var(--violet-soft)'};

function submitPost(){
  const title = document.getElementById('post-title').value.trim();
  const body = document.getElementById('post-body').value.trim();
  if(!title){ toast('Escribe un título para tu publicación'); return; }
  state.posts.unshift({
    who:'Tú', when:'justo ahora', cat:state.postCategory, catClass:CAT_STYLE[state.postCategory],
    color:CAT_MEDIA[state.postCategory], title, body: body || 'Sin descripción adicional.'
  });
  document.getElementById('post-title').value='';
  document.getElementById('post-body').value='';
  renderFeed();
  closeModal('modal-post');
  toast('Publicación creada');
}

function submitLogro(){
  const tipo = document.getElementById('logro-tipo').value;
  const titulo = document.getElementById('logro-titulo').value.trim();
  if(!titulo){ toast('Describe el logro antes de enviarlo'); return; }
  state.pendingLogros.push({tipo, titulo, estado:'Pendiente'});
  document.getElementById('logro-titulo').value='';
  renderPerfil();
  toast('Logro enviado a validación del administrador');
}

function resolveRow(arrName, index, rowId, message){
  const row = document.getElementById(rowId);
  if(row) row.classList.add('row-fade');
  setTimeout(()=>{
    state[arrName].splice(index,1);
    renderAdmin();
  }, 320);
  toast(message);
}

function simulateActivity(){
  state.xp += 80;
  if(state.xp >= state.xpNext){
    state.xp -= state.xpNext;
    state.level = Math.min(5, state.level+1);
    state.xpNext = Math.round(state.xpNext*1.15);
    toast('¡Subiste al nivel '+state.level+'!');
  } else {
    toast('+80 XP registrados');
  }
  renderPerfil();
}

function sortRanking(key){
  if(state.rankSort.key===key){ state.rankSort.dir *= -1; }
  else { state.rankSort.key = key; state.rankSort.dir = key==='pos'?1:-1; }
  renderRanking();
}

function toast(msg){
  const wrap = document.getElementById('toast-wrap');
  const t = document.createElement('div');
  t.className='toast';
  t.innerHTML = `<span class="dot"></span>${msg}`;
  wrap.appendChild(t);
  setTimeout(()=>{ t.style.opacity='0'; t.style.transform='translateY(10px)'; t.style.transition='.3s'; setTimeout(()=>t.remove(),300); }, 2600);
}
