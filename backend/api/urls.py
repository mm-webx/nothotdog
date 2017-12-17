from django.conf.urls import include, url
from rest_framework import routers

from api.views import PictureViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'pictures', PictureViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
