from django.utils.timezone import now
from datetime import timedelta

def is_user_online(user):
    delta = timedelta(minutes=5)  # activité récente ≤ 5 minutes
    return now() - user.last_login < delta  # ou use user.last_activity si tu l'as géré
