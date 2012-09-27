"""
provides RegistryConfig class as registry configuration storage
"""

import models
import backends


class RegistryConfig(object):
    """
    registry configuration storage class
    """
    def __init__(self, key=None, backend_class=None):
        """
        initializes configuration
        """
        self.key = key
        backend_class = backend_class or backends.InMemoryBackend
        self.backend = backend_class(self)
        self.clear()

        # lazy loading config is designed to 
        # avoid circullar import loop in django magic modules loading
        self.is_loaded = False

    def __getitem__(self, key):
        return self.get(key)

    def clear(self):
        self._data = {}

    def get(self, key, d=None):
        """
        accessor for configuration
        lazy loads data
        """
        if not self.is_loaded:
            self.reload()

        if self.key:
            real_key = '.'.join([self.key, key])
        else:
            real_key = key
        return self._data.get(real_key, d)

    def reload(self):
        """
        reloads data form Registry using owned backend
        """
        self.clear()
        self._data = self.backend.read(self.key)
        self.is_loaded = True


class DatabaseRegistryConfig(RegistryConfig):
    """
    helper class with backend set to Database
    """
    def __init__(self, *args, **kwargs):
        """
        initializes registry config with Database backend class
        """
        kwargs['backend_class'] = backends.DatabaseBackend
        super(DatabaseRegistryConfig, self).__init__(*args, **kwargs)
