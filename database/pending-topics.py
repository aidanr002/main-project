import sqlite3
import hashlib

class PendingTopics (object):
# Creates object using information from database information #
    def __init__(self, name, description, pendingtopicid=None):
        self.pendingtopicid = pendingtopicid
        self.name = name
        self.description = description

    def __str__(self):
        return "name: '{}', description: '{}', pendingtopicid: '{}'".format(self.name, self.description, self.pendingtopicid)

def get_newpending_topic(db_file, pendingtopicid):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pending_topics WHERE pendingtopicid = ?;",(int(pendingtopicid),))
    topic = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return topic

def get_allnewpending_topics(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pending_topics")
    selected_comments = []
    for row in cur:
        pendingtopicid, name, description = row
        atopic = PendingTopics(name, description, pendingtopicid)
        selected_comments.append(atopic)
    conn.commit()
    cur.close()
    conn.close()
    return selected_comments

def create_newpending_topic(db_file, information):
    """Creates a new topic using information passed to the function."""
    name, description = information
    pendingtopic = PendingTopics(name, description)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute('SELECT max(pendingtopicid) FROM pending_topics')
    pendingtopicid = cur.fetchone()[0] + 1
    cur.execute("""INSERT INTO pending_topics (pendingtopicid, name, description)
                VALUES (?,?,?);""",(pendingtopicid, name, description))
    conn.commit()
    cur.close()
    conn.close()
    return pendingtopic

def remove_newpending_topic(db_file, pendingtopicid):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM pending_topics WHERE pendingtopicid = ?;",(pendingtopicid,))
    conn.commit()
    cur.close()
    conn.close()
