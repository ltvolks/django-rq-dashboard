"""
admin_static templatetag compatibility shim for django 1.3
"""
import django
from django.conf import settings
from django import template

register = template.Library()

if django.VERSION[1] < 4:
    if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
        from django.core.files.storage import get_storage_class
        from django.utils.functional import LazyObject

        class ConfiguredStorage(LazyObject):
            def _setup(self):
                self._wrapped = get_storage_class(settings.STATICFILES_STORAGE)()
        staticfiles_storage = ConfiguredStorage()

        @register.simple_tag
        def static(path):
            """
            A template tag that returns the URL to a file
            using staticfiles' storage backend
            """
            return staticfiles_storage.url(path)
    else:
        from urlparse import urljoin
        from django.templatetags.static import PrefixNode

        @register.simple_tag
        def static(path):
            """
            Joins the given path with the STATIC_URL setting.
            """
            return urljoin(PrefixNode.handle_simple("STATIC_URL"), path)
else:
    from django.contrib.admin.templatetags.admin_static import static
    register.simple_tag(static)
