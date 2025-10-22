# workstation/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter to handle social account registration"""

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        """
        # If the user exists, connect the social account
        if sociallogin.is_existing:
            return

        # If it's a new user, we'll handle it in save_user
        pass

    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login user.
        """
        user = super().save_user(request, sociallogin, form)

        # Set default user_type if not provided
        if not user.user_type:
            # You can prompt user or set a default
            user.user_type = 'developer'  # Default value

        # Get extra data from social provider
        extra_data = sociallogin.account.extra_data

        # For Google
        if sociallogin.account.provider == 'google':
            if not user.first_name and 'given_name' in extra_data:
                user.first_name = extra_data['given_name']
            if not user.last_name and 'family_name' in extra_data:
                user.last_name = extra_data['family_name']

        # For GitHub
        elif sociallogin.account.provider == 'github':
            if not user.first_name and 'name' in extra_data:
                name_parts = extra_data['name'].split(' ', 1)
                user.first_name = name_parts[0]
                if len(name_parts) > 1:
                    user.last_name = name_parts[1]

        user.save()
        return user

    def populate_user(self, request, sociallogin, data):
        """
        Populate user information from social provider data.
        """
        user = super().populate_user(request, sociallogin, data)

        # Additional customization can be done here
        return user


# class MySocialAccountAdapter(DefaultSocialAccountAdapter):
#     """Custom adapter to handle social account registration"""
#
#     def pre_social_login(self, request, sociallogin):
#         """
#         Invoked just after a user successfully authenticates via a social provider,
#         but before the login is actually processed.
#         """
#         if sociallogin.is_existing:
#             return
#         pass
#
#     def save_user(self, request, sociallogin, form=None):
#         """
#         Saves a newly signed up social login user.
#         """
#         user = super().save_user(request, sociallogin, form)
#
#         # Don't set default user_type - let them choose
#         # This will trigger the complete_profile view
#
#         # Get extra data from social provider
#         extra_data = sociallogin.account.extra_data
#
#         # For Google
#         if sociallogin.account.provider == 'google':
#             if not user.first_name and 'given_name' in extra_data:
#                 user.first_name = extra_data['given_name']
#             if not user.last_name and 'family_name' in extra_data:
#                 user.last_name = extra_data['family_name']
#
#         # For GitHub
#         elif sociallogin.account.provider == 'github':
#             if not user.first_name and 'name' in extra_data:
#                 name_parts = extra_data['name'].split(' ', 1)
#                 user.first_name = name_parts[0]
#                 if len(name_parts) > 1:
#                     user.last_name = name_parts[1]
#
#         user.save()
#         return user
#
#     def get_login_redirect_url(self, request):
#         """
#         Redirect to complete profile if user_type is not set
#         """
#         user = request.user
#         if user.is_authenticated and not user.user_type:
#             return '/complete-profile/'
#         return super().get_login_redirect_url(request)
#
#     def populate_user(self, request, sociallogin, data):
#         """
#         Populate user information from social provider data.
#         """
#         user = super().populate_user(request, sociallogin, data)
#         return user

class MyAccountAdapter(DefaultAccountAdapter):
    """Custom adapter for regular account operations"""

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new user instance using information provided in the signup form.
        """
        user = super().save_user(request, user, form, commit=False)

        # Add any custom fields from the form
        if hasattr(form, 'cleaned_data'):
            if 'user_type' in form.cleaned_data:
                user.user_type = form.cleaned_data['user_type']
            if 'first_name' in form.cleaned_data:
                user.first_name = form.cleaned_data['first_name']
            if 'last_name' in form.cleaned_data:
                user.last_name = form.cleaned_data['last_name']

        if commit:
            user.save()

        return user