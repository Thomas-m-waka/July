# middleware.py
from datetime import timedelta
from django.utils import timezone

class SessionTimeoutMiddleware:
    def process_template_response(self, request, response):
        # Calculate the remaining time of the session in seconds
        session_duration = request.session.get_expiry_age()
        remaining_seconds = max(session_duration - (timezone.now() - request.session.get_expiry_date()).seconds, 0)

        # Add SESSION_EXPIRE_SECONDS to the template context
        response.context_data['SESSION_EXPIRE_SECONDS'] = remaining_seconds
        return response
