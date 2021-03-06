# Concurrent

## Locks

The lock context is used to indicate that a block of code entered in a [critical section](https://en.wikipedia.org/wiki/Critical_section).

### Local memory lock

Use in memory lock.

#### Example

```python
from django_toolkit.concurrent.locks import LocalMemoryLock

def run(*args, **kwargs):
    with LocalMemoryLock() as lock:
        assert lock.active is True
        # do some stuff
```

### Cache lock

`CacheLock` uses django cache system and `default` cache alias by default.
By default, the context manager raises `LockActiveError` when the lock was already active.

#### Arguments

`key`

Cache key.

`cache_alias`

Django cache alias.

`expire`

Time in seconds to expire the cache.
This argument defaults to the backend timeout configuration.

`raise_exception`

Condition to raise `LockActiveError` when lock was already active.

`delete_on_exit`

By default the value of this argument is `True` to have the default `CacheLock` behavior
When set to `False`, the lock persists during the key expiration time in the cache

#### Example

Django cache config

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'locks': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
```

Basic usage.

```python
from django_toolkit.concurrent.locks import CacheLock

def run(*args, **kwargs):
    with CacheLock(key='key') as lock:
        assert lock.active
        # do some stuff
```

You can set the timeout and alias of cache.

```python
from django_toolkit.concurrent.locks import CacheLock

def run(*args, **kwargs):
    with CacheLock(key='key', cache_alias='lock', expire=10):
        # do some stuff
```

You can control lock to don't raise `LockActiveError` exception.
The attribute `active` will indicate whether lock acquiring was successful or
not.

```python
from django_toolkit.concurrent.locks import CacheLock

def run(*args, **kwargs):
    with CacheLock(key='key', raise_exception=False) as lock:
        assert lock.active

    with CacheLock(key='key', raise_exception=False) as lock:
        if lock.active:
            # do some stuff, lock is now active
        else:
            # do other stuff, lock was not acquired
```

You can persist the lock in the cache by setting delete_on_exit = False. 
This makes the key remains in cache until the end expiration time

```python
from django_toolkit.concurrent.locks import CacheLock

def run(*args, **kwargs):
    with CacheLock(key='key', delete_on_exit=False) as lock:
        assert lock.active
    assert lock.cache.get(lock._key)
```
