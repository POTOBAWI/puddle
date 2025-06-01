

from django.db import models
from item.models import Item
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
    item=models.ForeignKey(Item,related_name='conversations',on_delete=models.CASCADE)
    members=models.ManyToManyField(User,related_name='conversations')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-modified_at',)

class ConversationMessage(models.Model):
    conversation=models.ForeignKey(Conversation,related_name="messages",on_delete=models.CASCADE)
    content=models.TextField(blank=True, null=True) 
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,related_name='created_message',on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    file = models.FileField(upload_to='messages/files/', blank=True, null=True)
    image = models.ImageField(upload_to='messages/images/', blank=True, null=True)
    class Meta:
        ordering = ('created_at',)