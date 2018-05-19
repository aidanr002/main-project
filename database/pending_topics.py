import sqlite3
import hashlib

class PendingTopics (object): #Sets up constructor for object that will have attributes. This object can be used in server.py. Specific attributes can be pulled from it.
# Creates object using information from database information #
    def __init__(self, name, description, pendingtopicid=None):
        self.pendingtopicid = pendingtopicid
        self.name = name
        self.description = description

    def __str__(self): #Decodes the object so it is printable
        return "name: '{}', description: '{}', pendingtopicid: '{}'".format(self.name, self.description, self.pendingtopicid)

def get_newpending_topic(db_file, pendingtopicid):  #Takes in a id, opens a connection, searches the db for matching entries, adds the matching results to list, converts the list to an object and returns this to the calling file. Then closes the connection.
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pending_topics WHERE pendingtopicid = ?;",(int(pendingtopicid),))
    topic = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return topic

def get_allnewpending_topics(db_file): #Opens a connection with the db, Gets all comments from the database, adds them to a list, returns the list to the server and terminates the connection.
    conn = sqlite3.connect(db_file)
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

def create_newpending_topic(db_file, information): #Takes in a list of information, opens a connection, creates a new row with that information + an id 1 number larger than the previous id. Saves row and closes connection.
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

def remove_newpending_topic(db_file, pendingtopicid): #Takes in pending topic id, opens a connection to db file, removes the line from the file (line at id) and closes the connection.
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM pending_topics WHERE pendingtopicid = ?;",(pendingtopicid,))
    conn.commit()
    cur.close()
    conn.close()
