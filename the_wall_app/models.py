from django.db import models
import re
import bcrypt

# Create your models here.
class MessageManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['content'] = "Message content needs to be at least one character"
        return errors

class CommentManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['content'] = "Comment content needs to be at least one character"
        return errors

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be 2 characters or more."

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be 2 characters or more."

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email'])==0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"

        
        
        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email is already in use"
        

        if len(postData['password']) < 8:
            errors["password"] = "Password must be 8 characters or more."

        if postData['password'] != postData['confirm_password']:
            errors["match"] = "Passwords do not match."

        return errors

    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be 8 characters or more"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password'] = "Email and password do not match"
        
        return errors

    def edit_validator(self, postData, user_id):
        errors = {}
        users = User.objects.filter(email=postData['email'])
        if users:
            my_user = User.objects.get(id=user_id)
            if my_user.email != users[0].email:
                errors['email'] = "Email is already in use"
            else:
                if len(postData['first_name']) < 2:
                    errors["first_name"] = "First name should be 2 characters or more."

                if len(postData['last_name']) < 2:
                    errors["last_name"] = "Last name should be 2 characters or more."

                if len(postData['password']) < 8:
                    errors["password"] = "Password must be 8 characters or more."

                if postData['password'] != postData['confirm_password']:
                    errors["match"] = "Passwords do not match."
                    
        else: 
            if len(postData['first_name']) < 2:
                errors["first_name"] = "First name should be 2 characters or more."

            if len(postData['last_name']) < 2:
                errors["last_name"] = "Last name should be 2 characters or more."

            if len(postData['password']) < 8:
                errors["password"] = "Password must be 8 characters or more."

            if postData['password'] != postData['confirm_password']:
                errors["match"] = "Passwords do not match."
        return errors




class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=250)
    password = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Message(models.Model):
    content = models.TextField()
    creator = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    users_who_liked = models.ManyToManyField(User, related_name="messages_user_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class Comment(models.Model):
    content = models.TextField()
    creator = models.ForeignKey(User, related_name="comments", 
    on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE, null=True)
    users_who_liked = models.ManyToManyField(User, related_name="comments_users_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
