from django import forms


class MessageForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Type your message...',
            'class': 'form-control'
        }),
        label=''
    )
