"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Order import views
from django.contrib.auth.models import User

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('MechCall/', views.mech_call, name='mech_call'),
    path('dashboard/', views.mechanic_dashboard, name='mechanic_dashboard'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('accept-order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('check-status/', views.check_status, name='check_status'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not User.objects.filter(username='admin_boss').exists():
    User.objects.create_superuser('admin_boss', 'admin@example.com', 'Fix12345')