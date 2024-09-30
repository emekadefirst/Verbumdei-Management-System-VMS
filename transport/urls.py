from django.urls import path
from .views import BusView, BusCount, BusDetailView, CommuteView, CommuteDetailView

urlpatterns = [
    path("buses/", BusView.as_view(), name="bus-list"),
    path("buses/count/", BusCount.as_view(), name="bus-count"),
    path("buses/<int:pk>/", BusDetailView.as_view(), name="bus-detail"),
    path("commutes/", CommuteView.as_view(), name="commute-list"),
    path("commutes/<int:pk>/", CommuteDetailView.as_view(), name="commute-detail"),
]
