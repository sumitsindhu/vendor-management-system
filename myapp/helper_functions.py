from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
    """
    This is a ModelBacked that allows authentication
    with either a username or an email address.
    
    """
    def authenticate(self, email=None, password=None):
        # if '@' in email:
        #     kwargs = {'email': email}
        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_name):
        try:
            return get_user_model().objects.get(pk=user_name)
        except get_user_model().DoesNotExist:
            return None

