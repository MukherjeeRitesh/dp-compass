"""
URL configuration for DP-COMPASS project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def reset_passwords_secret(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    users_to_reset = {
        'admin': 'admin123',
        'auditor1': 'auditor123',
        'developer1': 'developer123'
    }
    msgs = []
    for username, password in users_to_reset.items():
        try:
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
            msgs.append(f"Success: Reset password for {username}")
        except User.DoesNotExist:
            msgs.append(f"Error: User {username} does not exist.")
        except Exception as e:
            msgs.append(f"Error: {str(e)}")
    return HttpResponse("<br>".join(msgs) + "<br><br><b>Done! Please do not forget to remove this code and re-deploy once you have logged in!</b>")

urlpatterns = [
    path('reset-default-passwords-secret-12345/', reset_passwords_secret),
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('users/', include('apps.users.urls')),
    path('audits/', include('apps.audits.urls')),
    path('compliance/', include('apps.compliance.urls')),
    path('reports/', include('apps.reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
