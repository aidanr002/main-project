from customer import *
# Uses code from NCSS to generate profile !!TEMPORARY!! #
fields = []
fname = input("Enter First Name: ")
lname = input("Enter Last Name: ")
email = input("Enter Email: ")
country = input("Enter Country: ")
bio = input("Enter Bio: ")
username = input("Enter Username: ")
password = input("Enter Password: ")
fields.append(fname)
fields.append(lname)
fields.append(email)
fields.append(country)
fields.append(bio)
fields.append(username)
fields.append(password)
user = create_user('users.db', fields)
