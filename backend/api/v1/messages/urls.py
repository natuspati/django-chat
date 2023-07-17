from rest_framework.routers import DefaultRouter

from api.v1.messages.views import MessageViewSet

router = DefaultRouter()
router.register('', MessageViewSet)

urlpatterns = router.urls
