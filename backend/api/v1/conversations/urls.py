from rest_framework import routers

from api.v1.conversations.views import ConversationViewSet

router = routers.DefaultRouter()
router.register('', ConversationViewSet)

urlpatterns = router.urls
