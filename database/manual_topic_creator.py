from issues import * #Opens a command line window and prompts and recieves input for each of the required fields. It then parses these to the create topic function. The purpose of this to allow the creation of topics without using the webform. Also useful for stress testing.
user = input("Stress test, super stress test or normal entry ")
if user == "super stress test": #Allows a stress test or creating 10000 topics
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
