import os
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from workstation.models import Project
from workstation.views import bookmark_project, dashboard

User = get_user_model()

def verify_bookmark():
    # Create test user
    user, created = User.objects.get_or_create(username='testuser_bookmark', email='test@example.com')
    if created:
        user.set_password('password123')
        user.save()
    
    # Create test project
    project, created = Project.objects.get_or_create(
        title='Test Bookmark Project',
        creator=user,
        description='A project to test bookmarks'
    )
    
    print(f"Testing with User: {user.username}")
    print(f"Testing with Project: {project.title}")
    
    # Ensure project is not bookmarked initially
    if project in user.saved_projects.all():
        user.saved_projects.remove(project)
    
    factory = RequestFactory()
    
    # Test Bookmark (Add)
    print("\n--- Testing Bookmark (Add) ---")
    request = factory.post(f'/projects/{project.slug}/bookmark/')
    request.user = user
    
    response = bookmark_project(request, slug=project.slug)
    data = json.loads(response.content)
    
    print(f"Response: {data}")
    
    if data['success'] and data['bookmarked']:
        print("SUCCESS: Project bookmarked via view.")
    else:
        print("FAILURE: Project not bookmarked via view.")
        
    if project in user.saved_projects.all():
        print("SUCCESS: Project found in user.saved_projects.")
    else:
        print("FAILURE: Project NOT found in user.saved_projects.")

    # Test Dashboard Context
    print("\n--- Testing Dashboard Context ---")
    request = factory.get('/dashboard/')
    request.user = user
    
    # We can't easily test the render output context directly without using the test client, 
    # but we can check the view logic if we extracted it, or just rely on the model check above 
    # and the fact that we updated the view.
    # Let's use the test client for a full integration test of the dashboard view.
    from django.test import Client
    client = Client()
    client.force_login(user)
    response = client.get('/dashboard/')
    
    if response.status_code == 200:
        print("SUCCESS: Dashboard loaded successfully.")
        if 'saved_projects' in response.context:
            saved_projects = response.context['saved_projects']
            if project in saved_projects:
                print("SUCCESS: Project found in dashboard context 'saved_projects'.")
            else:
                print("FAILURE: Project NOT found in dashboard context 'saved_projects'.")
        else:
            print("FAILURE: 'saved_projects' not in dashboard context.")
    else:
        print(f"FAILURE: Dashboard failed to load. Status code: {response.status_code}")

    # Test Unbookmark (Remove)
    print("\n--- Testing Unbookmark (Remove) ---")
    request = factory.post(f'/projects/{project.slug}/bookmark/')
    request.user = user
    
    response = bookmark_project(request, slug=project.slug)
    data = json.loads(response.content)
    
    print(f"Response: {data}")
    
    if data['success'] and not data['bookmarked']:
        print("SUCCESS: Project unbookmarked via view.")
    else:
        print("FAILURE: Project not unbookmarked via view.")
        
    if project not in user.saved_projects.all():
        print("SUCCESS: Project removed from user.saved_projects.")
    else:
        print("FAILURE: Project still in user.saved_projects.")

if __name__ == '__main__':
    verify_bookmark()
