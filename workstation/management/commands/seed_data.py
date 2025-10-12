"""
Management command to seed the database with sample data
Place this file in: workstation/management/commands/seed_data.py
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from workstation.models import *
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create tags
        tags_data = [
            'AI', 'Climate', 'Fintech', 'Health', 'Open Source',
            'Blockchain', 'EdTech', 'SaaS', 'Mobile', 'Web',
            'Machine Learning', 'IoT', 'Cybersecurity', 'Gaming',
            'Social Impact', 'E-commerce', 'Analytics', 'Cloud'
        ]
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag_name}')

        # Create skills
        skills_data = [
            ('Python', 'Programming'),
            ('JavaScript', 'Programming'),
            ('React', 'Frontend'),
            ('Django', 'Backend'),
            ('Node.js', 'Backend'),
            ('UI/UX Design', 'Design'),
            ('Product Management', 'Business'),
            ('Marketing', 'Business'),
            ('Data Science', 'Analytics'),
            ('DevOps', 'Infrastructure'),
        ]
        skills = []
        for skill_name, category in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_name,
                defaults={'category': category}
            )
            skills.append(skill)
            if created:
                self.stdout.write(f'Created skill: {skill_name}')

        # Create users
        user_types = ['founder', 'professional', 'student', 'enthusiast']
        users = []

        for i in range(1, 11):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'user{i}@example.com',
                    password='password123',
                    first_name=f'User',
                    last_name=f'{i}',
                    user_type=random.choice(user_types),
                    bio=f'Sample bio for user {i}',
                    title=random.choice([
                        'Full Stack Developer',
                        'Product Designer',
                        'Data Scientist',
                        'Marketing Manager',
                        'Founder & CEO'
                    ]),
                    profile_completeness=random.randint(60, 100)
                )
                user.skills.add(*random.sample(skills, k=random.randint(2, 5)))
                user.interests.add(*random.sample(tags, k=random.randint(3, 6)))
                users.append(user)
                self.stdout.write(f'Created user: {username}')

        # Get all users (including existing ones)
        all_users = list(User.objects.all())

        # Create projects
        project_templates = [
            {
                'title': 'EdgeML: On-device AI toolkit',
                'description': 'Lightweight runtime and SDK to run transformers at the edge. Seeking hardware partners and open-source contributors.',
                'project_type': 'project',
                'stage': 'prototype',
                'collaboration_needed': 'contributors',
            },
            {
                'title': 'CampusShare: Student marketplace',
                'description': 'Peer-to-peer exchange for textbooks, gear, and services. Looking for React Native devs and campus ambassadors.',
                'project_type': 'project',
                'stage': 'mvp',
                'collaboration_needed': 'co-founders',
            },
            {
                'title': 'CarbonTrace: Climate impact API',
                'description': 'APIs to calculate product-level carbon footprints for e-commerce and logistics. Seeking data partners and design lead.',
                'project_type': 'venture',
                'stage': 'prototype',
                'collaboration_needed': 'investors',
            },
            {
                'title': 'HealthSync: Telemedicine Platform',
                'description': 'Connect patients with doctors remotely. HIPAA-compliant video consultations and health records management.',
                'project_type': 'venture',
                'stage': 'growth',
                'collaboration_needed': 'co-founders',
            },
            {
                'title': 'CodeLearn: Interactive Coding Education',
                'description': 'Gamified platform for learning programming. Built-in IDE, challenges, and peer collaboration.',
                'project_type': 'project',
                'stage': 'idea',
                'collaboration_needed': 'contributors',
            },
        ]

        projects = []
        for template in project_templates:
            if not Project.objects.filter(title=template['title']).exists():
                creator = random.choice(all_users)
                project = Project.objects.create(
                    creator=creator,
                    **template,
                    status='open'
                )
                project.tags.add(*random.sample(tags, k=random.randint(2, 4)))

                # Add creator as member
                ProjectMembership.objects.create(
                    user=creator,
                    project=project,
                    role='creator'
                )

                # Add random supporters
                supporters = random.sample(all_users, k=random.randint(3, 8))
                project.supporters.add(*supporters)

                # Add some members
                members = random.sample(
                    [u for u in all_users if u != creator],
                    k=random.randint(1, 3)
                )
                for member in members:
                    ProjectMembership.objects.create(
                        user=member,
                        project=project,
                        role=random.choice(['member', 'contributor'])
                    )

                projects.append(project)
                self.stdout.write(f'Created project: {project.title}')

        # Create thoughts
        thought_templates = [
            "Just launched our MVP! Excited to get feedback from the community.",
            "Looking for a technical co-founder with ML experience. DM if interested!",
            "What are the best tools for managing remote teams?",
            "Huge milestone today - we hit 1000 users! 🎉",
            "Anyone attending TechCrunch Disrupt this year?",
        ]

        for user in random.sample(all_users, k=min(5, len(all_users))):
            content = random.choice(thought_templates)
            thought = Thought.objects.create(
                user=user,
                content=content
            )
            thought.tags.add(*random.sample(tags, k=random.randint(1, 3)))
            thought.likes.add(*random.sample(all_users, k=random.randint(2, 6)))
            self.stdout.write(f'Created thought by {user.username}')

        # Create comments on projects
        for project in random.sample(projects, k=min(3, len(projects))):
            for _ in range(random.randint(2, 5)):
                user = random.choice(all_users)
                Comment.objects.create(
                    user=user,
                    project=project,
                    content=f"Great project! Looking forward to seeing how this develops."
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(f'Created {len(tags)} tags')
        self.stdout.write(f'Created {len(skills)} skills')
        self.stdout.write(f'Created {len(users)} new users')
        self.stdout.write(f'Created {len(projects)} projects')
        self.stdout.write('\nYou can login with any user1-user10 accounts using password: password123')
