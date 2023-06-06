from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_username(self, request):
        # Return None to indicate that the 'username' field doesn't exist
        return None