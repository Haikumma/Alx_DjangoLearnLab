from rest_framework.permissions import BasePermission

# custom permission class 
class IsLoggedIn(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        """
        Return True if permission is granted, False otherwise.

        :param request: The request object
        :param view: The view object
        :param obj: The object to check permission against
        :return: True if permission is granted, False otherwise
        """
        return request.user == obj