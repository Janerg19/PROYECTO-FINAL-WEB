from flask import request
from flask_jwt_extended import get_jwt_identity
from app.services.usuarios import UsuarioService
from app.schemas.usuarios import (
    UsuarioRegisterSchema, UsuarioLoginSchema, UsuarioSchema,
    UsuarioCompletoSchema, UsuarioUpdateSchema, PerfilInvestigadorUpdateSchema
)
from app.utils.errors import ValidationError


class UsuarioController:
    """Controlador HTTP para usuarios"""
    
    @staticmethod
    def register():
        """Registro de nuevo usuario"""
        try:
            # Validar datos de entrada
            schema = UsuarioRegisterSchema()
            data = schema.load(request.json)
            
            # Registrar usuario
            usuario = UsuarioService.registrar_usuario(data)
            
            # Serializar respuesta
            response_schema = UsuarioSchema()
            return response_schema.dump(usuario), 201
            
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError(f'Error al registrar usuario: {str(e)}')
    
    @staticmethod
    def login():
        """Login de usuario"""
        try:
            # Validar datos de entrada
            schema = UsuarioLoginSchema()
            data = schema.load(request.json)
            
            # Login
            resultado = UsuarioService.login_usuario(data['email'], data['password'])
            
            return resultado, 200
            
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError(f'Error al iniciar sesión: {str(e)}')
    
    @staticmethod
    def me():
        """Obtener usuario actual"""
        try:
            usuario_id = get_jwt_identity()
            usuario = UsuarioService.obtener_usuario_me(usuario_id)
            
            # Serializar con perfil completo
            response_schema = UsuarioCompletoSchema()
            return response_schema.dump(usuario), 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def listar_usuarios():
        """Listar usuarios (solo admin)"""
        try:
            # Obtener parámetros de query
            limit = request.args.get('limit', 50, type=int)
            offset = request.args.get('offset', 0, type=int)
            rol = request.args.get('rol')
            estado = request.args.get('estado')
            
            # Listar usuarios
            usuarios, total = UsuarioService.listar_usuarios(limit, offset, rol, estado)
            
            # Serializar
            response_schema = UsuarioSchema(many=True)
            return {
                'usuarios': response_schema.dump(usuarios),
                'total': total,
                'limit': limit,
                'offset': offset
            }, 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def obtener_usuario(usuario_id):
        """Obtener usuario por ID (solo admin)"""
        try:
            usuario = UsuarioService.obtener_usuario(usuario_id)
            
            response_schema = UsuarioCompletoSchema()
            return response_schema.dump(usuario), 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def actualizar_usuario(usuario_id):
        """Actualizar usuario"""
        try:
            solicitante_id = get_jwt_identity()
            
            # Validar datos de entrada
            schema = UsuarioUpdateSchema()
            data = schema.load(request.json)
            
            # Actualizar
            usuario = UsuarioService.actualizar_usuario(usuario_id, data, solicitante_id)
            
            response_schema = UsuarioSchema()
            return response_schema.dump(usuario), 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def aprobar_cuenta(usuario_id):
        """Aprobar cuenta de usuario (solo admin)"""
        try:
            admin_id = get_jwt_identity()
            usuario = UsuarioService.aprobar_cuenta(usuario_id, admin_id)
            
            response_schema = UsuarioSchema()
            return response_schema.dump(usuario), 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def rechazar_cuenta(usuario_id):
        """Rechazar cuenta de usuario (solo admin)"""
        try:
            admin_id = get_jwt_identity()
            usuario = UsuarioService.rechazar_cuenta(usuario_id, admin_id)
            
            response_schema = UsuarioSchema()
            return response_schema.dump(usuario), 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def actualizar_perfil(usuario_id):
        """Actualizar perfil investigativo"""
        try:
            # Validar datos de entrada
            schema = PerfilInvestigadorUpdateSchema()
            data = schema.load(request.json)
            
            # Actualizar
            perfil = UsuarioService.actualizar_perfil_investigador(usuario_id, data)
            
            response_schema = PerfilInvestigadorUpdateSchema()
            return response_schema.dump(perfil), 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def eliminar_usuario(usuario_id):
        """Eliminar usuario (solo admin)"""
        try:
            usuario = UsuarioService.eliminar_usuario(usuario_id)
            
            response_schema = UsuarioSchema()
            return response_schema.dump(usuario), 200
            
        except Exception as e:
            raise e
