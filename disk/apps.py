from django.apps import AppConfig


class DiskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'disk'
    
    def ready(self):
        import disk.signals