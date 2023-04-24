from rest_framework import permissions


class CustomerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == "list":
            return True
        elif view.action == "retrieve":
            return request.user.is_authenticated()
        elif view.action in ["create", "update", "partial_update", "destroy"]:
            return request.user.is_authenticated() and request.user.is_staff
        else:
            return False
