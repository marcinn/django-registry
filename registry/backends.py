"""
Registry configuration backends
"""

import models
from django.db.models.signals import post_save

class InMemoryBackend(object):
    """
    simple memory storage backend for registry configs
    """

    def __init__(self, registry_config):
        """
        initializes storage backend
        """
        self.registry_config = registry_config
        self._data = {}

    def read(self, key=None):
        """
        reads data from storage for key or all data
        """
        return self._data.get(key,{}) if key else self._data
    
    def write(self, config):
        """
        write config (update) to storage
        """
        self._data.update(config)


class DatabaseBackend(object):
    """
    Database registry configuration backend
    """
    def __init__(self, registry_config):
        """
        registry_config is a RegistryConfig instance (caller)
        """
        self.registry_config = registry_config

        # config is automatically reloaded
        # after any Entry model changes
        post_save.connect(self._reload_after_updates, models.Entry)

    def read(self, key=None):
        """
        reads all keys or only subkeys starts with "key"
        """
        if key:
            return dict([(entry.key, entry.value) for \
                    entry in models.Entry.objects.find_keys(key)])
        return dict([(entry.key, entry.value) for \
                entry in models.Entry.objects.all()])

    def write(self, config):
        """
        writes config to database
        config must be an instance of RegistryConfig class
        """
        pass # todo

    def _reload_after_updates(self, **opts):
        """
        reload config if changed Entry model key
        is matching self.key
        """
        if opts.has_key('instance'):
            if opts['instance'].key.startswith(self.registry_config.key):
                self.registry_config.reload()


def get_backend(import_path):
    from django.core.exceptions import ImproperlyConfigured
    try:
        class_name = import_path.split('.')[-1]
        import_path = '.'.join(import_path.split('.')[:-1])
        module = __import__(import_path, globals(), locals(), [class_name])
        return getattr(module, class_name)
    except ImportError:
        raise ImproperlyConfigured('Registry backend %s not found' % import_path) 
