"""
missions/urls.py
~~~~~~~~~~~~~~~~
URL patterns for the missions app.
 
Include in your project's root urls.py:
 
    path("api/", include("missions.urls")),
 
Which gives you:
    POST   /api/missions/estimate/
    POST   /api/missions/confirm/
    GET    /api/missions/available/
    POST   /api/missions/<pk>/accept/
    POST   /api/missions/<pk>/start/
    POST   /api/missions/<pk>/complete/
    GET    /api/missions/all/
    GET    /api/missions/dashboard/
"""
from django.urls import path
 
from .views import (
    AcceptMissionView,
    AllMissionsView,
    AvailableMissionsView,
    BossDashboardView,
    CompleteMissionView,
    MissionConfirmView,
    PriceEstimateView,
    StartMissionView,
)
 
app_name = "missions"
 
urlpatterns = [
    # ── Client ──────────────────────────────────────────────────────────────
    path("missions/estimate/", PriceEstimateView.as_view(), name="mission-estimate"),
    path("missions/confirm/", MissionConfirmView.as_view(), name="mission-confirm"),
 
    # ── Employee ─────────────────────────────────────────────────────────────
    path("missions/available/", AvailableMissionsView.as_view(), name="mission-available"),
    path("missions/<int:pk>/accept/", AcceptMissionView.as_view(), name="mission-accept"),
    path("missions/<int:pk>/start/", StartMissionView.as_view(), name="mission-start"),
    path("missions/<int:pk>/complete/", CompleteMissionView.as_view(), name="mission-complete"),
 
    # ── Boss ─────────────────────────────────────────────────────────────────
    path("missions/all/", AllMissionsView.as_view(), name="mission-all"),
    path("missions/dashboard/", BossDashboardView.as_view(), name="boss-dashboard"),
]
