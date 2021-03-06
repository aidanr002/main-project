import sqlite3 #Imports the functions of other modules
import os

f = os.path.dirname(os.path.abspath(__file__))#Allows the constructor to make the files.

conn = sqlite3.connect(os.path.join(f, "./users.db")) #Opens the db/sql file and establishes a connection.
cur = conn.cursor()
cur.executescript(open('users.sql', 'rU').read()) #Inserts into the file the two inital users.
cur.execute("""INSERT INTO users (fname, lname, email, country, bio,username, password)
            VALUES (?,?,?,?,?,?,?);""",('Aidan', 'Ryan', 'aidanr@westnet.com.au', 'Australia', 'I am a human', 'aidanr002', '0907Aidan'))
cur.execute("""INSERT INTO users (fname, lname, email, country, bio,username, password)
            VALUES (?,?,?,?,?,?,?);""",('Anon', 'User', 'anonuser@webservices.com', 'The World', 'I am not a real human, I am a disguise', 'anonymous', '0907Aidan'))
conn.commit()
cur.close() #Closes the file and closes connection
conn.close()

#The following functions fo similar things for the other db files. The overall purpose of this is to ensure that the command in the .py files (lastrowid) has a last row to get an id. It is also to ensure that the get popular topics functions have at least 5 topics and there is an anonymous user and an admin user.
conn = sqlite3.connect(os.path.join(f, "./topics.db"))
cur = conn.cursor()
cur.executescript(open('topics.sql', 'rU').read())
cur.execute("""INSERT INTO topics (topicid, name, description)
            VALUES (?,?,?);""",(1, 'Is the Earth Round?', "Many believe that the Earth is flat."))
cur.execute("""INSERT INTO topics (topicid, name, description)
            VALUES (?,?,?);""",(2, 'Did America land on the moon?', "Many believe that America did not land on the moon and that the images and videos were faked."))
cur.execute("""INSERT INTO topics (topicid, name, description)
            VALUES (?,?,?);""",(3, 'Death Penalty', "Should the death penalty remain/ be reinstated or not?"))
cur.execute("""INSERT INTO topics (topicid, name, description)
            VALUES (?,?,?);""",(4, 'Should there be more gun control in the US?', "Should the US implement stricter gun laws similar to countries such as Australia or the UK?"))
cur.execute("""INSERT INTO topics (topicid, name, description)
            VALUES (?,?,?);""",(5, 'Should Vaccines be required for Kids?', "Is it reasonable to force parents to have their child vacinated, and if they don't impose penalties on those parents?"))
conn.commit()
cur.close()
conn.close()

conn = sqlite3.connect(os.path.join(f, "./comments.db"))
cur = conn.cursor()
cur.executescript(open('comments.sql', 'rU').read())
cur.execute("""INSERT INTO comments (commentid, topicid, username, usercountry, stance, comment)
                VALUES (?,?,?,?,?,?);""",( 1, 1, 'aidanr002', 'Australia', 'yes', 'I believe that it is round'))
conn.commit()
cur.close()
conn.close()

conn = sqlite3.connect(os.path.join(f, "./pending-topics.db"))
cur = conn.cursor()
cur.executescript(open('pending-topics.sql', 'rU').read())
cur.execute("""INSERT INTO pending_topics (pendingtopicid, name, description)
            VALUES (?,?,?);""",(1, 'Is the Earth Round?', "Many believe that the Earth is flat."))
cur.execute("""INSERT INTO pending_topics (pendingtopicid, name, description)
            VALUES (?,?,?);""",(2, 'Did America land on the moon?', "Many believe that America did not land on the moon and that the images and videos were faked."))
cur.execute("""INSERT INTO pending_topics (pendingtopicid, name, description)
            VALUES (?,?,?);""",(3, 'Death Penalty', "Should the death penalty remain/ be reinstated or not?"))
cur.execute("""INSERT INTO pending_topics (pendingtopicid, name, description)
            VALUES (?,?,?);""",(4, 'Should there be more gun control in the US?', "Should the US implement stricter gun laws similar to countries such as Australia or the UK?"))
cur.execute("""INSERT INTO pending_topics (pendingtopicid, name, description)
            VALUES (?,?,?);""",(5, 'Should Vaccines be required for Kids?', "Is it reasonable to force parents to have their child vacinated, and if they don't impose penalties on those parents?"))
conn.commit()
cur.close()
conn.close()

conn = sqlite3.connect(os.path.join(f, "./pending-comments.db"))
cur = conn.cursor()
cur.executescript(open('pending-comments.sql', 'rU').read())
cur.execute("""INSERT INTO pending_comments (pendingcommentid, topicid, username, usercountry, stance, comment)
                VALUES (?,?,?,?,?,?);""",( 1, 1, 'aidanr002', 'Australia', 'yes', 'I believe that it is round'))
conn.commit()
cur.close()
conn.close()
