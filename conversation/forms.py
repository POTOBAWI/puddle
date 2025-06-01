from django import forms

from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model=ConversationMessage
        fields=('content','file','image')
        widgets={
            'content':forms.Textarea(attrs={
                'class':'w-full py-2 px-4 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-500 '
            }),
            'file':forms.ClearableFileInput(attrs={
                'class':'w-full py-2 px-4 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-500 '
            }),
            'image':forms.ClearableFileInput(attrs={
                'class':'w-full py-2 px-4 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-500 '
            }),
        }
        
            
       