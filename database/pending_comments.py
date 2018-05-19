import sqlite3 #Imports modules
import hashlib

class PendingComments(object): #Sets up constructor for object that will have attributes. This object can be used in server.py. Specific attributes can be pulled from it.
    def __init__(self, topicid, username, usercountry, stance, comment, pendingcommentid = None):
        self.username = username
        self.usercountry = usercountry
        self.topicid = topicid
        self.stance = stance
        self.comment = comment
        self.pendingcommentid = pendingcommentid

    def __str__(self): #Decodes the object so it is printable
        return "username: '{}', usercountry: '{}', topicid: '{}', stance: '{}', comment '{}', pendingcommentid: '{}'".format(self.username, self.usercountry, self.topicid, self.stance, self.comment, self.pendingcommentid)

def remove_newpending_comment(db_file, pendingcommentid): #Takes in pending comment id, opens a connection to db file, removes the line from the file (line at id) and closes the connection.
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM pending_comments WHERE pendingcommentid = ?;",(pendingcommentid,))
    conn.commit()
    cur.close()
    conn.close()

def get_newpending_comment(db_file, pendingcommentid):  #Takes in a id, opens a connection, searches the db for matching entries, adds the matching results to list, converts the list to an object and returns this to the calling file. Then closes the connection.
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pending_comments WHERE pendingcommentid = ?;",(pendingcommentid,))
    comment = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return comment

def get_allnewpending_comment(db_file): #Opens a connection with the db, Gets all comments from the database, adds them to a list, returns the list to the server and terminates the connection.
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pending_comments")
    selected_comments = []
    for row in cur:
        pendingcommentid, topicid, username, usercountry, stance, comment = row
        acomment = PendingComments(topicid, username, usercountry, stance, comment, pendingcommentid)
        selected_comments.append(acomment)
    conn.commit()
    cur.close()
    conn.close()
    return selected_comments

def create_newpending_comment(db_file, information): #Takes in a list of information, opens a connection, creates a new row with that information + an id 1 number larger than the previous id. Saves row and closes connection.
    """Creates a new comment using information passed to the function."""
    topicid, username, usercountry, stance, comment = information
    pendingcomments = PendingComments(topicid, username, usercountry, stance, comment)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute('SELECT max(pendingcommentid) FROM pending_comments')
    pendingcommentid = cur.fetchone()[0] + 1
    cur.execute("""INSERT INTO pending_comments (topicid, username, usercountry, stance, comment, pendingcommentid)
                VALUES (?,?,?,?,?,?);""",(int(topicid), str(username), str(usercountry), str(stance), str(comment), int(pendingcommentid)))
    conn.commit()
    cur.close()
    conn.close()
    return pendingcomments
