from config import RegistryConfig
import settings

def open(key):
    from backends import get_backend
    return RegistryConfig(key=key, 
            backend_class=get_backend(settings.DEFAULT_BACKEND))
