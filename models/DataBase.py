import sqlite3 as sql 

class DataBase:
    
    db_name = "PharmacySystem.db"
    
    def connect_to_db(self): 
        connection = sql.connect(self.db_name)
        cursor = connection.cursor()
        return connection, cursor
    
    def close_connection(self, connection): 
        connection.commit()
        connection.close()
        
    def insert(self, prefix, table, obj):
        data = {key: value for key, value in vars(obj).items() if key != 'id'}
        
        fields = ', '.join([f"{prefix}{field}" for field in data.keys()])
        values = ', '.join([f"'{value}'" if not isinstance(value, (float, int)) else f"{value}" for value in data.values()])
        connection, cursor = self.connect_to_db()
        
        cursor.execute(
            f'''
            INSERT INTO {table} ({fields})
            VALUES ({values})
            '''
        )
        self.close_connection(connection)
        
    def update(self, table, field, value, condition_field, condition_value): 
        connection, cursor = self.connect_to_db()
        
        set_condition   = f"SET {field} = '{value}'" if not isinstance(condition_value, (int, float)) \
            else f"SET {field} = {value}"
        where_condition = f"WHERE {condition_field} = '{condition_value}'" if not isinstance(condition_value, (int, float)) \
            else f"WHERE {condition_field} = {condition_value}"
        
        cursor.execute(
            f'''
            UPDATE {table}
            {set_condition}
            {where_condition}
            '''
        )
        self.close_connection(connection)
        
    def select_all(self, table): 
        connection, cursor = self.connect_to_db()
        
        cursor.execute(
            f'''
            SELECT * FROM {table}
            '''
        )
        data = cursor.fetchall()
        self.close_connection(connection)
        
        return data
    
    def select_where(self, table, field, value): 
        connection, cursor = self.connect_to_db()
        
        cursor.execute(
            f'''
            SELECT * FROM {table} WHERE {field} LIKE '%{value}%'
            '''
        )
        data = cursor.fetchall()
        self.close_connection(connection)
        
        return data
    
    def select_multiple_tables(self, tables, field, value): 
        connection, cursor = self.connect_to_db()
        main_table = list(tables.keys())[0]
        main_table_prefix = list(tables.values())[0]

        columns = f"{main_table}.*"        
        joins = " JOIN "
        joins += " JOIN ".join(f'{table} ON {main_table}.{main_table_prefix}{prefix}id = {table}.{prefix}id' for table, prefix in list(tables.items())[1::])
        
        for table, prefix in dict(tables.items()).items(): 
            if f'{prefix}id' == field:
                where_table = (table, prefix)
                        
        cursor.execute(f'''
            SELECT {columns}
            FROM {main_table}
            {joins}
            WHERE {where_table[0]}.{where_table[1]}name = '{value}'
            '''
        )
        
        data = cursor.fetchall()
        self.close_connection(connection)
        
        return data
    
    def select_where_multiple_fields(self, table, prefix, fields): 
        connection, cursor = self.connect_to_db()
        
        where_sentence = "WHERE "
        conditions = []

        for field, value in fields.items():
            if isinstance(value, str):
                conditions.append(f"{prefix}{field} = '{value}'")
            else:
                conditions.append(f"{prefix}{field} = {value}")

        where_sentence += " AND ".join(conditions)
        
        cursor.execute(
            f'''
            SELECT * FROM {table} {where_sentence}
            '''
        )
        data = cursor.fetchall()
        self.close_connection(connection)
        
        return data
        