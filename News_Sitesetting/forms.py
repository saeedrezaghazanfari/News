from django import forms
from News_Sitesetting.models import Contact, Opinion

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'subject', 'image', 'msg']

class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ['name', 'email', 'subject', 'msg']