from django import forms
from .models import Announcement


class AnnoCreateForm(forms.Form):
    class Meta:
        model = Announcement
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
