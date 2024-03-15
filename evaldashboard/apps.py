from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    name = 'evaldashboard'

    def ready(self):
        import evaldashboard.signals