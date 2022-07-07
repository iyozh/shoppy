from django.apps import AppConfig


class ShowcaseConfig(AppConfig):
    label = 'showcase'
    name = 'applications.showcase'

    def ready(self):
        import applications.showcase.signals