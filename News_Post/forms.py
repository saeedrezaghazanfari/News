from django import forms
from django.utils.translation import gettext_lazy as _
from News_Post.models import Comment


class SendCommentForm(forms.ModelForm):
    post_id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Comment
        fields = ['msg']
        labels = {'msg': _('')}

class SendReplyForm(forms.Form):
    rpl = forms.CharField(
        widget=forms.Textarea(
            attrs={'class':'form-control form-control-home-media p-4', 'rows':'2', 'placeholder':'پاسخ خود را وارد کنید:'}
        )
    )
    post_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )