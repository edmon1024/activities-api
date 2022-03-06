from rest_framework import routers

from activities.views import (
    PropertyViewSet,
    ActivityViewSet,
    SurveyViewSet,
)


router = routers.SimpleRouter()
router.register(r'property', PropertyViewSet)
router.register(r'activity', ActivityViewSet)
router.register(r'survey', SurveyViewSet)

urlpatterns = router.urls

