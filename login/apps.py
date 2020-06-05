from django.apps import AppConfig


class LoginConfig(AppConfig):
    name = 'login'

    def ready(self):
        from login import updater
        updater.start()
        print("Updater called")
