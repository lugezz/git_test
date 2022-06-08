from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import *

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic','name', 'description'] #podría ser __all__

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name'] 