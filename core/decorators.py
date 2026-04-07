from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def role_required(*allowed_roles, redirect_url="estagios:list", message="Acesso não autorizado."):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("accounts:login")

            if request.user.role not in allowed_roles:
                messages.error(request, message)
                return redirect(redirect_url)

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator