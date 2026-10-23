from flask import Blueprint
from controllers.auth_controller import register, login, get_me
from controllers.publicacion_controller import get_publicaciones, create_publicacion, comentar, reaccionar, compartir
from controllers.semillero_controller import get_semilleros, get_semillero_by_id, solicitar_vinculacion, get_integrantes, resolver_vinculacion
from controllers.logro_controller import get_logros_pendientes, enviar_logro, get_mis_logros, aprobar_logro, rechazar_logro
from controllers.admin_controller import get_cuentas_pendientes, aprobar_cuenta, rechazar_cuenta, get_facultades, get_programas
from controllers.ranking_controller import get_ranking_semilleros, get_ranking_investigadores, get_kpis, get_indicadores_facultad, get_hoja_vida
from middleware.auth import authenticate_token, require_role, optional_auth

# Blueprint para autenticación
auth_bp = Blueprint('auth', __name__)
auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/me', methods=['GET'])(authenticate_token(get_me))

# Blueprint para publicaciones
publicaciones_bp = Blueprint('publicaciones', __name__)
publicaciones_bp.route('/', methods=['GET'])(optional_auth(get_publicaciones))
publicaciones_bp.route('/', methods=['POST'])(authenticate_token(create_publicacion))
publicaciones_bp.route('/comentar', methods=['POST'])(authenticate_token(comentar))
publicaciones_bp.route('/reaccionar', methods=['POST'])(authenticate_token(reaccionar))
publicaciones_bp.route('/compartir', methods=['POST'])(authenticate_token(compartir))

# Blueprint para semilleros
semilleros_bp = Blueprint('semilleros', __name__)
semilleros_bp.route('/', methods=['GET'])(get_semilleros)
semilleros_bp.route('/<int:id>', methods=['GET'])(get_semillero_by_id)
semilleros_bp.route('/solicitar-vinculacion', methods=['POST'])(authenticate_token(solicitar_vinculacion))
semilleros_bp.route('/<int:id>/integrantes', methods=['GET'])(get_integrantes)
semilleros_bp.route('/resolver-vinculacion', methods=['POST'])(authenticate_token(require_role(['docente', 'administrador'])(resolver_vinculacion)))

# Blueprint para logros
logros_bp = Blueprint('logros', __name__)
logros_bp.route('/pendientes', methods=['GET'])(authenticate_token(require_role(['administrador'])(get_logros_pendientes)))
logros_bp.route('/', methods=['POST'])(authenticate_token(enviar_logro))
logros_bp.route('/mis-logros', methods=['GET'])(authenticate_token(get_mis_logros))
logros_bp.route('/<int:logro_id>/aprobar', methods=['POST'])(authenticate_token(require_role(['administrador'])(aprobar_logro)))
logros_bp.route('/<int:logro_id>/rechazar', methods=['POST'])(authenticate_token(require_role(['administrador'])(rechazar_logro)))

# Blueprint para admin
admin_bp = Blueprint('admin', __name__)
admin_bp.route('/cuentas-pendientes', methods=['GET'])(authenticate_token(require_role(['administrador'])(get_cuentas_pendientes)))
admin_bp.route('/cuentas/<int:usuario_id>/aprobar', methods=['POST'])(authenticate_token(require_role(['administrador'])(aprobar_cuenta)))
admin_bp.route('/cuentas/<int:usuario_id>/rechazar', methods=['POST'])(authenticate_token(require_role(['administrador'])(rechazar_cuenta)))
admin_bp.route('/facultades', methods=['GET'])(get_facultades)
admin_bp.route('/programas', methods=['GET'])(get_programas)

# Blueprint para ranking
ranking_bp = Blueprint('ranking', __name__)
ranking_bp.route('/semilleros', methods=['GET'])(get_ranking_semilleros)
ranking_bp.route('/investigadores', methods=['GET'])(get_ranking_investigadores)
ranking_bp.route('/kpis', methods=['GET'])(get_kpis)
ranking_bp.route('/indicadores-facultad', methods=['GET'])(get_indicadores_facultad)
ranking_bp.route('/hoja-vida/<int:usuario_id>', methods=['GET'])(get_hoja_vida)
