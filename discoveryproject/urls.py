from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from discoveryapi.views import register_user, login_user, get_current_user, ArtifactView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"artifacts", ArtifactView, "artifact")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("admin/", admin.site.urls),
    path("current_user", get_current_user),
]
