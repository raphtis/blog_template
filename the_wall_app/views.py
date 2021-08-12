from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Comment, Message, User, UserManager
import bcrypt

# Create your views here.
def log_and_reg(request):
    if 'user_id' in request.session:
        return redirect('/wall')
    return render(request, "log_and_reg.html")

#log in
def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/index')
    return redirect('/')
#REGISTERING
def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        #hashing  the password
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        #create a  new user
        new_user = User.objects.create(
            first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed_pw)

            #create a new session 
        request.session['user_id'] = new_user.id
        return redirect ('/index')


#render the success page
def index(request): 
    if 'user_id' not in request.session: 
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user': this_user[0]
    }

    return render(request, 'index.html', context)


# log out
def logout(request):
    request.session.flush()
    return redirect('/')

def wall(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']), 
        'all_messages': Message.objects.all()
    }
    return render(request, "wall.html", context)

#POST A MESSAGE
def post_message(request):
    errors = Message.objects.validator(request.POST)
    if errors: 
        for val in errors.values():
            messages.error(request, val)
    else: 
    
        Message.objects.create(
            content = request.POST['content'], 
            creator = User.objects.get(id=request.session['user_id'])
        )
    return redirect('/wall')



#post a comment 
def post_comment(request, message_id):
    errors = Comment.objects.validator(request.POST)
    if errors: 
        for val in errors.values():
            messages.error(request, val)
    else: 
    
        Comment.objects.create(
            content = request.POST['content'], 
            creator = User.objects.get(id=request.session['user_id']), 
            message = Message.objects.get(id=message_id)
        )
    return redirect('/wall')

#Render index page
def user(request, user_id):
    context = {
        "user": User.objects.get(id=user_id)
    }
    return render(request, "user.html", context)





#like button 
def like(request, message_id):
    message = Message.objects.get(id=message_id)
    user = User.objects.get(id=request.session['user_id'])
    message.users_who_liked.add(user)
    return redirect('/wall')

#unlike button
def unlike(request, message_id):
    message = Message.objects.get(id=message_id)
    user = User.objects.get(id=request.session['user_id'])
    message.users_who_liked.remove(user)
    return redirect('/wall')
    
#EDIT MESSAGE POST
def edit_message(request, message_id):
    context = {
        "message" : Message.objects.get(id=message_id)
    }
    return render(request, "edit_message.html", context)
#UPDATING THE MESSAGE
def update(request, message_id):
    errors = Message.objects.validator(request.POST)
    if errors: 
        for val in errors.values():
            messages.error(request, val)
    else: 
        message = Message.objects.get(id=message_id)
        message.content = request.POST['content']
        message.save()
    return redirect(f"/messages/{message_id}/edit_message")

def update_user(request, user_id):
    errors = User.objects.edit_validator(request.POST, user_id)
    if errors: 
        for val in errors.values():
            messages.error(request, val)
    else: 
        user = User.objects.get(id = user_id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        password = request.POST["password"]
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user.password = hashed_pw
        user.save()
    return redirect("/index")

