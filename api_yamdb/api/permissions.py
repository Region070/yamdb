from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin() or request.user.is_superuser
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Пользователи могут запрашивать данные.
    Администратор может изменять данные.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_admin())
        )


class PermissionReviewComment(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.is_admin()
                         or request.user.is_moderator()
                         or obj.author == request.user)))
