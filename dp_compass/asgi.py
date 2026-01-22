"""
ASGI config for DP-COMPASS project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dp_compass.settings')
application = get_asgi_application()
