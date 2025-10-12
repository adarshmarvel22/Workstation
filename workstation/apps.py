from django.apps import AppConfig


class WorkstationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workstation'
    verbose_name = 'Workstation Hub'

    def ready(self):
        """Import signals when app is ready"""
        import workstation.signals