from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Define si un usuario puede usar o no el endpoint que quiere utilizar
        :param request: HttpRequest
        :param view: UsersAPI/UserDetailAPI
        :return: True si puede, False si no puede
        """
        # cualquiera autenticado puede acceder al detalle para ver, actualizar o borrar
        if request.user.is_authenticated() and view.action in ("retrieve", "update", "destroy"):
            return True

        # si es superusuario y quiere acceder al listado
        if request.user.is_superuser and view.action == "list":
            return True

        # cualquiera puede crear un usuario (POST)
        if view.action == "create":
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario puede realizar la acción sobre el objeto que quiere realizarla
        :param request: HttpRequest
        :param view: UsersAPI/UserDetailAPI
        :param obj: User
        :return: True si puede, False si no puede
        """
        # si es admin o si es él mismo, le dejamos
        return request.user.is_superuser or request.user == obj
