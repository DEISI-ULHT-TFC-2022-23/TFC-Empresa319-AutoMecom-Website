from django import template
from django.contrib.auth.models import AnonymousUser

from automecom.models import Utilizador

register = template.Library()


@register.filter(name="is_administrador")
def is_administrador(user):
    if isinstance(user, AnonymousUser):
        return False
    try:
        utilizador = Utilizador.objects.get(user=user) or None
    except Utilizador.DoesNotExist:
        return False

    if utilizador is None:
        return False

    return utilizador.administrador
