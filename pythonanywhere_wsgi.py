import os
import sys

# Add your project directory to the sys.path
path = '/home/karim56489746532/airquiz'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_platform.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
