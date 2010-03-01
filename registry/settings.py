from django.conf import settings

DEFAULT_BACKEND = getattr(settings, 'REGISTRY_DEFAULT_BACKEND',
        'registry.backends.DatabaseBackend')
