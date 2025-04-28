from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'O que está acontecendo?'
    }))

    class Meta:
        model = Tweet
        fields = ['content']
