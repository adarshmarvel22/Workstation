"""
Management command to seed the database with comprehensive sample data
Place this file in: workstation/management/commands/seed_data.py
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from workstation.models import *
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with comprehensive sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create tags
        tags_data = [
            'AI', 'Climate', 'Fintech', 'Health', 'Open Source',
            'Blockchain', 'EdTech', 'SaaS', 'Mobile', 'Web',
            'Machine Learning', 'IoT', 'Cybersecurity', 'Gaming',
            'Social Impact', 'E-commerce', 'Analytics', 'Cloud',
            'AR/VR', 'Robotics', 'Quantum', 'Automation', 'Agriculture',
            'Energy', 'Transportation', 'Real Estate', 'Legal Tech',
            'Food Tech', 'Media', 'Entertainment', 'Fashion', 'Sports'
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
            ('TypeScript', 'Programming'),
            ('Java', 'Programming'),
            ('C++', 'Programming'),
            ('Go', 'Programming'),
            ('Rust', 'Programming'),
            ('Swift', 'Programming'),
            ('Kotlin', 'Programming'),
            ('React', 'Frontend'),
            ('Vue.js', 'Frontend'),
            ('Angular', 'Frontend'),
            ('Next.js', 'Frontend'),
            ('Django', 'Backend'),
            ('Node.js', 'Backend'),
            ('Flask', 'Backend'),
            ('FastAPI', 'Backend'),
            ('Spring Boot', 'Backend'),
            ('Express.js', 'Backend'),
            ('UI/UX Design', 'Design'),
            ('Figma', 'Design'),
            ('Adobe XD', 'Design'),
            ('Graphic Design', 'Design'),
            ('Motion Graphics', 'Design'),
            ('Product Management', 'Business'),
            ('Marketing', 'Business'),
            ('Sales', 'Business'),
            ('Business Development', 'Business'),
            ('Strategy', 'Business'),
            ('Data Science', 'Analytics'),
            ('Machine Learning', 'Analytics'),
            ('Deep Learning', 'Analytics'),
            ('Data Engineering', 'Analytics'),
            ('Business Intelligence', 'Analytics'),
            ('DevOps', 'Infrastructure'),
            ('AWS', 'Infrastructure'),
            ('Azure', 'Infrastructure'),
            ('GCP', 'Infrastructure'),
            ('Docker', 'Infrastructure'),
            ('Kubernetes', 'Infrastructure'),
            ('Blockchain Development', 'Emerging Tech'),
            ('AR/VR Development', 'Emerging Tech'),
            ('IoT', 'Emerging Tech'),
            ('Cybersecurity', 'Security'),
            ('Penetration Testing', 'Security'),
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

        # Create users with varied profiles
        user_types = ['founder', 'professional', 'student', 'enthusiast']
        job_titles = [
            'Full Stack Developer', 'Frontend Engineer', 'Backend Engineer',
            'Product Designer', 'UX Researcher', 'UI Designer',
            'Data Scientist', 'ML Engineer', 'AI Researcher',
            'Marketing Manager', 'Growth Hacker', 'Content Strategist',
            'Founder & CEO', 'CTO', 'CPO', 'Product Manager',
            'Business Analyst', 'DevOps Engineer', 'Solutions Architect',
            'Mobile Developer', 'Game Developer', 'Blockchain Developer',
            'Cybersecurity Specialist', 'Cloud Engineer', 'QA Engineer'
        ]

        bio_templates = [
            'Passionate about building products that make a difference.',
            'Looking to collaborate on innovative tech projects.',
            'Experienced in scaling startups from 0 to 1.',
            'Love solving complex problems with simple solutions.',
            'Open source enthusiast and community builder.',
            'Helping companies leverage AI and data.',
            'Building the future, one line of code at a time.',
            'Designer who codes. Developer who designs.',
            'Always learning, always building.',
            'Making technology accessible to everyone.',
        ]

        users = []
        for i in range(1, 31):  # Create 30 users
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'user{i}@example.com',
                    password='password123',
                    first_name=f'User',
                    last_name=f'{i}',
                    user_type=random.choice(user_types),
                    bio=random.choice(bio_templates),
                    title=random.choice(job_titles),
                    profile_completeness=random.randint(50, 100)
                )
                user.skills.add(*random.sample(skills, k=random.randint(3, 8)))
                user.interests.add(*random.sample(tags, k=random.randint(4, 10)))
                users.append(user)
                self.stdout.write(f'Created user: {username}')

        # Get all users
        all_users = list(User.objects.all())

        # Create projects with varied content
        project_templates = [
            {
                'title': 'EdgeML: On-device AI toolkit',
                'description': 'Lightweight runtime and SDK to run transformers at the edge. Optimized for mobile devices with minimal battery impact. Seeking hardware partners and open-source contributors.',
                'project_type': 'project',
                'stage': 'prototype',
                'collaboration_needed': 'contributors',
            },
            {
                'title': 'CampusShare: Student marketplace',
                'description': 'Peer-to-peer exchange platform for textbooks, gear, and services. Already active on 5 campuses. Looking for React Native devs and campus ambassadors to expand nationwide.',
                'project_type': 'project',
                'stage': 'mvp',
                'collaboration_needed': 'co-founders',
            },
            {
                'title': 'CarbonTrace: Climate impact API',
                'description': 'RESTful APIs to calculate product-level carbon footprints for e-commerce and logistics companies. Integrated with major shipping carriers. Seeking data partners and design lead.',
                'project_type': 'venture',
                'stage': 'prototype',
                'collaboration_needed': 'investors',
            },
            {
                'title': 'HealthSync: Telemedicine Platform',
                'description': 'Connect patients with doctors remotely through HIPAA-compliant video consultations. Includes electronic health records management and prescription services.',
                'project_type': 'venture',
                'stage': 'growth',
                'collaboration_needed': 'co-founders',
            },
            {
                'title': 'CodeLearn: Interactive Coding Education',
                'description': 'Gamified platform for learning programming with built-in IDE, coding challenges, and peer collaboration. Supports Python, JavaScript, and Java.',
                'project_type': 'project',
                'stage': 'idea',
                'collaboration_needed': 'contributors',
            },
            {
                'title': 'FarmConnect: AgTech IoT Solution',
                'description': 'IoT sensors and analytics platform for precision agriculture. Helps farmers optimize water usage and crop yields through real-time data.',
                'project_type': 'venture',
                'stage': 'mvp',
                'collaboration_needed': 'investors',
            },
            {
                'title': 'SecureVault: Decentralized Storage',
                'description': 'Blockchain-based encrypted file storage with zero-knowledge architecture. No central authority can access your data.',
                'project_type': 'project',
                'stage': 'prototype',
                'collaboration_needed': 'contributors',
            },
            {
                'title': 'MindfulAI: Mental Health Companion',
                'description': 'AI-powered mental health support app with CBT exercises, mood tracking, and crisis intervention resources. Working with licensed therapists.',
                'project_type': 'venture',
                'stage': 'mvp',
                'collaboration_needed': 'co-founders',
            },
            {
                'title': 'QuantumSim: Quantum Computing Simulator',
                'description': 'Educational quantum circuit simulator for students and researchers. Visualize quantum algorithms without expensive hardware.',
                'project_type': 'project',
                'stage': 'prototype',
                'collaboration_needed': 'contributors',
            },
            {
                'title': 'LocalHero: Community Service Platform',
                'description': 'Connect volunteers with local nonprofits and community projects. Track volunteer hours and impact metrics.',
                'project_type': 'project',
                'stage': 'growth',
                'collaboration_needed': 'contributors',
            },
            {
                'title': 'EnergyGrid: Smart Home Automation',
                'description': 'AI-driven home energy management system. Reduce electricity bills by 30% through intelligent appliance scheduling.',
                'project_type': 'venture',
                'stage': 'idea',
                'collaboration_needed': 'co-founders',
            },
            {
                'title': 'LegalTech AI: Document Automation',
                'description': 'Automated contract generation and legal document analysis using NLP. Reduce legal costs for small businesses.',
                'project_type': 'venture',
                'stage': 'mvp',
                'collaboration_needed': 'investors',
            },
            {
                'title': 'FoodWaste Zero: Restaurant Analytics',
                'description': 'Predictive analytics platform helping restaurants reduce food waste by 40%. Uses historical data and ML to optimize inventory.',
                'project_type': 'project',
                'stage': 'prototype',
                'collaboration_needed': 'co-founders',
            },
            {
                'title': 'VRLearn: Immersive Education',
                'description': 'Virtual reality educational experiences for K-12 students. Field trips to historical sites and scientific phenomena in VR.',
                'project_type': 'venture',
                'stage': 'idea',
                'collaboration_needed': 'investors',
            },
            {
                'title': 'CodeReview AI: Automated PR Reviews',
                'description': 'AI assistant that reviews pull requests and suggests improvements. Integrates with GitHub, GitLab, and Bitbucket.',
                'project_type': 'project',
                'stage': 'growth',
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
                project.tags.add(*random.sample(tags, k=random.randint(3, 6)))

                # Add creator as member
                ProjectMembership.objects.create(
                    user=creator,
                    project=project,
                    role='creator'
                )

                # Add random supporters
                num_supporters = random.randint(5, 20)
                supporters = random.sample(all_users, k=min(num_supporters, len(all_users)))
                project.supporters.add(*supporters)

                # Add team members
                num_members = random.randint(2, 6)
                members = random.sample(
                    [u for u in all_users if u != creator],
                    k=min(num_members, len(all_users) - 1)
                )
                for member in members:
                    ProjectMembership.objects.create(
                        user=member,
                        project=project,
                        role=random.choice(['member', 'contributor', 'contributor'])
                    )

                projects.append(project)
                self.stdout.write(f'Created project: {project.title}')

        # Create thoughts with varied content
        thought_templates = [
            "Just launched our MVP! Excited to get feedback from the community. 🚀",
            "Looking for a technical co-founder with ML experience. DM if interested!",
            "What are the best tools for managing remote teams? Need recommendations.",
            "Huge milestone today - we hit 1000 users! 🎉",
            "Anyone attending TechCrunch Disrupt this year?",
            "Working on something exciting in the AI space. Can't wait to share more!",
            "The startup journey is a rollercoaster. Today was a win! 💪",
            "Seeking feedback on our new feature. Who wants early access?",
            "Just finished reading 'The Lean Startup'. Game changer!",
            "Coffee and code - perfect Saturday morning ☕",
            "Our team is growing! Looking for a senior backend engineer.",
            "Pitched to investors today. Fingers crossed! 🤞",
            "Open sourcing our internal tools next week. Stay tuned!",
            "What's your favorite productivity hack? Always looking to optimize.",
            "Celebrating 6 months since we started. So much progress!",
            "Anyone else building in the climate tech space? Let's connect!",
            "Just got accepted into an accelerator program! 🎊",
            "The best part of building a startup? The amazing people you meet.",
            "Debugging at 2 AM. The glamorous startup life 😅",
            "Product demo went amazing today. Team killed it!",
        ]

        for user in random.sample(all_users, k=min(20, len(all_users))):
            num_thoughts = random.randint(1, 3)
            for _ in range(num_thoughts):
                content = random.choice(thought_templates)
                thought = Thought.objects.create(
                    user=user,
                    content=content,
                    created_at=timezone.now() - timedelta(days=random.randint(0, 30))
                )
                thought.tags.add(*random.sample(tags, k=random.randint(1, 4)))
                num_likes = random.randint(3, 15)
                thought.likes.add(*random.sample(all_users, k=min(num_likes, len(all_users))))
                self.stdout.write(f'Created thought by {user.username}')

        # Create comments on projects
        comment_templates = [
            "This looks really promising! Would love to contribute.",
            "Great idea! Have you considered adding feature X?",
            "I've worked on something similar. Happy to share insights.",
            "Count me in! This aligns perfectly with my interests.",
            "Love the approach you're taking here. Very innovative!",
            "What's the tech stack you're using for this?",
            "This could be huge! When are you planning to launch?",
            "Impressive work! The UI looks clean and intuitive.",
            "I'd be interested in joining as a contributor.",
            "This solves a real problem. Excited to see it grow!",
        ]

        for project in projects:
            num_comments = random.randint(3, 10)
            for _ in range(num_comments):
                user = random.choice(all_users)
                Comment.objects.create(
                    user=user,
                    project=project,
                    content=random.choice(comment_templates),
                    created_at=timezone.now() - timedelta(days=random.randint(0, 20))
                )

        # Create some follow relationships
        for user in all_users:
            num_following = random.randint(3, 12)
            following = random.sample(
                [u for u in all_users if u != user],
                k=min(num_following, len(all_users) - 1)
            )
            for followed_user in following:
                user.following.add(followed_user)

        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'✓ Created {len(tags)} tags')
        self.stdout.write(f'✓ Created {len(skills)} skills')
        self.stdout.write(f'✓ Created {len(users)} new users')
        self.stdout.write(f'✓ Created {len(projects)} projects')
        self.stdout.write(f'✓ Created thoughts and comments')
        self.stdout.write(f'✓ Created follow relationships')
        self.stdout.write('\n' + '='*50)
        self.stdout.write('LOGIN CREDENTIALS:')
        self.stdout.write('='*50)
        self.stdout.write('Username: user1 to user30')
        self.stdout.write('Password: password123')
        self.stdout.write('='*50 + '\n')