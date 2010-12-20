from config import RegistryConfig
import settings

def open(key):
    from backends import get_backend
    from django.db import models

    if isinstance(key, models.Model):
        backend_class = 'registry.backends.ModelBackend'
    else:
        backend_class = settings.DEFAULT_BACKEND

    return RegistryConfig(key=key, 
            backend_class=get_backend(backend_class))
