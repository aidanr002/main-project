# The Server
from tornado.ncss import Server, ncssbook_log # ncssbook_log --> Optional | The logs will be more legible and easyer to follow / understand
from templating import render
from database.customer import *
from database.comments import *
from database.issues import *
from database.pending_topics import *
from database.pending_comments import *

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
                break

    if populartopic2 != None:
        topicsused.append(populartopic2.topicid)
    if populartopic2 == None:
        for i in range(1,6):
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

    render (request, "index.html", {'populartopic1': populartopic1, 'populartopic2': populartopic2, 'populartopic3': populartopic3, 'populartopic4': populartopic4, 'populartopic5': populartopic5, "login": check_logged_in(request)})

def topicpage_handler(request, topicid):
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
        render (request, "topicpage.html", {'typecomment': typecomment, 'commentyes': commentyes, 'commentno': commentno, 'topic':topic, "login": check_logged_in(request)})

def topicpagel_handler(request, topicid):
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

def comment_creator_handler(request, topicid):
    anonymous = request.get_field('anonymous')
    if anonymous:
        user_id = 2
        user = get_user('./database/users.db', user_id)
    else:
        user_id = request.get_secure_cookie('user_id')
        user = get_user('./database/users.db', user_id.decode("UTF-8"))
    field = []
    field.append(topicid)
    field.append(user.username)
    field.append(user.country)
    stance = request.get_field('stance')
    comment = request.get_field('comment')
    field.append(stance)
    field.append(comment)
    create_newpending_comment('./database/pending-comments.db', field)
    request.redirect("/topicl/"+ topicid + "/")

def searchpage_handler (request):
    render (request, "searchpage.html", {"login": check_logged_in(request)})

def searchresult_handler (request, query):
    search_result = search_topic('./database/topics.db', query)
    if not search_result:
        render (request, "searchresultnone.html", {"login": check_logged_in(request)})
    else:
        render (request, "searchresults.html", {'topics': search_result, "login": check_logged_in(request)})

def profile_handler (request, user_page_id):
    user_page_id = int(user_page_id)
    user_id = request.get_secure_cookie('user_id')
    if user_id:
        user = get_user('./database/users.db', user_id.decode("UTF-8"))
        username = user.username
        user_id = int(user.id)
        comments = get_comment_fromusername('./database/comments.db', username)
        if comments:
            commentsyes = "yes"
            for comment in comments:
                tempcommentname = comment.topicid
                tempcommentname = get_topic('./database/topics.db', tempcommentname)
                comment.topicid = tempcommentname.name
                comment.stance = comment.stance.capitalize()
        else:
            commentsyes = ""
        if user_page_id == user_id:
            if user == None:
                render(request, "pagenotfound.html", {"login": check_logged_in(request)})
            else:
                render (request, "profilepage.html", {'commentsyes': commentsyes, 'user': user, "login": check_logged_in(request), "comments": comments})
        else:
            render(request, "pagenotfound.html", {"login": check_logged_in(request)})
    else:
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})

def remove_comment_handler(request, commentid):
    remove_comment('./database/comments.db', commentid)
    user_id = request.get_secure_cookie('user_id')
    if user_id:
        request.redirect('/user/' + (user_id.decode("UTF-8")) + '/')

def login_handler(request):
    render(request, "login.html", {"error": "", "login": check_logged_in(request)})

def post_login_handler(request):
    user = get_user_by_username('./database/users.db', request.get_field('username'))
    if user:
        if user.password == request.get_field('password'):
            request.set_secure_cookie('user_id', str(user.id))
            request.redirect("/")
        else:
            render(request, "login.html", {"error":"Incorrect password", "login": check_logged_in(request)})
    else:
        render(request, "login.html", {"error":"Incorrect username", "login": check_logged_in(request)})

def check_logged_in(request):
    user_id = request.get_secure_cookie('user_id')
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
def suggestatopic(request):
    render(request, 'suggestatopic.html',{"error": errormessage, "login": check_logged_in(request)})

def suggestatopicform(request):
    topic_fields = ['name', 'description']
    field = []
    for f in topic_fields:
        field.append(request.get_field(f))

    topic = create_newpending_topic('./database/pending-topics.db', field)
    request.redirect('/')

def remove_profile_handler (request, userid):
    remove_user('./database/users.db', userid)
    request.redirect('/')

def update_profile_handler(request, userid):
    render(request, 'updateprofile.html',{"error": errormessage, "login": check_logged_in(request)})

def update_profile_form(request, userid):
    fieldstoupdate = ['fname', 'lname', 'email', 'country', 'bio', 'username', 'password']
    newfieldinfo = []
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
            for f in fieldstoupdate:
                newfieldinfo.append(request.get_field(f))
            user = update_profile('./database/users.db', fieldstoupdate, newfieldinfo, userid)
            request.redirect('/user/' + userid + '/')

def approval_handler(request):
    user_id = request.get_secure_cookie('user_id')
    if user_id:
        user_id = user_id.decode("UTF-8")
        if int(user_id) == int(1):
            pendingcomments = get_allnewpending_comment('./database/pending-comments.db')
            pendingtopics = get_allnewpending_topics('./database/pending-topics.db')
            render(request, 'approval.html', {'pendingtopics': pendingtopics, 'pendingcomments': pendingcomments, "login": check_logged_in(request)})
    else:
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})

def approve_comment_handler(request, pendingcommentid):
    user_id = request.get_secure_cookie('user_id')
    if user_id:
        if int(user_id.decode("UTF-8")) == 1:
            information = get_newpending_comment('./database/pending-comments.db', pendingcommentid)
            if information:
                create_comment('./database/comments.db', information[1:])
                remove_newpending_comment('./database/pending-comments.db', pendingcommentid)
                request.redirect('/approve/')
        else:
            render(request, "pagenotfound.html", {"login": check_logged_in(request)})

def deny_comment_handler(request, pendingcommentid):
    user_id = request.get_secure_cookie('user_id')
    if user_id:
        if int(user_id.decode("UTF-8")) == 1:
            remove_newpending_comment('./database/pending-comments.db', pendingcommentid)
            request.redirect('/approve/')
    else:
        render(request, "pagenotfound.html", {"login": check_logged_in(request)})

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
