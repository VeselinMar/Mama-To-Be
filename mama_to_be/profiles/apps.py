from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mama_to_be.profiles'

    def ready(self):
        import mama_to_be.profiles.signals
