import sqlite3
import hashlib

class PendingComments(object):
    def __init__(self, topicid, username, usercountry, stance, comment, pendingcommentid = None):
        self.username = username
        self.usercountry = usercountry
        self.topicid = topicid
        self.stance = stance
        self.comment = comment
        self.pendingcommentid = pendingcommentid

    def __str__(self):
        return "username: '{}', usercountry: '{}', topicid: '{}', stance: '{}', comment '{}', pendingcommentid: '{}'".format(self.username, self.usercountry, self.topicid, self.stance, self.comment, self.pendingcommentid)

def remove_newpending_comment(db_file, pendingcommentid):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM pending_comments WHERE pendingcommentid = ?;",(pendingcommentid,))
    conn.commit()
    cur.close()
    conn.close()

def get_newpending_comment(db_file, pendingcommentid):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pending_comments WHERE pendingcommentid = ?;",(pendingcommentid,))
    comment = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return comment

def get_allnewpending_comment(db_file):
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

def create_newpending_comment(db_file, information):
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
