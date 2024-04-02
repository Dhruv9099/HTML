import cx_Oracle
import psycopg2

class DatabaseHandler:
    def __init__(self, oracle_config, postgresql_config):
        self.oracle_config = oracle_config
        self.postgresql_config = postgresql_config
        self.oracle_connection = None
        self.oracle_cursor = None
        self.postgresql_connection = None
        self.postgresql_cursor = None

    def connect_to_oracle(self):
        try:
            self.oracle_connection = cx_Oracle.connect(
                user=self.oracle_config['username'],
                password=self.oracle_config['password'],
                dsn=cx_Oracle.makedsn(
                    self.oracle_config['host'],
                    self.oracle_config['port'],
                    service_name=self.oracle_config['service_name']
                )
            )
            self.oracle_cursor = self.oracle_connection.cursor()
            print("Connected to Oracle database.")
        except cx_Oracle.DatabaseError as e:
            print("Error:", e)

    def connect_to_postgresql(self):
        try:
            self.postgresql_connection = psycopg2.connect(
                user=self.postgresql_config['username'],
                password=self.postgresql_config['password'],
                host=self.postgresql_config['host'],
                port=self.postgresql_config['port'],
                database=self.postgresql_config['database']
            )
            self.postgresql_cursor = self.postgresql_connection.cursor()
            print("Connected to PostgreSQL database.")
        except psycopg2.DatabaseError as e:
            print("Error:", e)

    def close_connections(self):
        if self.oracle_cursor:
            self.oracle_cursor.close()
        if self.oracle_connection:
            self.oracle_connection.close()
        if self.postgresql_cursor:
            self.postgresql_cursor.close()
        if self.postgresql_connection:
            self.postgresql_connection.close()
        print("Connections closed.")

    def select_from_oracle(self, table):
        self.oracle_cursor.execute(f"SELECT * FROM {table}")
        data = self.oracle_cursor.fetchall()
        print("Oracle Data:")
        for row in data:
            print(row)

    def select_from_postgresql(self, table):
        self.postgresql_cursor.execute(f"SELECT * FROM {table}")
        data = self.postgresql_cursor.fetchall()
        print("PostgreSQL Data:")
        for row in data:
            print(row)

    def insert_into_oracle(self, table, values):
        self.oracle_cursor.execute(f"INSERT INTO {table} VALUES {values}")
        self.oracle_connection.commit()
        print("Inserted into Oracle table.")

    def insert_into_postgresql(self, table, values):
        self.postgresql_cursor.execute(f"INSERT INTO {table} VALUES {values}")
        self.postgresql_connection.commit()
        print("Inserted into PostgreSQL table.")

    def update_oracle(self, table, column, new_value, condition):
        self.oracle_cursor.execute(f"UPDATE {table} SET {column} = {new_value} WHERE {condition}")
        self.oracle_connection.commit()
        print("Updated Oracle table.")

    def update_postgresql(self, table, column, new_value, condition):
        self.postgresql_cursor.execute(f"UPDATE {table} SET {column} = {new_value} WHERE {condition}")
        self.postgresql_connection.commit()
        print("Updated PostgreSQL table.")

    def delete_from_oracle(self, table, condition):
        self.oracle_cursor.execute(f"DELETE FROM {table} WHERE {condition}")
        self.oracle_connection.commit()
        print("Deleted from Oracle table.")

    def delete_from_postgresql(self, table, condition):
        self.postgresql_cursor.execute(f"DELETE FROM {table} WHERE {condition}")
        self.postgresql_connection.commit()
        print("Deleted from PostgreSQL table.")

# Example usage
oracle_config = {
    'username': 'your_oracle_username',
    'password': 'your_oracle_password',
    'host': 'your_oracle_host',
    'port': 'your_oracle_port',
    'service_name': 'your_oracle_service_name'
}

postgresql_config = {
    'username': 'your_postgresql_username',
    'password': 'your_postgresql_password',
    'host': 'your_postgresql_host',
    'port': 'your_postgresql_port',
    'database': 'your_postgresql_database'
}

db_handler = DatabaseHandler(oracle_config, postgresql_config)
db_handler.connect_to_oracle()
db_handler.connect_to_postgresql()

# Perform CRUD operations
# Example: Select from Oracle
db_handler.select_from_oracle('your_oracle_table')

# Example: Select from PostgreSQL
db_handler.select_from_postgresql('your_postgresql_table')

# Example: Insert into Oracle
db_handler.insert_into_oracle('your_oracle_table', "('value1', 'value2')")

# Example: Insert into PostgreSQL
db_handler.insert_into_postgresql('your_postgresql_table', "('value1', 'value2')")

# Example: Update Oracle
db_handler.update_oracle('your_oracle_table', 'column1', "'new_value'", 'column2 = 'value2'')

# Example: Update PostgreSQL
db_handler.update_postgresql('your_postgresql_table', 'column1', "'new_value'", 'column2 = 'value2'')

# Example: Delete from Oracle
db_handler.delete_from_oracle('your_oracle_table', 'column1 = 'value1'')

# Example: Delete from PostgreSQL
db_handler.delete_from_postgresql('your_postgresql_table', 'column1 = 'value1'')

db_handler.close_connections()
