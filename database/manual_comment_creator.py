from comments import *
# Uses code from NCSS to generate profile !!TEMPORARY!! #
fields = []
topicid = input("Enter topicid: ")
username = input("Enter username: ")
usercountry = input("Enter Country ")
stance = input("Enter stance: ")
comment = input("Enter comment: ")
fields.append(topicid)
fields.append(username)
fields.append(usercountry)
fields.append(stance)
fields.append(comment)
comments = create_comment('comments.db', fields)
