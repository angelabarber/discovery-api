from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from discoveryapi.views import (
    register_user,
    login_user,
    get_current_user,
    ArtifactView,
    TraitView,
    SiteView,
    CityView,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"artifacts", ArtifactView, "artifact")
router.register(r"traits", TraitView, "trait")
router.register(r"sites", SiteView, "site")
router.register(r"cities", CityView, "city")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("admin/", admin.site.urls),
    path("current_user", get_current_user),
]
