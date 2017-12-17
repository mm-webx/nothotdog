from django.conf.urls import include, url
from rest_framework import routers

from api.views import PictureViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'pictures', PictureViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
