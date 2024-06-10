import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(dbname="bot_schemes", user="evraz", password="123456789", host="localhost", port='5434')
        self.conn.autocommit = True

    def query(self, request, params = []):
        cursor = self.conn.cursor()
        if len(params) == 0:
            cursor.execute(request)
        else:
            cursor.execute(request, params)
        return cursor.fetchall()    
    
    def release(self):
        self.conn.close()