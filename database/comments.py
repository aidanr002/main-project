import sqlite3
import hashlib

class Comments(object): #Sets up constructor for object that will have attributes. This object can be used in server.py. Specific attributes can be pulled from it.
    def __init__(self, topicid, username, usercountry, stance, comment, commentid = None):
        self.username = username
        self.usercountry = usercountry
        self.topicid = topicid
        self.stance = stance
        self.comment = comment
        self.commentid = commentid

    def __str__(self): #Decodes the object so it is printable
        return "username: '{}', usercountry: '{}', topicid: '{}', stance: '{}', comment '{}', commentid: '{}'".format(self.username, self.usercountry, self.topicid, self.stance, self.comment, self.commentid)

def remove_comment(db_file, commentid): #Takes in comment id, opens a connection to db file, removes the line from the file (line at id) and closes the connection.
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM comments WHERE commentid = ?;",(commentid,))
    conn.commit()
    cur.close()
    conn.close()

def get_comment(db_file, topicid, stance): #Takes in a id, opens a connection, searches the db for matching entries, adds the matching results to list, converts the list to an object and returns this to the calling file. Then closes the connection.
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM comments WHERE topicid = ? AND stance = ?;",(topicid, stance))
    selected_comments = []
    for row in cur:
        commentid, topicid, username, usercountry, stance, comment = row
        acomment = Comments(topicid, username, usercountry, stance, comment, commentid)
        selected_comments.append(acomment)
    conn.commit()
    cur.close()
    conn.close()
    return selected_comments

def get_comment_fromusername(db_file, username):  #Takes in a users username, opens a connection, searches the db for matching entries, adds the matching results to list, converts the list to an object and returns this to the calling file. Then closes the connection.
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM comments WHERE username = ?;",(username,))
    selected_comments = []
    for row in cur:
        commentid, topicid, username, usercountry, stance, comment = row
        acomment = Comments(topicid, username, usercountry, stance, comment, commentid)
        selected_comments.append(acomment)
    conn.commit()
    cur.close()
    conn.close()
    return selected_comments

def create_comment(db_file, information): #Takes in a list of information, opens a connection, creates a new row with that information + an id 1 number larger than the previous id. Saves row and closes connection.
    """Creates a new comment using information passed to the function."""
    topicid, username, usercountry, stance, comment = information
    comments = Comments(topicid, username, usercountry, stance, comment)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("""INSERT INTO comments (topicid, username, usercountry, stance, comment)
                VALUES (?,?,?,?,?);""",(int(topicid), str(username), str(usercountry), str(stance), str(comment)))
    comments.commentid = cur.lastrowid
    print ("here")
    conn.commit()
    cur.close()
    conn.close()
    return comment

def get_popular_topic(db_file, topic_file):
    # Get the last topic id
    conn = sqlite3.connect(topic_file)
    cur = conn.cursor()
    cur.execute('SELECT max(topicid) FROM topics')
    numbertopics = cur.fetchone()[0]
    cur.close()
    conn.close()
    # Uses a topic id to find out which post has the most Comments
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    topiccount = 1
    commentcount = 0
    populartopic1_id = 0
    populartopic1_commentnumber = 0
    populartopic2_id = 0
    populartopic2_commentnumber = 0
    populartopic3_id = 0
    populartopic3_commentnumber = 0
    populartopic4_id = 0
    populartopic4_commentnumber = 0
    populartopic5_id = 0
    populartopic5_commentnumber = 0

    for i in range(numbertopics):
        commentcount = 0
        cur.execute("SELECT * FROM comments WHERE topicid  = ?;",(int(topiccount),))
        for comment in cur:
            commentcount += 1
        if commentcount > populartopic1_commentnumber:
            populartopic5_id = populartopic4_id
            populartopic5_commentnumber = populartopic4_commentnumber
            populartopic4_id = populartopic3_id
            populartopic4_commentnumber = populartopic3_commentnumber
            populartopic3_id = populartopic2_id
            populartopic3_commentnumber = populartopic2_commentnumber
            populartopic2_id = populartopic1_id
            populartopic2_commentnumber = populartopic1_commentnumber
            populartopic1_id = topiccount
            populartopic1_commentnumber = commentcount

        elif commentcount > populartopic2_commentnumber:
            populartopic5_id = populartopic4_id
            populartopic5_commentnumber = populartopic4_commentnumber
            populartopic4_id = populartopic3_id
            populartopic4_commentnumber = populartopic3_commentnumber
            populartopic3_id = populartopic2_id
            populartopic3_commentnumber = populartopic2_commentnumber
            populartopic2_id = topiccount
            populartopic2_commentnumber = commentcount

        elif commentcount > populartopic3_commentnumber:
            populartopic5_id = populartopic4_id
            populartopic5_commentnumber = populartopic4_commentnumber
            populartopic4_id = populartopic3_id
            populartopic4_commentnumber = populartopic3_commentnumber
            populartopic3_id = topiccount
            populartopic3_commentnumber = commentcount

        elif commentcount > populartopic4_commentnumber:
            populartopic5_id = populartopic4_id
            populartopic5_commentnumber = populartopic4_commentnumber
            populartopic4_id = topiccount
            populartopic4_commentnumber = commentcount

        elif commentcount > populartopic5_commentnumber:
            populartopic5_id = topiccount
            populartopic5_commentnumber = commentcount

        topiccount += 1
    return (populartopic1_id, populartopic2_id, populartopic3_id, populartopic4_id, populartopic5_id)
