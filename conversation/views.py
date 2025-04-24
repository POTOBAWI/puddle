from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, Item, ConversationMessage
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required

# Création d'une nouvelle conversation
@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    # Vérifie si l'utilisateur est le créateur de l'article
    if item.created_by == request.user:
        return redirect('dashboard:index')

    # Vérifie si une conversation existe déjà entre l'utilisateur et l'article
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])
    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            # Crée une nouvelle conversation
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user) #ajout du createur de la conversation
            conversation.members.add(item.created_by) # ajout du proprietaire du produit
            conversation.save()

            # Crée un message pour la conversation
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        "form": form
    })


# Boîte de réception des conversations
@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required

def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    if request.user not in conversation.members.all():
        return redirect('conversation:inbox')

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })
