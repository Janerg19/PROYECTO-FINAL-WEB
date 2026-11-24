import bcrypt
from datetime import datetime
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.usuarios import Usuario, Rol, PerfilInvestigador, UsuarioPrograma
from app.models.gamificacion import TipoActividadXP, MovimientoXP, Nivel
from app.utils.errors import ValidationError, AuthenticationError, NotFoundError, ConflictError, AuthorizationError


class UsuarioService:
    """Servicio de lógica de negocio para usuarios"""
    
    @staticmethod
    def registrar_usuario(data):
        """
        Registrar un nuevo usuario
        - Estado por defecto: pendiente
        - Contraseña hasheada con bcrypt
        - No puede iniciar sesión hasta que sea aprobado por admin
        """
        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=data['email']).first():
            raise ConflictError('El email ya está registrado')
        
        # Obtener rol por defecto (estudiante)
        rol_estudiante = Rol.query.filter_by(nombre='estudiante').first()
        if not rol_estudiante:
            raise ValidationError('Rol estudiante no encontrado')
        
        # Obtener nivel inicial
        nivel_inicial = Nivel.query.filter_by(numero=1).first()
        
        # Hash de contraseña
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Crear usuario
        usuario = Usuario(
            rol_id=rol_estudiante.id,
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            email=data['email'],
            password_hash=password_hash,
            estado='pendiente',
            nivel_id=nivel_inicial.id if nivel_inicial else None,
            xp_total=0
        )
        
        db.session.add(usuario)
        db.session.flush()  # Para obtener el ID antes del commit
        
        # Si se proporciona programa, crear relación usuario-programa
        if 'programa_id' in data and data['programa_id']:
            usuario_programa = UsuarioPrograma(
                usuario_id=usuario.id,
                programa_id=data['programa_id'],
                fecha_inicio=datetime.utcnow().date(),
                actual=True
            )
            db.session.add(usuario_programa)
        
        db.session.commit()
        
        return usuario
    
    @staticmethod
    def login_usuario(email, password):
        """
        Login de usuario
        - Solo usuarios con estado 'aprobada' pueden iniciar sesión
        - Retorna access token JWT
        """
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario:
            raise AuthenticationError('Credenciales inválidas')
        
        # Verificar estado de la cuenta
        if usuario.estado != 'aprobada':
            if usuario.estado == 'pendiente':
                raise AuthenticationError('Cuenta pendiente de aprobación por administrador')
            elif usuario.estado == 'rechazada':
                raise AuthenticationError('Cuenta rechazada')
            elif usuario.estado == 'suspendida':
                raise AuthenticationError('Cuenta suspendida')
        
        # Verificar contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
            raise AuthenticationError('Credenciales inválidas')
        
        # Crear token JWT con rol incluido
        rol_nombre = usuario.rol.nombre if usuario.rol else 'visitante'
        additional_claims = {
            'rol': rol_nombre,
            'estado': usuario.estado
        }
        access_token = create_access_token(identity=usuario.id, additional_claims=additional_claims)
        
        return {
            'access_token': access_token,
            'usuario': {
                'id': usuario.id,
                'email': usuario.email,
                'nombres': usuario.nombres,
                'apellidos': usuario.apellidos,
                'rol': rol_nombre,
                'estado': usuario.estado
            }
        }
    
    @staticmethod
    def obtener_usuario(usuario_id):
        """Obtener usuario por ID"""
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundError('Usuario no encontrado')
        return usuario
    
    @staticmethod
    def obtener_usuario_me(usuario_id):
        """Obtener usuario actual con perfil completo"""
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundError('Usuario no encontrado')
        return usuario
    
    @staticmethod
    def listar_usuarios(limit=50, offset=0, rol=None, estado=None):
        """Listar usuarios con filtros (solo admin)"""
        query = Usuario.query
        
        if rol:
            query = query.join(Rol).filter(Rol.nombre == rol)
        
        if estado:
            query = query.filter(Usuario.estado == estado)
        
        query = query.filter(Usuario.eliminado_en.is_(None))
        
        usuarios = query.order_by(Usuario.creado_en.desc()).limit(limit).offset(offset).all()
        total = query.count()
        
        return usuarios, total
    
    @staticmethod
    def aprobar_cuenta(usuario_id, admin_id):
        """
        Aprobar cuenta de usuario (solo admin)
        - Cambia estado a 'aprobada'
        - Registra validado_por y fecha_validacion
        - Otorga 50 XP por registro validado
        """
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundError('Usuario no encontrado')
        
        if usuario.estado != 'pendiente':
            raise ValidationError('Solo se pueden aprobar cuentas pendientes')
        
        usuario.estado = 'aprobada'
        usuario.validado_por = admin_id
        usuario.fecha_validacion = datetime.utcnow()
        
        # Otorgar XP por registro validado
        UsuarioService._otorgar_xp(usuario_id, 'registro_usuario', referencia_id=usuario_id)
        
        db.session.commit()
        
        return usuario
    
    @staticmethod
    def rechazar_cuenta(usuario_id, admin_id):
        """
        Rechazar cuenta de usuario (solo admin)
        - Cambia estado a 'rechazada'
        - Registra validado_por y fecha_validacion
        """
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundError('Usuario no encontrado')
        
        if usuario.estado != 'pendiente':
            raise ValidationError('Solo se pueden rechazar cuentas pendientes')
        
        usuario.estado = 'rechazada'
        usuario.validado_por = admin_id
        usuario.fecha_validacion = datetime.utcnow()
        
        db.session.commit()
        
        return usuario
    
    @staticmethod
    def actualizar_usuario(usuario_id, data, solicitante_id):
        """
        Actualizar usuario
        - Admin puede actualizar cualquier usuario
        - Usuario solo puede actualizar su propio perfil
        """
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundError('Usuario no encontrado')
        
        # Verificar permisos
        if solicitante_id != usuario_id:
            # Aquí se debería verificar si el solicitante es admin
            # Por ahora, solo permitir auto-actualización
            raise AuthorizationError('No autorizado para actualizar este usuario')
        
        # Actualizar campos permitidos
        if 'nombres' in data:
            usuario.nombres = data['nombres']
        if 'apellidos' in data:
            usuario.apellidos = data['apellidos']
        
        usuario.actualizado_en = datetime.utcnow()
        db.session.commit()
        
        return usuario
    
    @staticmethod
    def actualizar_perfil_investigador(usuario_id, data):
        """Actualizar perfil investigativo del usuario"""
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundError('Usuario no encontrado')
        
        perfil = usuario.perfil_investigador
        
        if not perfil:
            # Crear perfil si no existe
            perfil = PerfilInvestigador(usuario_id=usuario_id)
            db.session.add(perfil)
        
        # Actualizar campos
        if 'biografia' in data:
            perfil.biografia = data['biografia']
        if 'intereses' in data:
            perfil.intereses = data['intereses']
        if 'orcid' in data:
            perfil.orcid = data['orcid']
        if 'cvlac' in data:
            perfil.cvlac = data['cvlac']
        
        perfil.actualizado_en = datetime.utcnow()
        db.session.commit()
        
        return perfil
    
    @staticmethod
    def eliminar_usuario(usuario_id):
        """Borrado lógico de usuario (solo admin)"""
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundError('Usuario no encontrado')
        
        usuario.eliminado_en = datetime.utcnow()
        db.session.commit()
        
        return usuario
    
    @staticmethod
    def _otorgar_xp(usuario_id, tipo_actividad, referencia_tipo=None, referencia_id=None):
        """
        Otorgar XP a un usuario (método interno)
        - Crea movimiento de XP inmutable
        - Actualiza xp_total del usuario
        - Recalcula nivel
        - Otorga insignias si corresponde
        """
        # Obtener tipo de actividad
        tipo = TipoActividadXP.query.filter_by(tipo=tipo_actividad).first()
        if not tipo:
            raise ValidationError(f'Tipo de actividad {tipo_actividad} no encontrado')
        
        # Crear movimiento de XP
        movimiento = MovimientoXP(
            usuario_id=usuario_id,
            tipo_actividad_id=tipo.id,
            xp_ganada=tipo.xp_base,
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id
        )
        db.session.add(movimiento)
        
        # Actualizar XP total del usuario
        usuario = Usuario.query.get(usuario_id)
        usuario.xp_total += tipo.xp_base
        
        # Recalcular nivel
        UsuarioService._recalcular_nivel(usuario)
        
        # Otorgar insignias (se implementará después)
        # UsuarioService._otorgar_insignias(usuario)
    
    @staticmethod
    def _recalcular_nivel(usuario):
        """Recalcular nivel del usuario según su XP total"""
        niveles = Nivel.query.order_by(Nivel.umbral_xp.desc()).all()
        
        for nivel in niveles:
            if usuario.xp_total >= nivel.umbral_xp:
                usuario.nivel_id = nivel.id
                break
        else:
            # Si no alcanza ningún nivel, asignar el más bajo
            nivel_mas_bajo = Nivel.query.order_by(Nivel.umbral_xp.asc()).first()
            usuario.nivel_id = nivel_mas_bajo.id if nivel_mas_bajo else None
