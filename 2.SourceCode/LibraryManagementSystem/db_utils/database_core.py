import pyodbc
import json
import os
from contextlib import contextmanager
import threading

class DbUtils:
    _config_path = "config.json"
    _thread_local = threading.local()

    @classmethod
    def _load_config(cls):
        if not os.path.exists(cls._config_path):
            raise FileNotFoundError(f"Config file {cls._config_path} not found.")
        with open(cls._config_path, 'r') as f:
            config = json.load(f)
        return config

    @classmethod
    def get_connection(cls):
        conn = getattr(cls._thread_local, 'connection', None)
        if conn is None or not conn:
            config = cls._load_config()
            connection_string = f"""
                DRIVER={{ODBC Driver 17 for SQL Server}};
                SERVER={config['DB_SERVER']};
                DATABASE={config['DB_NAME']};
                UID={config['DB_USERNAME']};
                PWD={config['DB_PASSWORD']};
            """
            conn = pyodbc.connect(connection_string)
            cls._thread_local.connection = conn
        return conn

    @classmethod
    def begin_transaction(cls):
        conn = cls.get_connection()
        conn.autocommit = False

    @classmethod
    def commit(cls):
        conn = getattr(cls._thread_local, 'connection', None)
        if conn:
            conn.commit()

    @classmethod
    def rollback(cls):
        conn = getattr(cls._thread_local, 'connection', None)
        if conn:
            conn.rollback()

    @classmethod
    def close(cls):
        conn = getattr(cls._thread_local, 'connection', None)
        if conn:
            try:
                conn.autocommit = True
                conn.close()
            except Exception as e:
                print(f"Error closing connection: {e}")
            finally:
                cls._thread_local.connection = None

    @classmethod
    def update(cls, sql, *args):
        conn = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, args)
            conn.commit()
        finally:
            cls.close()

    @classmethod
    def get_stmt(cls, sql):
        conn = cls.get_connection()
        return conn.cursor()

    @classmethod
    def query(cls, sql, *args):
        try:
            cursor = cls.get_stmt(sql)
            cursor.execute(sql, args)
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Query error: {e}")

    @classmethod
    def value(cls, sql, *args):
        try:
            cursor = cls.get_stmt(sql)
            cursor.execute(sql, args)
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            raise RuntimeError(f"Value error: {e}")

    @classmethod
    @contextmanager
    def transaction(cls):
        try:
            cls.begin_transaction()
            yield cls.get_connection()
            cls.commit()
        except Exception as e:
            cls.rollback()
            raise
        finally:
            cls.close()

get_connection = DbUtils.get_connection
begin_transaction = DbUtils.begin_transaction
commit = DbUtils.commit
rollback = DbUtils.rollback
close = DbUtils.close
update = DbUtils.update
get_stmt = DbUtils.get_stmt
query = DbUtils.query
value = DbUtils.value
transaction = DbUtils.transaction 