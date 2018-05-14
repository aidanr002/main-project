import sqlite3
import hashlib

class Customer(object):
    """Creates user object from database"""
    def __init__(self, fname, lname, email, country, bio, username, password, id= None):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.country = country
        self.bio = bio
        self.username = username
        self.password = password
    def __str__(self):
        return "fname: '{}', lname: '{}', email: '{}', country: '{}', bio: '{}', id:'{}', username: '{}', password: '{}'".format(self.fname, self.lname, self.email, self.country, self.bio, self.id, self.username, self.password)

def update_profile(db_file, fieldstoupdate, newfieldinfo, userid):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("UPDATE users SET fname = ? WHERE userid = ?;",(newfieldinfo[0], userid,))
    conn.commit()
    cur.execute("UPDATE users SET lname = ? WHERE userid = ?;",(newfieldinfo[1], userid,))
    conn.commit()
    cur.execute("UPDATE users SET email = ? WHERE userid = ?;",(newfieldinfo[2], userid,))
    conn.commit()
    cur.execute("UPDATE users SET country = ? WHERE userid = ?;",(newfieldinfo[3], userid,))
    conn.commit()
    cur.execute("UPDATE users SET bio = ? WHERE userid = ?;",(newfieldinfo[4], userid,))
    conn.commit()
    cur.execute("UPDATE users SET username = ? WHERE userid = ?;",(newfieldinfo[5], userid,))
    conn.commit()
    cur.execute("UPDATE users SET password = ? WHERE userid = ?;",(newfieldinfo[6], userid,))
    conn.commit()
    cur.close()
    conn.close()

def remove_user(db_file, userid):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE userid = ?;",(userid,))
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_username(db_file, username):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?;",(username,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row == None:
        return None
    id, fname, lname, email, country, bio, username, password = row
    user = Customer(fname, lname, email, country, bio, username, password, id)
    return user

def get_user(db_file, id):
    """Returns information about a customer (user) from the database."""
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE userid = ?;",(id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row == None:
        return None
    id, fname, lname, email, country, bio, username, password = row
    user = Customer(fname, lname, email, country, bio, username, password, id)
    return user

def create_user(db_file, information):
    """Creates a new user using information passed to the function."""
    fname, lname, email, country, bio, username, password = information
    user = Customer(fname, lname, email, country, bio, username, password)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("""INSERT INTO users (fname, lname, email, country, bio,username, password)
                VALUES (?,?,?,?,?,?,?);""",(fname, lname, email, country, bio, username, password))
    user.id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return user
