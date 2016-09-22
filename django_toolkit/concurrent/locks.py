from django.core.cache import caches


class LockActiveError(Exception):
    pass


class Lock(object):

    def __init__(self):
        self.active = False


class LocalMemoryLock(Lock):
    """
    A context manager to handle a lock status in memory

    The active status is True on __enter__ and False on __exit__
    """

    def __enter__(self):

        if self.active:
            raise LockActiveError('Lock is already active')

        self.active = True
        return self

    def __exit__(self, *args, **kwargs):
        self.active = False


class CacheLock(Lock):

    def __init__(self, key, cache_alias='default', expire=0):
        super(CacheLock, self).__init__()
        self._key = key
        self._expire = expire
        self.cache = caches[cache_alias]

    def __enter__(self):
        self.active = self.cache.add(self._key, True, self._expire)

        if not self.active:
            raise LockActiveError('For key {key}'.format(key=self._key))

        return self

    def __exit__(self, *args, **kwargs):
        self.active = False
        self.cache.delete(self._key)
