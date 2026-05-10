from django.urls import path

from .views import admin_portal_logout


urlpatterns = [
    path("", admin_portal_logout, name="admin_logout_direct"),
]
