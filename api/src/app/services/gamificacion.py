from datetime import datetime
from app.extensions import db
from app.models.gamificacion import Logro, TipoActividadXP, MovimientoXP
from app.models.usuarios import Usuario, Nivel, Insignia, UsuarioInsignia
from app.utils.errors import ValidationError, NotFoundError


class GamificacionService:
    """Servicio de lógica de negocio para gamificación"""
    
    @staticmethod
    def obtener_gamificacion_usuario(usuario_id):
        """Obtener datos de gamificación del usuario (XP, nivel, insignias, historial)"""
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundError('Usuario no encontrado')
        
        # Obtener nivel
        nivel = Nivel.query.get(usuario.nivel_id) if usuario.nivel_id else None
        
        # Obtener insignias
        insignias = db.session.query(Insignia).join(UsuarioInsignia).filter(
            UsuarioInsignia.usuario_id == usuario_id
        ).all()
        
        # Obtener historial de XP
        movimientos = MovimientoXP.query.filter_by(usuario_id=usuario_id).order_by(
            MovimientoXP.creado_en.desc()
        ).limit(50).all()
        
        return {
            'xp_total': usuario.xp_total,
            'nivel': nivel,
            'estrellas': nivel.estrellas if nivel else 0,
            'insignias': insignias,
            'historial_xp': movimientos
        }
    
    @staticmethod
    def listar_logros(usuario_id, limit=50, offset=0, estado=None):
        """Listar logros de usuario"""
        query = Logro.query.filter_by(usuario_id=usuario_id)
        
        if estado:
            query = query.filter(Logro.estado == estado)
        
        logros = query.order_by(Logro.creado_en.desc()).limit(limit).offset(offset).all()
        total = query.count()
        
        return logros, total
    
    @staticmethod
    def listar_logros_pendientes(limit=50, offset=0):
        """Listar logros pendientes (solo admin)"""
        query = Logro.query.filter_by(estado='enviado')
        logros = query.order_by(Logro.creado_en.asc()).limit(limit).offset(offset).all()
        total = query.count()
        return logros, total
    
    @staticmethod
    def enviar_logro(data, usuario_id):
        """Enviar logro para validación"""
        logro = Logro(
            usuario_id=usuario_id,
            tipo=data['tipo'],
            titulo=data['titulo'],
            descripcion=data.get('descripcion'),
            estado='enviado'
        )
        
        db.session.add(logro)
        db.session.commit()
        
        return logro
    
    @staticmethod
    def validar_logro(logro_id, admin_id):
        """Validar logro (solo admin)"""
        logro = Logro.query.get(logro_id)
        if not logro:
            raise NotFoundError('Logro no encontrado')
        
        if logro.estado != 'enviado':
            raise ValidationError('Solo se pueden validar logros enviados')
        
        logro.estado = 'validado'
        logro.validado_por = admin_id
        logro.fecha_validacion = datetime.utcnow()
        
        # Otorgar XP por logro validado
        GamificacionService._otorgar_xp(logro.usuario_id, 'logro_validado', referencia_id=logro.id)
        
        # Otorgar insignia si corresponde
        GamificacionService._otorgar_insignias(logro.usuario_id)
        
        # Crear notificación
        GamificacionService._crear_notificacion(
            logro.usuario_id,
            'logro_validado',
            f'Tu logro "{logro.titulo}" ha sido validado',
            referencia_tipo='logro',
            referencia_id=logro.id
        )
        
        db.session.commit()
        
        return logro
    
    @staticmethod
    def rechazar_logro(logro_id, admin_id):
        """Rechazar logro (solo admin)"""
        logro = Logro.query.get(logro_id)
        if not logro:
            raise NotFoundError('Logro no encontrado')
        
        if logro.estado != 'enviado':
            raise ValidationError('Solo se pueden rechazar logros enviados')
        
        logro.estado = 'rechazado'
        logro.validado_por = admin_id
        logro.fecha_validacion = datetime.utcnow()
        
        # Crear notificación
        GamificacionService._crear_notificacion(
            logro.usuario_id,
            'logro_rechazado',
            f'Tu logro "{logro.titulo}" ha sido rechazado',
            referencia_tipo='logro',
            referencia_id=logro.id
        )
        
        db.session.commit()
        
        return logro
    
    @staticmethod
    def _otorgar_xp(usuario_id, tipo_actividad, referencia_tipo=None, referencia_id=None):
        """Otorgar XP (método interno)"""
        tipo = TipoActividadXP.query.filter_by(tipo=tipo_actividad).first()
        if not tipo:
            return
        
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
        
        # Recalcular nivel
        GamificacionService._recalcular_nivel(usuario)
    
    @staticmethod
    def _recalcular_nivel(usuario):
        """Recalcular nivel según XP"""
        niveles = Nivel.query.order_by(Nivel.umbral_xp.desc()).all()
        
        for nivel in niveles:
            if usuario.xp_total >= nivel.umbral_xp:
                usuario.nivel_id = nivel.id
                break
        else:
            nivel_mas_bajo = Nivel.query.order_by(Nivel.umbral_xp.asc()).first()
            usuario.nivel_id = nivel_mas_bajo.id if nivel_mas_bajo else None
    
    @staticmethod
    def _otorgar_insignias(usuario_id):
        """Otorgar insignias según criterios (simplificado)"""
        usuario = Usuario.query.get(usuario_id)
        
        # Insignia: Nivel 3 alcanzado
        if usuario.nivel_id and usuario.nivel.numero >= 3:
            insignia = Insignia.query.filter_by(nombre='Nivel 3 alcanzado').first()
            if insignia:
                existente = UsuarioInsignia.query.filter_by(
                    usuario_id=usuario_id,
                    insignia_id=insignia.id
                ).first()
                if not existente:
                    usuario_insignia = UsuarioInsignia(
                        usuario_id=usuario_id,
                        insignia_id=insignia.id
                    )
                    db.session.add(usuario_insignia)
        
        # Insignia: 1000 XP
        if usuario.xp_total >= 1000:
            insignia = Insignia.query.filter_by(nombre='1000 XP').first()
            if insignia:
                existente = UsuarioInsignia.query.filter_by(
                    usuario_id=usuario_id,
                    insignia_id=insignia.id
                ).first()
                if not existente:
                    usuario_insignia = UsuarioInsignia(
                        usuario_id=usuario_id,
                        insignia_id=insignia.id
                    )
                    db.session.add(usuario_insignia)
    
    @staticmethod
    def _crear_notificacion(usuario_id, tipo, mensaje, referencia_tipo=None, referencia_id=None):
        """Crear notificación (método interno)"""
        from app.models.comunidad import Notificacion
        notificacion = Notificacion(
            usuario_id=usuario_id,
            tipo=tipo,
            titulo=tipo,
            mensaje=mensaje,
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id
        )
        db.session.add(notificacion)
