from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, Item, ConversationMessage
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.db.models import Q, Count




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
        form = ConversationMessageForm(request.POST, request.FILES)
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
    conversations = Conversation.objects.filter(members=request.user).annotate(
        unread_count=Count(
            'messages',
            filter=Q(messages__is_read=False) & ~Q(messages__created_by=request.user)
        )
    ).order_by('-modified_at')

    for convo in conversations:
        last_message = convo.messages.order_by('-created_at').first()
        convo.last_message = last_message.content if last_message else ""

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
        'last_message': {convo.id: convo.last_message for convo in conversations}
    })


@login_required
def detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)

    if request.user not in conversation.members.all():
        return redirect('conversation:inbox')

    # Marquer comme lus les messages de l'autre utilisateur
    conversation.messages.filter(
        ~Q(created_by=request.user),
        is_read=False
    ).update(is_read=True)
    conversation.unread_count=0

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



from django.shortcuts import render
from .utils import TraducteurAgent

def traduire_vue(request):
    print("✅ Vue appelée")
    traduction = ""
    texte_source = ""

    if request.method == "POST":
        print("📨 POST reçu")
        texte_source = request.POST.get("texte", "")
        print(f"✏️ Texte soumis : {texte_source}")

        if texte_source:
            try:
                print("🚀 Chargement de l'agent...")
                agent = TraducteurAgent()
                print("🤖 Traduction en cours...")
                traduction = agent.traduire(texte_source)
                print("✅ Traduction terminée")
                traduction = traduction.strip()
            except Exception as e:
                print(f"❌ Erreur : {e}")
                traduction = "Erreur lors de la traduction."

    return render(request, "conversation/traduction.html", {
        "texte": texte_source,
        "traduction": traduction
    })

from transformers import pipeline

# Choisis un modèle léger
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    # Limite de tokens pour rester léger
    summary = summarizer(text, max_length=255, min_length=40, do_sample=False)
    return summary[0]['summary_text']


def summarize_view(request):
    summary = ""
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            summary = summarize_text(text)
    else:
        text = ""
    return render(request, "conversation/summarize.html", {"summary": summary})



translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

def traducteur_vue(request):
    traduction = ""
    if request.method == "POST":
        texte = request.POST.get("texte", "")
        if texte:
            resultat = translator(texte, max_length=100)
            traduction = resultat[0]['translation_text']
    return render(request, "conversation/traduction.html", {"traduction": traduction})



