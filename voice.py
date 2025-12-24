# Importation des bibliothèques nécessaires
from selenium import webdriver  # Pour automatiser l'interaction avec le navigateur
from selenium.webdriver.chrome.service import Service  # Pour gérer le service ChromeDriver
from selenium.webdriver.common.keys import Keys  # Pour utiliser les touches du clavier
from selenium.webdriver.common.by import By  # Pour localiser les éléments HTML
import speech_recognition as sr  # Pour la reconnaissance vocale
import time  # Pour ajouter des pauses
import pyttsx3  # Pour la synthèse vocale (text-to-speech)

# Configuration du service ChromeDriver avec le chemin vers le fichier exécutable
service = Service('"C:\\Users\\HP\\Downloads\\Project of 327\\Project of 327\\HRS\HRS\\chromedriver.exe"')

# Initialisation du navigateur Chrome avec le service configuré
driver = webdriver.Chrome(service=service)

# Ouvre une page web locale à l'adresse spécifiée
driver.get('http://127.0.0.1:8000/login/RentPost/')

# Initialisation du moteur de synthèse vocale
engine = pyttsx3.init()# utile pour    
voices = engine.getProperty('voices')  # Récupère la liste des voix disponibles
engine.setProperty('voice', voices[1].id)  # Sélectionne une voix (par exemple, une voix féminine)

# Initialisation du module de reconnaissance vocale
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Fonction pour convertir du texte en parole
def speak(query):
    engine.say(query)  # Convertit le texte en parole
    engine.runAndWait()  # Fait parler le moteur de synthèse vocale

# Fonction pour reconnaître la parole et la convertir en texte
def recognize_speech():
    with microphone as source:
        audio = recognizer.listen(source, phrase_time_limit=5)  # Écoute pendant 5 secondes
    response = ""
    speak("Noted")  # Informe l'utilisateur que l'audio a été capturé
    try:
        response = recognizer.recognize_google(audio)  # Convertit l'audio en texte avec Google API
    except:
        response = "Error"  # En cas d'erreur, retourne "Error"
    return response

# Pause de 3 secondes avant de commencer
time.sleep(3)

# Salutation initiale
speak("Hello master! ")

# Boucle principale pour capturer les commandes vocales et interagir avec l'utilisateur
while True:
    # Demande à l'utilisateur de fournir des informations sur la zone
    speak("Enter your product price")
    voice = recognize_speech().lower()  # Capture et convertit la réponse en minuscules
    print(voice)  # Affiche la réponse dans la console
    
    # Demande à l'utilisateur de fournir le montant du loyer
    speak("Enter ")
    voice = recognize_speech().lower()
    print(voice)
    
    # Demande à l'utilisateur de fournir des détails sur la maison
    speak("Enter Details of your house")
    voice = recognize_speech().lower()
    print(voice)
    
    # Demande à l'utilisateur de fournir le montant du loyer (encore une fois)
    speak("Enter Rent")
    voice = recognize_speech().lower()
    print(voice)
    
    # Demande à l'utilisateur de fournir la surface en pieds carrés
    speak("Enter Squarefeet")
    voice = recognize_speech().lower()
    print(voice)
    
    # Demande à l'utilisateur de fournir son numéro de téléphone
    speak("Enter your phone number")
    voice = recognize_speech().lower()
    print(voice)
    
    # Vérifie si l'utilisateur a dit "exit" pour quitter la boucle
    if 'exit' in voice:
        speak('Goodbye Master!')  # Message de départ
        driver.quit()  # Ferme le navigateur
        break  # Quitte la boucle
    else:
        speak('Not a valid command. Please try again.')  # Message d'erreur pour les commandes non valides
    
    # Pause de 2 secondes avant de redémarrer la boucle
    time.sleep(2)
