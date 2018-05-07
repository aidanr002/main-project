from issues import *
# Uses code from NCSS to generate profile !!TEMPORARY!! #
user = input("Stress test, super stress test or normal entry ")
if user == "super stress test":
    for i in range(10000):
        fields = ["Name" + str(i), "Description" + str(i)]
        print (fields)
        topic = create_topic('topics.db', fields)
if user == "stress test":
    for i in range(1000):
        fields = ["Name" + str(i), "Description" + str(i)]
        if i == 100 or i == 200 or i == 300 or i == 400 or i == 500 or i == 600 or i == 700 or i ==800 or i == 900:
            print ("At number " + str(i))
            user = input("Do you wish to continue? ")
            if user == 'yes':
                continue
            else:
                break
        print (fields)
        topic = create_topic('topics.db', fields)
if user == "normal entry":
    fields = []
    name = input("Enter name: ")
    description = input("Enter Description ")
    fields.append(name)
    fields.append(description)
    topic = create_topic('topics.db', fields)
