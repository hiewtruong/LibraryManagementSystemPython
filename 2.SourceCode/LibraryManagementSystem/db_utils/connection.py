import pyodbc
from contextlib import contextmanager
import json
import os

class DatabaseConnection:
    def __init__(self, config_file="config.json"):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"File cấu hình {config_file} không tồn tại.")
        
        with open(config_file, 'r') as f:
            config = json.load(f)

        self.server = config.get('DB_SERVER')
        self.database = config.get('DB_NAME')
        self.username = config.get('DB_USERNAME')
        self.password = config.get('DB_PASSWORD')
        self.conn = None

        if not all([self.server, self.database, self.username, self.password]):
            raise ValueError("Một hoặc nhiều giá trị cấu hình không được tìm thấy. Kiểm tra file config.json.")

    def get_connection(self):
        try:
            connection_string = f'''
                DRIVER={{ODBC Driver 17 for SQL Server}};
                SERVER={self.server};
                DATABASE={self.database};
                UID={self.username};
                PWD={self.password};
            '''
            self.conn = pyodbc.connect(connection_string)
            return self.conn
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    @contextmanager
    def transaction(self):
        try:
            yield self.conn
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Lỗi giao dịch: {e}")
            raise
        finally:
            self.close()