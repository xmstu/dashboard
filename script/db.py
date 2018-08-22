# coding=utf-8
import logging
import pymysql
from queue import Queue
import threading
import time
import re
import datetime
import uuid

logger = logging.getLogger(__name__)


class PoolError(Exception):
    """连接异常类"""
    pass


class PooledConnection(object):
    """连接池"""

    def __init__(self, connection_strings, max_count=10, min_free_count=1, keep_conn_alive=False):
        self._max_count = max_count
        self._min_free_count = min_free_count
        self._connection_strings = connection_strings
        self._count = 0
        self._queue = Queue(max_count)
        self._lock = threading.Lock()
        if keep_conn_alive:
            self._run_ping()

    def __del__(self):
        while not self._queue.empty():
            conn_info = self._queue.get()
            conn = conn_info.get('connection') if conn_info else None
            if conn:
                self._close_connection(conn)
            else:
                break

    def _run_ping(self):
        '开启一个后台线程定时 ping 连接池里的连接，保证池子里的连接可用'

        def ping_conn(pool_queue, pool_lock):
            # 每5分钟检测池子里未操作过的连接进行ping操作，移除失效的连接
            pre_time = time.time()
            per_seconds = 300
            while True:
                if pre_time <= time.time() - per_seconds:
                    while not pool_queue.empty():
                        conn = None
                        usable = True
                        pool_lock.acquire()
                        try:
                            conn_info = pool_queue.get()
                            if conn_info:
                                if conn_info.get('active_time') <= time.time() - per_seconds:
                                    conn = conn_info.get('connection')
                                    try:
                                        conn._conn.ping()
                                    except:
                                        usable = False
                                else:
                                    # 只要遇到连接的激活时间未到 ping 时间就结束检测后面的连接【Queue的特性决定了后面的连接都不需要检测】
                                    break
                        except:
                            pass
                        finally:
                            pool_lock.release()
                        # 必须放在 lock 的外面，避免在做drop和release的时候死锁
                        if conn:
                            if not usable:
                                conn.drop()
                            else:
                                conn.release()
                    pre_time = time.time()
                else:
                    time.sleep(2)

        thread = threading.Thread(target=ping_conn, args=(self._queue, self._lock), daemon=True)
        thread.start()

    def _create_connection(self, auto_commit=True):
        if self._count >= self._max_count:
            raise PoolError('The maximum number of connections beyond!')
        conn = Connection(self, host=self._connection_strings.get('host'),
                          port=self._connection_strings.get('port'),
                          user=self._connection_strings.get('user'),
                          password=self._connection_strings.get('password'),
                          db=self._connection_strings.get('database'),
                          charset=self._connection_strings.get('charset', 'utf8'),
                          autocommit=auto_commit,
                          cursorclass=pymysql.cursors.DictCursor)
        self._count += 1
        return conn

    def release_connection(self, connection):
        """释放连接"""
        self._lock.acquire()
        try:
            if self._queue.qsize() >= self._min_free_count:
                self._close_connection(connection)
            else:
                self._queue.put({'connection': connection, 'active_time': time.time()})
        except:
            pass
        finally:
            self._lock.release()

    def get_connection(self, timeout=15):
        """获取一个连接"""
        begin_time = datetime.datetime.now()

        def get_conn():
            '获取连接'
            self._lock.acquire()
            try:
                if not self._queue.empty():
                    conn_info = self._queue.get()
                    conn = conn_info.get('connection') if conn_info else None
                elif self._count < self._max_count:
                    conn = self._create_connection()
                else:
                    conn = None
                return conn
            except:
                raise
            finally:
                self._lock.release()

        conn = get_conn()
        if conn:
            return conn
        else:
            if timeout:
                while (datetime.datetime.now() - begin_time).seconds < timeout:
                    conn = get_conn()
                    if conn:
                        break
                    time.sleep(0.2)
            if not conn:
                raise PoolError('Timeout!There has no enough connection to be used!')
            return conn

    def _close_connection(self, connection):
        """关闭连接"""
        try:
            if connection._close():
                self._count -= 1
        except:
            pass


class Connection(object):
    """连接类"""
    PARAMERTS_REG = re.compile(r'\:([_0-9]*[_A-z]+[_0-9]*[_A-z]*)')

    def __init__(self, pool, *args, **kwargs):
        self._pool = pool
        self.id = uuid.uuid4()
        # 连不上数据库时，自动重试
        try:
            self._conn = pymysql.connections.Connection(*args, **kwargs)
            self.__is_closed = False
        except pymysql.err.OperationalError:
            self._conn = pymysql.connections.Connection(*args, **kwargs)
            self.__is_closed = False

    def __del__(self):
        """销毁连接"""
        self.drop()

    def execute(self, sql, args=None):
        """执行 sql"""
        cursor = self._conn.cursor()
        sql_text = self.PARAMERTS_REG.sub(r'%(\1)s', sql)
        model_attrs = []
        result = self.PARAMERTS_REG.finditer(sql)
        for match in result:
            model_attrs.append(match.group(1))

        def filter_args(attrs, model):
            '过滤参数'
            if model is None:
                return None
            return {a: model[a] for a in attrs}

        if args and isinstance(args, list):
            cursor.executemany(
                sql_text, [filter_args(model_attrs, a) for a in args])
        else:
            cursor.execute(sql_text, filter_args(model_attrs, args))
        return cursor

    def insert(self, sql, args=None):
        """插入记录"""
        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_id = cursor.lastrowid
            return row_id
        except:
            raise
        finally:
            cursor and cursor.close()

    def update(self, sql, args=None):
        """更新记录"""
        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_count = cursor.rowcount
            if not row_count:
                logger.debug(cursor._last_executed)
            return row_count
        except:
            raise
        finally:
            cursor and cursor.close()

    def delete(self, sql, args=None):
        """删除记录"""
        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_count = cursor.rowcount
            return row_count
        except:
            raise
        finally:
            cursor and cursor.close()

    def query(self, sql, args=None):
        """查询"""
        cursor = None
        try:
            cursor = self.execute(sql, args)
            return cursor.fetchall()
        except:
            raise
        finally:
            cursor and cursor.close()

    def query_one(self, sql, args=None):
        """查询返回一条数据"""
        cursor = None
        try:
            cursor = self.execute(sql, args)
            return cursor.fetchone()
        except:
            raise
        finally:
            cursor and cursor.close()

    def release(self):
        """释放连接，将连接放回连接池"""
        self._pool.release_connection(self)

    def close(self):
        """释放连接，将连接放回连接池"""
        self.release()

    def drop(self):
        """丢弃连接"""
        self._pool._close_connection(self)

    def _close(self):
        """真正关闭"""
        if self.__is_closed:
            return False
        try:
            self._conn.close()
            self.__is_closed = True
        except:
            logger.error('mysql connection close error', exc_info=True)
        return True


class MySQLdb(object):
    """mysql 的数据库操作类，支持连接池"""

    def __init__(self, cfg):
        self.config = cfg
        self._pool = PooledConnection(self.config,
                                      self.config.get('maxConnections'),
                                      self.config.get('minFreeConnections', 1),
                                      self.config.get('keepConnectionAlive', False))

    def execute(self, sql, args=None):
        """执行 sql"""
        cursor = None
        conn = None
        try:
            try:
                conn = self._pool.get_connection()
                cursor = conn.execute(sql, args)
            except (pymysql.err.OperationalError, RuntimeError):
                logger.error('execute error ready to retry', exc_info=True)
                conn and conn.drop()
                conn = self._pool.get_connection()
                cursor = conn.execute(sql, args)
        except (pymysql.err.InterfaceError, pymysql.err.IntegrityError):
            raise
        except:
            logger.error('MySQLdb execute error', exc_info=True)
            conn and conn.drop()
            conn = None
            raise
        finally:
            conn and conn.release()
        return cursor

    def insert(self, sql, args=None):
        """插入记录"""
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                row_id = cursor.lastrowid
                return row_id
            return None
        except:
            raise
        finally:
            cursor and cursor.close()

    def update(self, sql, args=None):
        """更新记录"""
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                row_count = cursor.rowcount
                return row_count
            return 0
        except:
            raise
        finally:
            cursor and cursor.close()

    def delete(self, sql, args=None):
        """删除记录"""
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                row_count = cursor.rowcount
                return row_count
            return 0
        except:
            raise
        finally:
            cursor and cursor.close()

    def query(self, sql, args=None):
        """查询"""
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                return cursor.fetchall()
            return None
        except:
            raise
        finally:
            cursor and cursor.close()

    def query_one(self, sql, args=None):
        """查询返回一条数据"""
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                return cursor.fetchone()
            return None
        except:
            raise
        finally:
            cursor and cursor.close()

    def begin(self):
        """开启并返回一个事务"""
        tran = Transaction(self._pool.get_connection())
        tran.begin()
        return tran

    def commit(self, tran):
        """提交事务"""
        return tran.commit()

    def rollback(self, tran):
        """回滚事务"""
        return tran.rollback()


class Transaction(object):
    """事务类"""

    def __init__(self, conn):
        self.__is_began = False
        self.conn = conn
        self.__old_autocommit = self.conn._conn.get_autocommit()
        self.conn._conn.autocommit(False)

    def begin(self):
        """开启事务"""
        if not self.__is_began:
            self.conn._conn.begin()
            self.__is_began = True

    def commit(self):
        """提交事务"""
        self.conn._conn.commit()
        self.__is_began = False
        self._finished()

    def rollback(self):
        """回滚事务"""
        self.conn._conn.rollback()
        self.__is_began = False
        self._finished()

    def _finished(self):
        self.__reset_autocommit()
        self.conn.release()

    def __reset_autocommit(self):
        """将连接的自动提交设置重置回原来的设置"""
        self.conn._conn.autocommit(self.__old_autocommit)

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()