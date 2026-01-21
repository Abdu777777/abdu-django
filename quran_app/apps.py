from django.apps import AppConfig

class QuranAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quran_app'

    def ready(self):
        import quran_app.models
