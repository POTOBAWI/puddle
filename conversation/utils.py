from django.utils.timezone import now
from datetime import timedelta
#from transformers import T5Tokenizer, T5ForConditionalGeneration

def is_user_online(user):
    delta = timedelta(minutes=5)  # activité récente ≤ 5 minutes
    return now() - user.last_login < delta  




# Charger le modèle T5-small (résumé)

# mon_app/utils/traducteur.py





# puddle/conversation/utils/traducteur.py

from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

class TraducteurAgent:
    def __init__(self, modele="mistral"):
        self.llm = OllamaLLM(model=modele)
        self.prompt = PromptTemplate(
            input_variables=["texte"],
            template="""
Tu es professionnel pour résumer des textes . resume le texte que tu reçois en restant fidèle au sens original.et la langue:

Texte : "{texte}"
            """
        )
        # Nouvelle syntaxe : pipeline avec le pipe |
        self.chaine = self.prompt | self.llm

    def traduire(self, texte):
        return self.chaine.invoke({"texte": texte})

