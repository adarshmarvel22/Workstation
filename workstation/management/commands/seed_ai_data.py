# Save this file as: workstation/management/commands/seed_ai_data.py

from django.core.management.base import BaseCommand
from workstation.models import AIWorker, AITool

class Command(BaseCommand):
    help = 'Seed AI Workers and Tools data'

    def handle(self, *args, **kwargs):
        # Create AI Workers
        workers_data = [
            {
                'name': 'AI Coder',
                'worker_type': 'coder',
                'description': 'Expert in writing, debugging, and optimizing code across multiple languages',
                'icon': '💻'
            },
            {
                'name': 'AI Researcher',
                'worker_type': 'researcher',
                'description': 'Conducts deep research and analysis on any topic',
                'icon': '🔬'
            },
            {
                'name': 'AI Marketer',
                'worker_type': 'marketer',
                'description': 'Creates marketing strategies, content, and campaign ideas',
                'icon': '📈'
            },
            {
                'name': 'AI Designer',
                'worker_type': 'designer',
                'description': 'Helps with design concepts, UI/UX, and visual solutions',
                'icon': '🎨'
            },
            {
                'name': 'AI Writer',
                'worker_type': 'writer',
                'description': 'Crafts compelling content, articles, and creative writing',
                'icon': '✍️'
            },
            {
                'name': 'AI Analyst',
                'worker_type': 'analyst',
                'description': 'Analyzes data, generates insights, and creates visualizations',
                'icon': '📊'
            },
        ]

        for worker_data in workers_data:
            worker, created = AIWorker.objects.get_or_create(
                worker_type=worker_data['worker_type'],
                defaults=worker_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created worker: {worker.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Worker already exists: {worker.name}'))

        # Create AI Tools
        tools_data = [
            {
                'name': 'Code Generator',
                'description': 'Generate code snippets in any language',
                'icon': '⚙️',
                'category': 'Development',
                'order': 1
            },
            {
                'name': 'Data Analyzer',
                'description': 'Analyze and visualize data',
                'icon': '📈',
                'category': 'Analytics',
                'order': 2
            },
            {
                'name': 'Content Writer',
                'description': 'Create engaging content',
                'icon': '📝',
                'category': 'Writing',
                'order': 3
            },
            {
                'name': 'Image Generator',
                'description': 'Generate AI images from text',
                'icon': '🖼️',
                'category': 'Creative',
                'order': 4
            },
            {
                'name': 'API Tester',
                'description': 'Test and debug APIs',
                'icon': '🔌',
                'category': 'Development',
                'order': 5
            },
            {
                'name': 'SEO Optimizer',
                'description': 'Optimize content for search engines',
                'icon': '🔍',
                'category': 'Marketing',
                'order': 6
            },
            {
                'name': 'Database Query Builder',
                'description': 'Build and optimize SQL queries',
                'icon': '🗄️',
                'category': 'Development',
                'order': 7
            },
            {
                'name': 'Social Media Planner',
                'description': 'Plan and schedule social media posts',
                'icon': '📱',
                'category': 'Marketing',
                'order': 8
            },
            {
                'name': 'Bug Detector',
                'description': 'Find and fix code issues',
                'icon': '🐛',
                'category': 'Development',
                'order': 9
            },
            {
                'name': 'Translation Tool',
                'description': 'Translate content to any language',
                'icon': '🌐',
                'category': 'Language',
                'order': 10
            },
        ]

        for tool_data in tools_data:
            tool, created = AITool.objects.get_or_create(
                name=tool_data['name'],
                defaults=tool_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created tool: {tool.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Tool already exists: {tool.name}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Successfully seeded AI Workers and Tools data!'))
