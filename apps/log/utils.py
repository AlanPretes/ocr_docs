from .models import Log
import json

def registrar_log(request, content):
    log = Log(
        user = str(request.user.id),
        ip = request.META.get('REMOTE_ADDR'),
        rota=request.path,
        metodo=request.method,
        content = json.dumps({"content": content})
    )
    log.save()