import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="123sishen321", database="school_library"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except Error as e:
            print(f"连接数据库时出错: {e}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params or ())
            
            if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE')):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.rowcount
        except Error as e:
            print(f"执行查询时出错: {e}")
            return None

    def execute_procedure(self, procedure_name, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            # 构建调用存储过程的SQL语句
            if params is None:
                params = []
            
            # 确保所有参数都被正确处理，避免类型转换问题
            processed_params = []
            for param in params:
                if isinstance(param, str) and param.startswith('@'):
                    # 对于输出参数，使用变量声明
                    var_name = param[1:]  # 去掉@符号
                    self.cursor.execute(f"SET @{var_name} = NULL")
                    processed_params.append(f"@{var_name}")
                else:
                    processed_params.append(param)
            
            param_placeholders = ', '.join(['%s' if not isinstance(p, str) or not p.startswith('@') else p for p in processed_params])
            call_query = f"CALL {procedure_name}({param_placeholders})"
            
            # 执行存储过程，不使用 multi=True 参数
            self.cursor.execute(call_query, [p for p in processed_params if not isinstance(p, str) or not p.startswith('@')])
            
            # 获取所有结果集
            results = []
            result = self.cursor.fetchall()
            if result:
                results.append(result)
            
            # 处理可能的多个结果集
            while self.cursor.nextset():
                result = self.cursor.fetchall()
                if result:
                    results.append(result)
            
            # 获取输出参数的值
            output_params = {}
            for param in params:
                if isinstance(param, str) and param.startswith('@'):
                    var_name = param[1:]  # 去掉@符号
                    self.cursor.execute(f"SELECT @{var_name} AS value")
                    output_value = self.cursor.fetchone()
                    if output_value:
                        output_params[var_name] = output_value['value']
            
            # 将输出参数添加到结果中
            if output_params:
                results.append([output_params])
            
            return results
        except Error as e:
            print(f"执行存储过程时出错: {e}")
            return None 