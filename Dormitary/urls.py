from django.urls import path
from .views import HostelView, DormAPIView, AllDorm, DormDetail, DormCountView

urlpatterns = [
    path("", HostelView.as_view(), name="hostel-list-create"),
    path("add/", DormAPIView.as_view(), name="hostel-list-create"),
    path("room/", AllDorm.as_view(), name="All - dorm"),
    path("dorm-detail/<int:pk>/", DormDetail.as_view(), name="dorm-detail"),
    path("room/count/", DormCountView.as_view(), name="dorm-detail"),
]
