# The Server - the heart of the website
from tornado.ncss import Server, ncssbook_log # ncssbook_log --> Optional | The logs will be more legible and easyer to follow / understand
from templating import render #Imports the templating engine from the templating file - allows the dynamic content and renders the pages
from database.customer import * #Imports the database control file (customers.py) that allows access to the database
from database.comments import * #Imports the database file (comments.py) that accesses the stored approved comments
from database.issues import * #Imports the control file for the topic database that stores the approved topics
from database.pending_topics import * #Imports the control file for the datatbase that stores pending comments
from database.pending_comments import * #Imports the control file for the database that stores pending comments

def index_handler (request): #The handler that controls the index page (home page)
    populartopic = get_popular_topic('./database/comments.db', './database/topics.db') #Gets the popular topic id - function from issues.py (gets the 5 topics with the most comments if any meets that criteria)
    topicsused = [] #Sets a list for the topics used
    populartopic1_id, populartopic2_id, populartopic3_id, populartopic4_id, populartopic5_id = populartopic #Converts the list/order of popular topics into individual id's
    populartopic1 = get_topic('./database/topics.db', populartopic1_id) #Gets the information for each popular topic from the database using the id from above.
    populartopic2 = get_topic('./database/topics.db', populartopic2_id)
    populartopic3 = get_topic('./database/topics.db', populartopic3_id)
    populartopic4 = get_topic('./database/topics.db', populartopic4_id)
    populartopic5 = get_topic('./database/topics.db', populartopic5_id)

    if populartopic1 != None: #Checks if there is a topic associated to populartopic1
        topicsused.append(populartopic1.topicid) #if there is, it adds the id to the list of topics used.
    if populartopic1 == None: #Checks if there isn't a topic in the variable
        for i in range(1,6): #for each number between 1-6 (5 numbers)
            if i not in topicsused: #if it isn't in the list of topics used, the program assigns it the value being iterated
                populartopic1 = get_topic('./database/topics.db', i) #Gets the topic information from the id
                topicsused.append(i) #Adds id to the list of topics used
                break #Breaks the for loop

    if populartopic2 != None: #Same as above (also as below)
        topicsused.append(populartopic2.topicid)
    if populartopic2 == None:
        for i in range(1,6): #For loop serves to check for a topic not in the topics used list. There are 5 popular topics so in the event that none have more comments, it will put the topics with ids 1-5 in the popular topic variables.
            if i not in topicsused:
                populartopic2 = get_topic('./database/topics.db', i)
                topicsused.append(i)
                break

    if populartopic3 != None:
        topicsused.append(populartopic3.topicid)
    if populartopic3 == None:
        for i in range(1,6):
            if i not in topicsused:
                populartopic3 = get_topic('./database/topics.db', i)
                topicsused.append(i)
                break

    if populartopic4 != None:
        topicsused.append(populartopic4.topicid)
    if populartopic4 == None:
        for i in range(1,6):
            if i not in topicsused:
                populartopic4 = get_topic('./database/topics.db', i)
                topicsused.append(i)
                break

    if populartopic5 != None:
        topicsused.append(populartopic5.topicid)
    if populartopic5 ==  None:
        for i in range(1,6):
            if i not in topicsused:
                populartopic5 = get_topic('./database/topics.db', i)
                topicsused.append(i)
                break
                    # Selects the index.html page as the page to be displayed                                                                                                                       #Checks if there is a user logged in
    render (request, "index.html", {'populartopic1': populartopic1, 'populartopic2': populartopic2, 'populartopic3': populartopic3, 'populartopic4': populartopic4, 'populartopic5': populartopic5, "login": check_logged_in(request)})
    #The line above is a render command from templating. The function breaks down the page selected and reloads it (it checks for key word sequences in the page and if they are found, it subsitutes the values above in for them.)

def topicpage_handler(request, topicid): #The handler for the topic page. Pulls a topicid from the url. Set up for the version where no comment has been submitted
    topic = get_topic('./database/topics.db',topicid) #Gets the topic using the topicid
    commentyes = get_comment('./database/comments.db', topicid, 'yes') #Gets the comments on the topic with the attribute yes
    commentno = get_comment('./database/comments.db', topicid, 'no') #Gets the comments on the topic with the attribute no
    typecomment = "" #Sets the variable to be neutral - it is a error keyword that is used on the page
    if topic == None: #If there is no topic associated with the id, it will display a page not found page.
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})
    else: #Otherwise the following crazy logic happens.
        if not commentyes:
            if not commentno: #If there are no yes comments and no no comments it sets the keyword to none (no comments: display on the page "No Comments")
                typecomment = "none"
            else: #If there are no yes comments but some no comments set the keyword to noyes (display: no comments, "No Yes comments")
                typecomment = "noyes"
        if not commentno:
            if commentyes: #If no no comments and some yes comments it will set the keyword to nono (display: No no comments, yes comments)
                typecomment = "nono"
        #Renders the page with the type of comments keyword and then all of the comments as assigned above.
        render (request, "topicpage.html", {'typecomment': typecomment, 'commentyes': commentyes, 'commentno': commentno, 'topic':topic, "login": check_logged_in(request)})

def topicpagel_handler(request, topicid): #Same as above but for when a comment has been submitted
    topic = get_topic('./database/topics.db',topicid)
    commentyes = get_comment('./database/comments.db', topicid, 'yes')
    commentno = get_comment('./database/comments.db', topicid, 'no')
    typecomment = ""
    if topic == None:
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})
    else:
        if not commentyes:
            if not commentno:
                typecomment = "none"
            else:
                typecomment = "noyes"
        if not commentno:
            if commentyes:
                typecomment = "nono"
        render (request, "topicpagel.html", {'typecomment': typecomment, 'commentyes': commentyes, 'commentno': commentno, 'topic':topic, "login": check_logged_in(request)})

def comment_creator_handler(request, topicid): #The POST handler for creating a comment. There is a field to enter a comment on the page and if submitted the info comes through here.
    anonymous = request.get_field('anonymous') #First checks if the anonymous field is selected.
    if anonymous: #If it is
        user_id = 2 #Set the user id to 2
        user = get_user('./database/users.db', user_id) #And get the user info for a preset profile (anonymous) at user id 2.
    else: #Otherwise
        user_id = request.get_secure_cookie('user_id') #Get the userid from the secure cookie set (from when the user logs in)
        user = get_user('./database/users.db', user_id.decode("UTF-8")) #And get that users information using the get_user function and the user_id from cookie (needs to be decoded from hash[a jumbled form of important user information])
    field = [] #The empty list ready for the information from the form
    field.append(topicid) #Adds the topicid to the list
    field.append(user.username) #Adds the username from the user variable (defined above) and
    field.append(user.country) #adds the users country to the list
    stance = request.get_field('stance')  #sets the stance attribute to the information inputted in the field using the get_field
    comment = request.get_field('comment')
    field.append(stance) #Appends the content of the stance variable to the field list
    field.append(comment)
    create_newpending_comment('./database/pending-comments.db', field) #Calls the function create_newpending_comment with the information
    request.redirect("/topicl/"+ topicid + "/") #Redirects the user to the topicl page (the topic page with the text saying you have left a comment)

def searchpage_handler (request): #Displays the search page (the page has a form on it)
    render (request, "searchpage.html", {"login": check_logged_in(request)})

def searchresult_handler (request, query): # the handler that deals with the results of the search query
    search_result = search_topic('./database/topics.db', query) #Calls the search function - parses it the query statement
    if not search_result: #If it doesn't match the search query
        render (request, "searchresultnone.html", {"login": check_logged_in(request)}) #renders the no search results page which has another form on it.
    else: #Otherwise
        render (request, "searchresults.html", {'topics': search_result, "login": check_logged_in(request)}) #Render the seatrch results page with the search results

def profile_handler (request, user_page_id): #Handler that displays the profile page
    user_page_id = int(user_page_id) #ensures that the user id from the page url is a number (integer)
    user_id = request.get_secure_cookie('user_id') #Gets the secure cookie of the logged in user
    if user_id: #If there is a user logged in,
        user = get_user('./database/users.db', user_id.decode("UTF-8")) #Gets the profile info of the user from their id.
        username = user.username #Gets the username from the list of profile info
        user_id = int(user.id) #ensures the user id is matching to the user profile.
        comments = get_comment_fromusername('./database/comments.db', username) #Gets all of the comments the user has created using their username
        if comments: #If there are some:
            commentsyes = "yes" #the message is set to comment yes - detirmines if the page displays comments/how.
            for comment in comments: #For each comment in the list of comments
                tempcommentname = comment.topicid #Sets the temp comment name to the topic id
                tempcommentname = get_topic('./database/topics.db', tempcommentname) #Gets the actual name of the topic
                comment.topicid = tempcommentname.name #Sets the 'topic id' equal to the temp topic id
                comment.stance = comment.stance.capitalize() #For all of the comment stances, sets the first letter to be capital.
        else: #If there aren't comments,
            commentsyes = "" #sets the message to be an empty string
        if user_page_id == user_id: #Checks if the pages user id matches the logged in user (so you can't view other peoples profiles)
            if user == None: # If the user information doesn't exist (empty), renders page no found
                render(request, "pagenotfound.html", {"login": check_logged_in(request)})
            else: #Otherwise displays the profile page with comments
                render (request, "profilepage.html", {'commentsyes': commentsyes, 'user': user, "login": check_logged_in(request), "comments": comments})
        else: #If the user id doesn't match the user logged in, renders page not found
            render(request, "pagenotfound.html", {"login": check_logged_in(request)})
    else: #If user not logged in, displays page not found.
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})

def remove_comment_handler(request, commentid): #Sets the handler for the remove comment function. Takes comment id from url.
    remove_comment('./database/comments.db', commentid) # Calls the remove comment function using the comment id
    user_id = request.get_secure_cookie('user_id') #Code redirects back to the users profile page. Gets the accurate user id from secure cookie.
    if user_id:
        request.redirect('/user/' + (user_id.decode("UTF-8")) + '/')

def login_handler(request): #Login page handler. Displays the login page with form.
    render(request, "login.html", {"error": "", "login": check_logged_in(request)})

def post_login_handler(request): #The POST method handler for the login form.
    user = get_user_by_username('./database/users.db', request.get_field('username')) #Gets the info of the username entered in the form
    if user: #If the username entered is real and is in the database
        if user.password == request.get_field('password'): #And if the password of the user (whos username matched) matches the field information
            request.set_secure_cookie('user_id', str(user.id)) #If so, it sets the secure cookie to the users id.
            request.redirect("/") #Redirects to the home page.
        else: #If the password does not match the users actual password, it renders the page again with the error incorrect password
            render(request, "login.html", {"error":"Incorrect password", "login": check_logged_in(request)})
    else:#If the username does exist, it renders the page again with the error incorrect username
        render(request, "login.html", {"error":"Incorrect username", "login": check_logged_in(request)})

def check_logged_in(request): #Checks if a user is logged in.
    user_id = request.get_secure_cookie('user_id') #Gets the user id from the secure cookie
    if user_id: #If there is a secure cookie,
        return get_user('./database/users.db', user_id.decode("UTF-8")) #it returns the users information

def logout_handler(request): #When called, sets the cookie to none - empty and redirects to the home page
    request.clear_cookie('user_id')
    request.redirect('/')

def pagenotfound_handler(request): #Renders the page not found page
    render(request, 'pagenotfound.html', {"login": check_logged_in(request)})

errormessage = "" #Ensures that error message is set to none initially.

def profile_creator_handler(request): #Renders the page that contains the signup form.
    render(request, 'createprofile.html',{"error": errormessage, "login": check_logged_in(request)})

def update_profile_form(request, userid): #Similar to create profile field - update profile fields - POST method
    fieldstoupdate = ['fname', 'lname', 'email', 'country', 'bio', 'username', 'password'] #The list of variables needed
    newfieldinfo = [] #Where the new info will be stored until parsed to profile creator in db
    password = request.get_field('password') #gets the password field
    confpass = request.get_field('passwordconf') # gets the confirm password field
    if password != confpass: #if they don't match, sets an error message and rerenders update profile page
        errormessage = "Password does not match"
        render(request, 'updateprofile.html',{"error": errormessage, "login": check_logged_in(request)})
    else: #Otherwise error message set to nothing
        errormessage = ""
    usernameinuse = get_user_by_username('./database/users.db', request.get_field('username')) #Searches and returns the results of the username in the fields.
    if usernameinuse: #If there is an entry for that username, throws error "Username Already Exists"
        errormessage = "Username already exists"
        render(request, 'updateprofile.html',{"error": errormessage, "login": check_logged_in(request)}) #Renders update profile page with error
    else:
        if confpass == password: #Otherwise if the two passwords match, for each item in the list of required fields, it gets the corresponding information from the form and adds it to the list of new information.
            for f in fieldstoupdate:
                newfieldinfo.append(request.get_field(f))
            user = update_profile('./database/users.db', fieldstoupdate, newfieldinfo, userid) #This calls the uodate function. Puts the new info into db
            request.redirect('/user/' + userid + '/') #Redirects back to the users profile.

def finished_profile_handler(request): #See the update profile above.
    profile_fields = ['fname', 'lname', 'email', 'country', 'bio', 'username', 'password']
    field = []

    password = request.get_field('password')
    confpass = request.get_field('passwordconf')
    if password != confpass:
        errormessage = "Password does not match"
        render(request, 'createprofile.html',{"error": errormessage, "login": check_logged_in(request)})
    else:
        errormessage = ""
    usernameinuse = get_user_by_username('./database/users.db', request.get_field('username'))
    if usernameinuse:
        errormessage = "Username already exists"
        render(request, 'createprofile.html',{"error": errormessage, "login": check_logged_in(request)})
    else:
        if confpass == password:
            for f in profile_fields:
                field.append(request.get_field(f))

            user = create_user('./database/users.db', field)
            request.set_secure_cookie('user_id', str(user.id))
            request.redirect('/')

def suggestatopic(request): # The handler that loads the page with the suggest topic form on it.
    render(request, 'suggestatopic.html',{"error": errormessage, "login": check_logged_in(request)}) #Renders the page with the form on it.

def suggestatopicform(request): #The handler for the suggest a topic form
    topic_fields = ['name', 'description'] #The fields required
    field = [] #Creates a place for the information to be added
    for f in topic_fields: #for each item that is required, it pulls the corresponding information from the fields of the form and adds to the list of information
        field.append(request.get_field(f))

    topic = create_newpending_topic('./database/pending-topics.db', field) #Creates a new pending comment using the information
    request.redirect('/') #Redirects to home

def remove_profile_handler (request, userid): #Handler for the remove profile function. Called by a url
    remove_user('./database/users.db', userid) #Calls the function remove user and parses the userid
    request.clear_cookie('userid') #Clears the secure cookie - removing profile and signing out
    request.redirect('/') #Returns to home

def update_profile_handler(request, userid):#The handler that displays the page with the update profile form on it.
    render(request, 'updateprofile.html',{"error": errormessage, "login": check_logged_in(request)}) #Renders the page with the form.

def approval_handler(request):
    user_id = request.get_secure_cookie('user_id')  # gets the secure cookie id of the user
    if user_id: #if there is actually information in the variable
        user_id = user_id.decode("UTF-8") #It gets decoded and compared to 1. If it is equal to 1,
        if int(user_id) == int(1):
            pendingcomments = get_allnewpending_comment('./database/pending-comments.db') #Gets all comments in db pending comments and stores them in a variavle that is parsed when rendered to the approve page.
            pendingtopics = get_allnewpending_topics('./database/pending-topics.db')
            render(request, 'approval.html', {'pendingtopics': pendingtopics, 'pendingcomments': pendingcomments, "login": check_logged_in(request)})
    else: #If not logged in as user 1, displays page not found
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})

def approve_comment_handler(request, pendingcommentid): #Takes the pending comment id in. Handler for a approve comment function
    user_id = request.get_secure_cookie('user_id') # gets the secure cookie id of the user
    if user_id: #if there is actually information in the variable
        if int(user_id.decode("UTF-8")) == 1: #It gets decoded and compared to 1. If it is equal to 1,
            information = get_newpending_comment('./database/pending-comments.db', pendingcommentid) #It gets the pendingcomments information from a function using its id.
            if information: #If there is actually informaation stored,
                create_comment('./database/comments.db', information[1:]) #It adds the comment using its information to the actually comment db (ignoring the oendingcommentid)
                remove_newpending_comment('./database/pending-comments.db', pendingcommentid) # And removes it from the pending comment db using its id.
                request.redirect('/approve/') #It redirects back to the approve page.
            else: #If not logged in as user 1, displays page not found
                render(request, "pagenotfound.html", {"login": check_logged_in(request)})
    else: #If not logged in as user 1, displays page not found
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})

def deny_comment_handler(request, pendingcommentid): #Takes the pending comment id in. Handler for a deny comment function
    user_id = request.get_secure_cookie('user_id') # gets the secure cookie id of the user
    if user_id: #if there is actually information in the variable
        if int(user_id.decode("UTF-8")) == 1: #It gets decoded and compared to 1. If it is equal to 1,
            remove_newpending_comment('./database/pending-comments.db', pendingcommentid) #Removes the pending comment from the pending comment db using its id.
            request.redirect('/approve/') #Redirects back to the approve page.
        else: #If not logged in as user 1, displays page not found
            render(request, "pagenotfound.html", {"login": check_logged_in(request)})
    else: #If not logged in as user 1, displays page not found
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})

#The below are the same as the above two functions - but just for topics
def approve_topic_handler(request, pendingtopicid):
    user_id = request.get_secure_cookie('user_id')
    if user_id:
        if int(user_id.decode("UTF-8")) == 1:
            information = get_newpending_topic('./database/pending-topics.db', pendingtopicid)
            if information:
                create_topic('./database/topics.db', information[1:])
                remove_newpending_topic('./database/pending-topics.db', pendingtopicid)
                request.redirect('/approve/')
    else:
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})

def deny_topic_handler(request, pendingtopicid):
    user_id = request.get_secure_cookie('user_id')
    if user_id:
        if int(user_id.decode("UTF-8")) == 1:
            remove_newpending_topic('./database/pending-topics.db', pendingtopicid)
            request.redirect('/approve/')
    else:
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})

#Registers all of the url's going to be used. If one of these matches, it will call the handler attached and/or the POST method handler (for forms)
# This uses regex to make matches. The (\+) section is where a variable id goes - this gets parsed to the handler as well.
server = Server() # Create a server object
server.register(r'/', index_handler)
server.register(r'/search/', searchpage_handler)
server.register(r'/searchresults/(.*)/', searchresult_handler)
server.register(r'/user/(\d+)/', profile_handler)
server.register(r'/user/deletecomment/(\d+)/', remove_comment_handler)
server.register(r'/user/updateprofile/(\d+)/', update_profile_handler, post = update_profile_form)
server.register(r'/topic/(\d+)/', topicpage_handler, post = comment_creator_handler)
server.register(r'/topicl/(\d+)/', topicpagel_handler, post = comment_creator_handler)
server.register(r'/login/', login_handler, post = post_login_handler)
server.register(r'/signup/', profile_creator_handler, post = finished_profile_handler)
server.register(r'/logout/', logout_handler)
server.register(r'/suggestatopic/', suggestatopic, post = suggestatopicform)
server.register(r'/user/removeprofile/(\d+)/', remove_profile_handler)
server.register(r'/approve/', approval_handler)
server.register(r'/approvecomment/(\d+)/', approve_comment_handler)
server.register(r'/denycomment/(\d+)/', deny_comment_handler)
server.register(r'/approvetopic/(\d+)/', approve_topic_handler)
server.register(r'/denytopic/(\d+)/', deny_topic_handler)
server.register(r'/.*', pagenotfound_handler)

server.run() # Runs Server
