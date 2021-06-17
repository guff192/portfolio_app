from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and request.user.is_authenticated and obj.employees.filter(user__exact=request.user).filter(
                role__exact='o'))


class IsEmployee(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.employees.filter(user__exact=request.user))


class IsEmployeeOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        employee_permissions = super(IsEmployeeOrStaff, self).has_object_permission(request, view, obj)

        return bool(employee_permissions or request.user.is_staff)


class IsEmployeeOrStaffOrReadOnly(IsEmployeeOrStaff):
    def has_object_permission(self, request, view, obj):
        super_permissions = super(IsEmployeeOrStaffOrReadOnly, self).has_object_permission(request, view, obj)

        return bool(request.method in SAFE_METHODS or super_permissions)
