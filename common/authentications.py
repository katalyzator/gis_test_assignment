from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Override SessionAuthentication
    without checking csrf token
    """

    def authenticate_header(self, request):
        return 'Session'

    def enforce_csrf(self, request):
        return
