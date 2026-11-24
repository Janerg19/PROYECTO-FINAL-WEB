from datetime import datetime
from app.extensions import db
from app.models.investigacion import (
    Semillero, SemilleroIntegrante, SemilleroLinea,
    Proyecto, ProyectoIntegrante, AvanceProyecto, Producto,
    Facultad, Programa, LineaInvestigacion
)
from app.models.usuarios import Usuario, TipoActividadXP, MovimientoXP
from app.utils.errors import ValidationError, NotFoundError, ConflictError, AuthorizationError


class InvestigacionService:
    """Servicio de lógica de negocio para investigación"""
    
    @staticmethod
    def listar_semilleros(limit=50, offset=0, facultad_id=None, activo=None):
        """Listar semilleros con filtros"""
        query = Semillero.query.filter(Semillero.eliminado_en.is_(None))
        
        if facultad_id:
            query = query.filter(Semillero.facultad_id == facultad_id)
        
        if activo is not None:
            query = query.filter(Semillero.activo == activo)
        
        semilleros = query.order_by(Semillero.nombre).limit(limit).offset(offset).all()
        total = query.count()
        
        return semilleros, total
    
    @staticmethod
    def obtener_semillero(semillero_id):
        """Obtener semillero por ID"""
        semillero = Semillero.query.get(semillero_id)
        if not semillero:
            raise NotFoundError('Semillero no encontrado')
        return semillero
    
    @staticmethod
    def crear_semillero(data, creador_id):
        """Crear semillero (solo docente)"""
        # Verificar que el creador sea docente
        creador = Usuario.query.get(creador_id)
        if not creador or creador.rol.nombre != 'docente':
            raise AuthorizationError('Solo docentes pueden crear semilleros')
        
        # Crear semillero
        semillero = Semillero(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            facultad_id=data['facultad_id'],
            programa_id=data.get('programa_id'),
            lider_id=data['lider_id'],
            fecha_creacion=datetime.utcnow().date()
        )
        
        db.session.add(semillero)
        db.session.flush()
        
        # Agregar líneas de investigación si se proporcionan
        if 'lineas' in data and data['lineas']:
            for linea_id in data['lineas']:
                semillero_linea = SemilleroLinea(
                    semillero_id=semillero.id,
                    linea_id=linea_id
                )
                db.session.add(semillero_linea)
        
        # Agregar al líder como integrante
        integrante = SemilleroIntegrante(
            semillero_id=semillero.id,
            usuario_id=data['lider_id'],
            rol='lider',
            estado='aprobada',
            fecha_solicitud=datetime.utcnow(),
            fecha_resolucion=datetime.utcnow(),
            revisado_por=creador_id
        )
        db.session.add(integrante)
        
        db.session.commit()
        
        return semillero
    
    @staticmethod
    def actualizar_semillero(semillero_id, data, solicitante_id):
        """Actualizar semillero (solo líder o admin)"""
        semillero = Semillero.query.get(semillero_id)
        if not semillero:
            raise NotFoundError('Semillero no encontrado')
        
        # Verificar permisos
        if semillero.lider_id != solicitante_id:
            # Aquí se debería verificar si es admin
            raise AuthorizationError('Solo el líder puede actualizar el semillero')
        
        if 'nombre' in data:
            semillero.nombre = data['nombre']
        if 'descripcion' in data:
            semillero.descripcion = data['descripcion']
        if 'activo' in data:
            semillero.activo = data['activo']
        
        semillero.actualizado_en = datetime.utcnow()
        db.session.commit()
        
        return semillero
    
    @staticmethod
    def solicitar_vinculacion(semillero_id, usuario_id):
        """Solicitar vinculación a semillero"""
        # Verificar que no exista una solicitud previa
        existente = SemilleroIntegrante.query.filter_by(
            semillero_id=semillero_id,
            usuario_id=usuario_id
        ).first()
        
        if existente:
            raise ConflictError('Ya existe una solicitud o vinculación a este semillero')
        
        # Crear solicitud
        vinculacion = SemilleroIntegrante(
            semillero_id=semillero_id,
            usuario_id=usuario_id,
            rol='estudiante',
            estado='solicitada',
            fecha_solicitud=datetime.utcnow()
        )
        
        db.session.add(vinculacion)
        db.session.commit()
        
        return vinculacion
    
    @staticmethod
    def resolver_vinculacion(vinculacion_id, estado, revisor_id):
        """Resolver solicitud de vinculación (solo líder del semillero o admin)"""
        vinculacion = SemilleroIntegrante.query.get(vinculacion_id)
        if not vinculacion:
            raise NotFoundError('Vinculación no encontrada')
        
        if vinculacion.estado != 'solicitada':
            raise ValidationError('Solo se pueden resolver solicitudes pendientes')
        
        # Verificar que el revisor sea líder del semillero
        semillero = Semillero.query.get(vinculacion.semillero_id)
        if semillero.lider_id != revisor_id:
            raise AuthorizationError('Solo el líder del semillero puede resolver solicitudes')
        
        vinculacion.estado = estado
        vinculacion.fecha_resolucion = datetime.utcnow()
        vinculacion.revisado_por = revisor_id
        
        # Si es aprobada, otorgar XP
        if estado == 'aprobada':
            InvestigacionService._otorgar_xp(vinculacion.usuario_id, 'vinculacion_semillero', referencia_id=vinculacion.id)
        
        db.session.commit()
        
        return vinculacion
    
    @staticmethod
    def listar_integrantes_semillero(semillero_id):
        """Listar integrantes de un semillero"""
        integrantes = SemilleroIntegrante.query.filter_by(semillero_id=semillero_id).all()
        return integrantes
    
    @staticmethod
    def listar_proyectos(limit=50, offset=0, semillero_id=None, estado=None):
        """Listar proyectos con filtros"""
        query = Proyecto.query.filter(Proyecto.eliminado_en.is_(None))
        
        if semillero_id:
            query = query.filter(Proyecto.semillero_id == semillero_id)
        
        if estado:
            query = query.filter(Proyecto.estado == estado)
        
        proyectos = query.order_by(Proyecto.creado_en.desc()).limit(limit).offset(offset).all()
        total = query.count()
        
        return proyectos, total
    
    @staticmethod
    def crear_proyecto(data, creador_id):
        """Crear proyecto (solo docente)"""
        creador = Usuario.query.get(creador_id)
        if not creador or creador.rol.nombre != 'docente':
            raise AuthorizationError('Solo docentes pueden crear proyectos')
        
        proyecto = Proyecto(
            titulo=data['titulo'],
            descripcion=data.get('descripcion'),
            semillero_id=data['semillero_id'],
            estado=data.get('estado', 'formulacion'),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin')
        )
        
        db.session.add(proyecto)
        db.session.flush()
        
        # Agregar creador como integrante
        integrante = ProyectoIntegrante(
            proyecto_id=proyecto.id,
            usuario_id=creador_id,
            rol='investigador'
        )
        db.session.add(integrante)
        
        # Otorgar XP por proyecto registrado
        InvestigacionService._otorgar_xp(creador_id, 'proyecto_registrado', referencia_id=proyecto.id)
        
        db.session.commit()
        
        return proyecto
    
    @staticmethod
    def crear_avance_proyecto(proyecto_id, data, creador_id):
        """Crear avance de proyecto"""
        avance = AvanceProyecto(
            proyecto_id=proyecto_id,
            titulo=data['titulo'],
            descripcion=data.get('descripcion'),
            fecha_avance=data.get('fecha_avencia', datetime.utcnow().date()),
            creado_por=creador_id
        )
        
        db.session.add(avance)
        db.session.commit()
        
        return avance
    
    @staticmethod
    def crear_producto(proyecto_id, data, creador_id):
        """Crear producto de investigación"""
        producto = Producto(
            proyecto_id=proyecto_id,
            titulo=data['titulo'],
            tipo=data['tipo'],
            descripcion=data.get('descripcion'),
            fecha_publicacion=data.get('fecha_publicacion'),
            url=data.get('url'),
            creado_por=creador_id
        )
        
        db.session.add(producto)
        db.session.flush()
        
        # Otorgar XP por producto registrado
        InvestigacionService._otorgar_xp(creador_id, 'producto_registrado', referencia_id=producto.id)
        
        db.session.commit()
        
        return producto
    
    @staticmethod
    def _otorgar_xp(usuario_id, tipo_actividad, referencia_tipo=None, referencia_id=None):
        """Otorgar XP (método interno)"""
        tipo = TipoActividadXP.query.filter_by(tipo=tipo_actividad).first()
        if not tipo:
            raise ValidationError(f'Tipo de actividad {tipo_actividad} no encontrado')
        
        movimiento = MovimientoXP(
            usuario_id=usuario_id,
            tipo_actividad_id=tipo.id,
            xp_ganada=tipo.xp_base,
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id
        )
        db.session.add(movimiento)
        
        usuario = Usuario.query.get(usuario_id)
        usuario.xp_total += tipo.xp_base
        
        # Recalcular nivel (simplificado, debería usar servicio de usuarios)
        from services.usuarios import UsuarioService
        UsuarioService._recalcular_nivel(usuario)
