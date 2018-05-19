from comments import * #Opens a command line window and prompts and recieves input for each of the required fields. It then parses these to the create comment function. The purpose of this to allow the creation of comments without using the webform. Also useful for stress testing.
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
