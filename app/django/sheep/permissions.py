from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Handles permissions for users.  The basic rules are

     - owner may GET, PUT, POST, DELETE
     - nobody else can access
     """
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'POST', 'PATCH', 'DELETE']:
            # check if user is owner
            return request.user == obj.owner
        else:
            return True
