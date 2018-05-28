# coding=utf-8
# author=veficos

import pathlib
import logging, os
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.recipe.lock import Lock


log = logging


class DistributedLockTimeout(Exception):
    pass


class DistributedLockConnectFailure(Exception):
    pass


class DistributedLock(object):
    def __init__(self, hosts, name, rootpath='/distributed_locks/', timeout=10.0, logger=None):
        if logger:
            global log
            log = logger

        self.timeout = timeout
        self.name = name

        try:
            self.zk_client = KazooClient(hosts=hosts, logger=log, timeout=timeout)
            self.zk_client.start(timeout=self.timeout)
        except Exception as ex:
            log.debug('[DistributedLock] Create KazooClient failed! Exception: %s' % ex)
            raise DistributedLockConnectFailure(ex)

        try:
            self.lock = Lock(self.zk_client, (pathlib.PurePath(rootpath) / name).as_posix())
        except Exception as ex:
            log.debug('[DistributedLock] Create lock failed! Exception: %s' % str(ex))
            raise DistributedLockConnectFailure(ex)

    def __del__(self):
        self.zk_client.stop()

    def acquire(self, blocking=True, timeout=None):
        if not self.lock:
            return None

        try:
            log.debug('[DistributedLock] Acquire lock')
            return self.lock.acquire(blocking=blocking, timeout=timeout)
        except Exception as ex:
            log.debug("[DistributedLock] Acquire lock failed! Exception: %s" % ex)
            raise DistributedLockTimeout(ex)

    def release(self):
        if not self.lock:
            return None

        log.debug('[DistributedLock] Release lock')
        return self.lock.release()

    def __enter__(self):
        self.acquire(timeout=self.timeout)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            pass
        self.release()


class SynchronizedScope(object):
    def __init__(self, lock, blocking=True, timeout=None):
        self.lock = lock
        self.timeout = timeout
        self.blocking = blocking

    def __enter__(self):
        self.lock.acquire(blocking=self.blocking, timeout=self.timeout)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            pass
        self.lock.release()


if __name__ == '__main__':
    import time

    z = DistributedLock('192.168.10.139:31081,192.168.10.139:31082,192.168.10.139:31083', name='test_zkname')


    def test_lock():
        with SynchronizedScope(z):
            pass


    t = time.time()
    for _ in range(2000):
        test_lock()

    # windows
    # 56.956626176834106
    # 0.028478313088417053

    # linux
    # 52.96471643447876
    # 0.026482382655143737
    print(time.time() - t)
    print((time.time() - t) / 2000)

    from concurrent.futures import ThreadPoolExecutor

    pool = ThreadPoolExecutor(20)

    t = time.time()
    for _ in range(2000):
        pool.submit(test_lock)
    pool.shutdown()

    # windows
    # 111.504225730896
    # 0.055752112865448

    # linux
    # 137.80438566207886
    # 0.06890224719047547
    print(time.time() - t)
    print((time.time() - t) / 2000)