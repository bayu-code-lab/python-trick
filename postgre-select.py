import psycopg2

class PostgresDBManager:
    def __init__(self,query,values,is_update):
        self.query=query
        self.is_update=is_update
        self.values=values
        self.connection=psycopg2.connect(
            user = 'user',
            password = 'password',
            host = 'host',
            port = 'port',
            database = 'database-name'
        )

        self.cursor=self.connection.cursor()

    def __enter__(self):
        self.cursor.execute(self.query,self.values)
        if self.is_update ==True:
            self.connection.commit()
        return self.cursor

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.connection.close()
        self.cursor.close()
       
#example get all and singlee data
column_name = ['salt', 'password']
query = """
        select {column_name} from mpm_customer.mst_customer limit 1
"""
settings = {'column_name': ','.join(column_name)}
query = query.format(**settings)
    
with PostgresDBManager(query, None, False) as cursor: #query Select All
    result = []
    for item in cursor.fetchall():
        row = {}
        for a, b in zip(column_name, item):
            row[a] = b
        result.append(row)
    print(result)


with PostgresDBManager(query, None, False) as cursor: #query Select One
    data = cursor.fetchone()
    result = {}
    if data is not None:
        for a, b in zip(column_name, data):
            result[a] = b
    print(result)
