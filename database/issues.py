import sqlite3
import hashlib

class Topics (object):
# Creates object using information from database information #
    def __init__(self, name, description, topicid=None):
        self.topicid = topicid
        self.name = name
        self.description = description

    def __str__(self):
        return "name: '{}', description: '{}', topicid: '{}'".format(self.name, self.description, self.topicid)

def get_topic(db_file, topicid):
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

def search_topic(db_file, query):
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

def create_topic(db_file, information):
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
"""
Flat Earthers believe the earth is flat while Globers think it is globe-like.
"""
