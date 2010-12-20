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
        self._data = {}
        self.key = key
        backend_class = backend_class or backends.InMemoryBackend
        self.backend = backend_class()

        # lazy loading config is designed to 
        # avoid circullar import loop in django magic modules loading
        self.is_loaded = False

    def __getitem__(self, key, d=None):
        """
        accessor for configuration
        lazy loads data
        """
        if not self.is_loaded:
            self.reload()

        return self._data.get(key,d)

    def reload(self):
        """
        reloads data form Registry using owned backend
        """
        self._data = dict(self.backend.read(self.key))
        self.is_loaded = True

    def set(self, key, value):
        if not self.is_loaded:
            self.reload()
        self._data[key] = value
        self.backend.write(self.key, self._data)

    def __setitem__(self, key, value):
        self.set(key,value)

    def get(self, key):
        try:
            return self[key]
        except KeyError:
            return None


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
