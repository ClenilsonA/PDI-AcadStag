from empresas.models import Empresa


def get_empresa_profile(user):
    if not user.is_authenticated or user.role != "EMPRESA":
        return None

    try:
        return user.empresa
    except Empresa.DoesNotExist:
        return None