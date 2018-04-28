# The Server
from tornado.ncss import Server, ncssbook_log # ncssbook_log --> Optional | The logs will be more legible and easyer to follow / understand
from templating import render
from database.customer import *
from database.comments import *
from database.issues import *
#from database.issues import *

def index_handler (request):
    populartopic = get_popular_topic('./database/comments.db', './database/topics.db')
    topicsused = []
    populartopic1_id, populartopic2_id, populartopic3_id, populartopic4_id, populartopic5_id = populartopic
    populartopic1 = get_topic('./database/topics.db', populartopic1_id)
    populartopic2 = get_topic('./database/topics.db', populartopic2_id)
    populartopic3 = get_topic('./database/topics.db', populartopic3_id)
    populartopic4 = get_topic('./database/topics.db', populartopic4_id)
    populartopic5 = get_topic('./database/topics.db', populartopic5_id)

    if populartopic1 != None:
        topicsused.append(populartopic1.topicid)
    if populartopic1 == None:
        for i in range(1,6):
            if i not in topicsused:
                populartopic1 = get_topic('./database/topics.db', i)
                topicsused.append(i)
                print (topicsused)
                break

    if populartopic2 != None:
        topicsused.append(populartopic2.topicid)
    if populartopic2 == None:
        for i in range(1,6):
            if i not in topicsused:
                populartopic2 = get_topic('./database/topics.db', i)
                topicsused.append(i)
                print (topicsused)
                break

    if populartopic3 != None:
        topicsused.append(populartopic3.topicid)
    if populartopic3 == None:
        for i in range(1,6):
            if i not in topicsused:
                populartopic3 = get_topic('./database/topics.db', i)
                topicsused.append(i)
                print (topicsused)
                break

    if populartopic4 != None:
        topicsused.append(populartopic4.topicid)
    if populartopic4 == None:
        for i in range(1,6):
            if i not in topicsused:
                populartopic4 = get_topic('./database/topics.db', i)
                topicsused.append(i)
                print (topicsused)
                break

    if populartopic5 != None:
        topicsused.append(populartopic5.topicid)
    if populartopic5 ==  None:
        for i in range(1,6):
            if i not in topicsused:
                populartopic5 = get_topic('./database/topics.db', i)
                topicsused.append(i)
                print (topicsused)
                break

    render (request, "index.html", {'populartopic1': populartopic1, 'populartopic2': populartopic2, 'populartopic3': populartopic3, 'populartopic4': populartopic4, 'populartopic5': populartopic5, "login": check_logged_in(request)})

def topicpage_handler(request, topicid):
    topic = get_topic('./database/topics.db',topicid)
    commentyes = get_comment('./database/comments.db', topicid, 'yes')
    commentno = get_comment('./database/comments.db', topicid, 'no')
    if topic == None:
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})
    else:
        if not commentyes:
            if not commentno:
                render (request, "topicpagenocomment.html", {'topic':topic, "login": check_logged_in(request)})
            else:
                render (request, "topicpagenoyes.html", {'topic': topic, 'commentno': commentno, "login": check_logged_in(request)})
        if not commentno:
            if commentyes:
                render (request, "topicpagenono.html", {'topic': topic, 'commentyes': commentyes, "login": check_logged_in(request)})
        else:
            render (request, "topicpage.html", {'commentyes': commentyes, 'commentno': commentno, 'topic':topic, "login": check_logged_in(request)})

def searchpage_handler (request):
    render (request, "searchpage.html", {"login": check_logged_in(request)})

def searchresult_handler (request, query):
    search_result = search_topic('./database/topics.db', query)
    if search_result == None:
        render (request, "searchresultnone.html", {"login": check_logged_in(request)})
    else:
        render (request, "searchresults.html", {'topics': search_result, "login": check_logged_in(request)})

def profile_handler (request, user_id):
    user = get_user('./database/users.db', user_id)
    if user == None:
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})
    else:
        render (request, "profilepage.html", {'user': user, "login": check_logged_in(request)})

def login_handler(request):
    render(request, "login.html", {"error": "", "login": check_logged_in(request)})

def post_login_handler(request):
    user = get_user_by_username('./database/users.db', request.get_field('username'))
    if user:
        # check if password is correct
        if user.password == request.get_field('password'):
            request.set_secure_cookie('user_id', str(user.id))
            request.redirect("/")
        else:
            render(request, "login.html", {"error":"Incorrect password", "login": check_logged_in(request)})
    else:
        render(request, "login.html", {"error":"Incorrect username", "login": check_logged_in(request)})

def check_logged_in(request):
    user_id = request.get_secure_cookie('user_id')
    print(user_id)
    if user_id:
        return get_user('./database/users.db', user_id.decode("UTF-8"))

def logout_handler(request):
    request.clear_cookie('user_id')
    request.redirect('/')

def pagenotfound_handler(request):
    render(request, 'pagenotfound.html', {"login": check_logged_in(request)})
errormessage = ""
def profile_creator_handler(request):
    render(request, 'createprofile.html',{"error": errormessage, "login": check_logged_in(request)})

def finished_profile_handler(request):
    profile_fields = ['fname', 'lname', 'email', 'country', 'bio', 'username', 'password']
    field = []

    password = request.get_field('password')
    confpass = request.get_field('passwordconf')
    print (password, confpass)
    if password != confpass:
        errormessage = "Password does not match"
        request.redirect('/signup/')
    else:
        errormessage = ""

    for f in profile_fields:
        field.append(request.get_field(f))

    user = create_user('./database/users.db', field)
    request.set_secure_cookie('user_id', str(user.id))
    request.redirect('/')

server = Server() # Create a server object
server.register(r'/', index_handler)
server.register(r'/search/', searchpage_handler)
server.register(r'/searchresults/(.*)/', searchresult_handler)
server.register(r'/user/(\d+)/', profile_handler)
server.register(r'/topic/(\d+)/', topicpage_handler)
server.register(r'/login/', login_handler, post = post_login_handler)
server.register(r'/signup/', profile_creator_handler, post = finished_profile_handler)
server.register(r'/logout/', logout_handler)
server.register(r'/.*', pagenotfound_handler)
server.run() # Runs Server
