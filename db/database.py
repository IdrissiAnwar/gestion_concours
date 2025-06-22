import mysql

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="concours"
    )

def get_admin_by_username(username):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
    result = cursor.fetchone()
    conn.close()
    return result