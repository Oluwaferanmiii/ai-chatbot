from django import forms
from .models import Message


class ChatForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Type your message...',
                'style': 'width: 100%; padding: 10px; border-radius: 5px;'
            })
        }
