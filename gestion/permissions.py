# gestion/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

# 1. Permiso original de administración
class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


# 2. Permiso para usuarios con rol "Coach"
class IsCoachOrReadOnly(BasePermission):
    """
    Permite lectura a cualquier usuario autenticado, 
    pero solo permite escritura (POST, PUT, DELETE) a los entrenadores (Coach) o Staff.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.tipo_usuario == 'Coach' or request.user.is_staff)
        )


# 3. Permiso a nivel de objeto para Partidos (Dueño o Staff)
class IsOwnerOrStaff(BasePermission):
    """
    Permiso para asegurar que solo el Coach creador del partido o un administrador 
    pueda añadir o modificar las métricas/datos de ese objeto específico.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
            
        return bool(obj.usuario == request.user or request.user.is_staff)


# 4. Permiso genérico basado en roles (Opcional para el futuro)
class IsRoleOrReadOnly(BasePermission):
    """
    Permiso dinámico. Puedes definir qué roles tienen permitido el acceso
    directamente en la vista usando: required_roles = ['Coach', 'Scout']
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
            
        allowed_roles = getattr(view, 'required_roles', [])
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.tipo_usuario in allowed_roles or request.user.is_staff)
        )


# 5. Permiso a nivel de objeto para Evaluaciones basadas en el Jugador
class IsCoachOwnerOrStaff(BasePermission):
    """
    Permite acceso total al Coach que registró originalmente al jugador, 
    o al equipo de Staff/Administración.
    """
    def has_object_permission(self, request, view, obj):
        # Primero aseguramos que el usuario esté logueado
        if not request.user or not request.user.is_authenticated:
            return False
            
        # En el objeto evaluado, navegamos hasta el dueño del jugador: obj.jugador.usuario
        return bool(obj.jugador.usuario == request.user or request.user.is_staff)