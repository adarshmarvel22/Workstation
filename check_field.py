import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()
if hasattr(User, 'saved_projects'):
    print("Field 'saved_projects' exists on User model.")
else:
    print("Field 'saved_projects' DOES NOT exist on User model.")
