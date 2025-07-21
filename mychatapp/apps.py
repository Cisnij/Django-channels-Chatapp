from django.apps import AppConfig


class MychatappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mychatapp'

    #Setting signals
    def ready(self):
        import mychatapp.signals

