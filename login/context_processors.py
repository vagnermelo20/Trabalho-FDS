from login.models import Usuario

def processar_contexto_usuario(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            return {'usuario': usuario}
        except Usuario.DoesNotExist:
            pass
    return {'usuario': None}