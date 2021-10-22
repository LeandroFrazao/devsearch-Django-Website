from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill, Message
from django import forms
from django.utils.translation import gettext as _

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email', 'username', 'password1', 'password2']
        labels = {
            'first_name':'Name'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class ProfileForm(ModelForm):
    class Meta:
        model= Profile
        #fields = '__all__'
        fields = ['name', 'email', 'username', 'location', 'bio', 'short_intro', 
        'profile_image', 'social_github','social_twitter','social_linkedin','social_youtube','social_website']
        
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
             
        errorList = list(self.errors)
        for item in errorList:
            self.fields[item].widget.attrs.update({'autofocus':''})
            break

    def clean(self):
        cleanData = self.cleaned_data
        
        fields = ["name","email","username"]
        fieldsError = [ele for ele in fields if(ele in cleanData and cleanData.get(ele) is None)]
        if(fieldsError):
            for error in fieldsError:
                self.add_error(error, error.capitalize() +" cant be blank !")   

        usernameField = cleanData.get("username")
        usernameSaved = self.instance.username
        try:
            if Profile.objects.filter(username=usernameField).exists() and usernameField !=usernameSaved : 
                self.add_error("username", "Username is being used. Try another one.")
        except:
            self.add_error("username", "An error has occurred during registration.")
                     
        return cleanData


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name','email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})