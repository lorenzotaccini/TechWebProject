from django.apps import AppConfig


class MovieappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movieapp'
    def ready(self):
        import movieapp.signals
