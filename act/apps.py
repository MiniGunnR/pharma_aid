from django.apps import AppConfig


class ActConfig(AppConfig):
    name = 'act'

    def ready(self):
        import act.signals.handlers
