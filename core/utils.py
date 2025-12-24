from transformers import pipeline
from django.db.models import Avg

# =============================
# Chargement paresseux (lazy)
# =============================

_translator_fr_en = None
_translator_en_fr = None
_summarizer = None


def get_translator_fr_en():
    global _translator_fr_en
    if _translator_fr_en is None:
        _translator_fr_en = pipeline(
            "translation",
            model="Helsinki-NLP/opus-mt-fr-en"
        )
    return _translator_fr_en


def get_translator_en_fr():
    global _translator_en_fr
    if _translator_en_fr is None:
        _translator_en_fr = pipeline(
            "translation",
            model="Helsinki-NLP/opus-mt-en-fr"
        )
    return _translator_en_fr


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6"
        )
    return _summarizer


# =============================
# Fonctions métier
# =============================

def summarize_text(text):
    if not text or not text.strip():
        return text

    summarizer = get_summarizer()

    max_len = min(200, max(50, len(text) // 2))
    min_len = min(50, max(10, len(text) // 4))

    try:
        summary = summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )
        return summary[0]["summary_text"]
    except Exception:
        return text


def translate(text, source_lang="fr", target_lang="fr"):
    if not text or not text.strip():
        return text

    if source_lang == "fr" and target_lang == "en":
        translator = get_translator_fr_en()
    elif source_lang == "en" and target_lang == "fr":
        translator = get_translator_en_fr()
    else:
        return text

    result = translator(text, max_length=200)
    return result[0]["translation_text"]


def moyenne_notes(vendeur):
    return vendeur.notes_recues.aggregate(
        Avg("note")
    )["note__avg"] or 0
