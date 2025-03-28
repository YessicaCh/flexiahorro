from rest_framework import routers
from django.urls import path, include
from .views import LevelListView, SavingsGoalViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"savings-goals", SavingsGoalViewSet, basename="savings-goal")

urlpatterns = [
    path("", include(router.urls)),  # Incluye todas las rutas del CRUD
    path("levels/", LevelListView.as_view(), name="level-list"),
]


# router = routers.DefaultRouter()
# router.register(r'ping', AppPingView, 'version')

# router.register(r'version', AppVersionView, 'version')
# router.register(r'init', AppInitDataView, 'init')
# router.register(r'faq', AppFaqView, 'faq')
# router.register(r'use-terms', AppUseTermView, 'use-terms')
# router.register(r'privacy-alert', AppPrivacyAlertView, 'privacy')
# router.register(r'open', OpenNewsView, 'open') # configuracion 
# router.register(r'breaking-alert', BreakingAlertView, 'open') # configuracion 
