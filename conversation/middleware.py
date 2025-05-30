import datetime
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.user.last_activity = now()
            request.session['last_activity'] = str(request.user.last_activity)
