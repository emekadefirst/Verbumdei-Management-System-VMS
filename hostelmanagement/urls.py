from django.urls import path
from .views import HostelView, RoomView, RoomDetailAPIView, RoomCountView, RoomSearchView

urlpatterns = [
    path("", HostelView.as_view(), name="hostel-list-create"),
    path("rooms/", RoomView.as_view(), name="room-list-create"),
    path("rooms-count/", RoomCountView.as_view(), name="room-count"),
    path("room - detail/<int:pk>/", RoomDetailAPIView.as_view(), name="room-detail"),
    path("room - search/", RoomSearchView.as_view(), name="room-search"),
]
