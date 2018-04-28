from issues import *
# Uses code from NCSS to generate profile !!TEMPORARY!! #
fields = []
name = input("Enter name: ")
description = input("Enter Description ")
fields.append(name)
fields.append(description)

topic = create_topic('topics.db', fields)
