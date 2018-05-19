import sqlite3
import hashlib

class Topics (object): #Sets up constructor for object that will have attributes. This object can be used in server.py. Specific attributes can be pulled from it.
# Creates object using information from database information #
    def __init__(self, name, description, topicid=None):
        self.topicid = topicid
        self.name = name
        self.description = description

    def __str__(self): #Decodes the object so it is printable
        return "name: '{}', description: '{}', topicid: '{}'".format(self.name, self.description, self.topicid)

def get_topic(db_file, topicid):  #Takes in a id, opens a connection, searches the db for matching entries, adds the matching results to list, converts the list to an object and returns this to the calling file. Then closes the connection.
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM topics WHERE topicid = ?;",(int(topicid),))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row == None:
        return None
    topicid, name, description = row
    topic = Topics(name, description, topicid)
    return topic

def search_topic(db_file, query): #Takes in a query, opens the connection, gets all rows, checks all rows to see if they have matching results. If they do, it adds them to a list. This list is then returned to the server and the connection terminated.
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM topics;")

    search_results = []

    for row in cur:
        topicid, name, description = row
        namelower = name.lower()
        namelower = namelower.replace('?','')
        namelower = namelower.replace('!','')
        namelower = namelower.replace('.','')
        name_ls = namelower.split()
        print (name_ls, query)
        if query in name_ls:
            topic = Topics(name, description, topicid)
            search_results.append(topic)

    for row in cur:
        topicid, name, description = row
        descriptionlower = description.lower()
        descriptionlower = descriptionlower.replace('?','')
        descriptionlower = descriptionlower.replace('!','')
        descriptionlower = descriptionlower.replace('.','')
        description_ls = descriptionlower.split()
        topicid = str(topicid)
        if query in topicid or description_ls:
            topic = Topics(name, description, topicid)
            search_results.append(topic)

    conn.commit()
    cur.close()
    conn.close()
    return search_results

def create_topic(db_file, information): #Takes in a list of information, opens a connection, creates a new row with that information + an id 1 number larger than the previous id. Saves row and closes connection.
    """Creates a new topic using information passed to the function."""
    name, description = information
    topic = Topics(name, description)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute('SELECT max(topicid) FROM topics')
    topicnumber = cur.fetchone()[0] + 1
    cur.execute("""INSERT INTO topics (topicid, name, description)
                VALUES (?,?,?);""",(topicnumber, name, description))
    conn.commit()
    cur.close()
    conn.close()
    return topic
