from rest_framework.permissions import BasePermission
from django.conf import settings

AUTH0_DOMAIN = settings.DOMAIN


class HasRole(BasePermission):
    required_roles = []

    def has_permission(self, request, view):
        roles = request.auth.get(f"https://{AUTH0_DOMAIN}/claims/roles", [])
        return any(role in roles for role in self.required_roles)


class HasScope(BasePermission):
    required_scopes = []

    def has_permission(self, request, view):
        scopes = request.auth.get("scope", "").split()
        return any(scope in scopes for scope in self.required_scopes)
