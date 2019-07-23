from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'
    # a human readble application name it's display
    verbose_name = 'Image bookmarks'
    # a ready method where we import signals for this application
    def ready(self):
        # import signals handlers
        import images.signals
