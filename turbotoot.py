from social_core.backends.oauth import BaseOAuth2
from misago.users.models import Rank

class TurboTootOAuth2(BaseOAuth2):
    """Turbo Toot OAuth authentication backend"""
    name = 'turbotoot'
    AUTHORIZATION_URL = 'https://toot.turbo.chat/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://toot.turbo.chat/oauth/token'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('bot', 'bot'),
        ('locked', 'locked')
    ]
    ACCESS_TOKEN_METHOD = 'POST'

    def get_user_details(self, response):
        """Return user details from Turbo Toot account"""
        return {'username': response.get('acct'),
                'email': ''}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://toot.turbo.chat/api/v1/accounts/verify_credentials'
        auth_header = {"Authorization": "Bearer %s" % access_token}
        return self.get_json(url, headers=auth_header)

def associate_rank(strategy, details, backend, user=None, is_new=False, *args, **kwargs
):
    if user and user.requires_activation:
        user.rank = Rank.objects.get(slug="turbo-club")
        user.save()
    return {"user": user, "is_new" : is_new}
 
