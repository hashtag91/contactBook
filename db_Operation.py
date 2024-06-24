import sqlite3

def db_adding(name, phone, email, adress, path):
    try:
        conn = sqlite3.connect("Database.db")
        cur = conn.cursor()
        req = "INSERT INTO carnet (name,telephone,email,adress,path) VALUES (?,?,?,?,?)"
        cur.execute(req, (name,phone,email,adress,path))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        print(e)
        return False
def db_trievment():
    try:
        conn = sqlite3.connect("Database.db")
        cur = conn.cursor()
        req = "SELECT * FROM carnet"
        cur.execute(req)
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data
    except Exception as e:
        conn.rollback()
        return False
def selected_retrieve(email):
    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()
    req = "SELECT * FROM carnet WHERE email=?"
    try:
        cur.execute(req,[email])
        data = cur.fetchone()
        conn.commit()
        conn.close()
        return data
    except Exception as e:
        conn.rollback()
        return False
def db_update(data:list):
    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()
    req = """UPDATE carnet 
            SET name=?, telephone=?, email=?, adress=?, path=?
            WHERE email=?"""
    try:
        cur.execute(req,data)
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        print(e)
def db_deletion(email):
    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()
    req = "DELETE FROM carnet WHERE email=?"
    try:
        cur.execute(req,[email])
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        print(e)