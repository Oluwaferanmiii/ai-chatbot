from django import forms
from .models import Message  # Make sure this import is here


class MessageForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Type your message...',
            'class': 'form-control'
        }),
        label=''
    )

    class Meta:
        model = Message
        fields = ['content']
