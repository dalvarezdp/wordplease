from datetime import datetime

from rest_framework.permissions import BasePermission


class BlogPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Define si un usuario puede usar o no el endpoint que quiere utilizar
        :param request: HttpRequest
        :param view: UsersAPI/UserDetailAPI
        :return: True si puede, False si no puede
        """

        # si es superusuario y quiere acceder al listado
        if view.action == "list":
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


class PostPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Define si un usuario puede usar o no el endpoint que quiere utilizar
        :param request: HttpRequest
        :param view: UsersAPI/UserDetailAPI
        :return: True si puede, False si no puede
        """
        if view.action == "list":
            return True

        if request.user.is_authenticated() and view.action in ("retrieve", "update", "destroy"):
            return True


        # cualquiera puede crear un usuario (POST)
        if request.user.is_authenticated() and view.action == "create":
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
        # si no es admin o si mismo, y el post no esta publicado no le dejamos
        IsPublished = datetime.today().strftime("%d-%m-%y %H:%M:%S") >= obj.date_public.strftime("%d-%m-%y %H:%M:%S")

        if (request.user.is_superuser or request.user == obj.owner) and view.action in ("update", "destroy"):
            return True

        if (request.user.is_superuser or request.user == obj.owner or IsPublished) and view.action == "retrieve":
            return True

        return False
