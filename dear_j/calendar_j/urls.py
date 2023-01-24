from django import urls

from calendar_j import views

urlpatterns = [
    urls.path("schedule/", views.ScheduleListCreateView.as_view()),
    urls.path("schedule/<int:pk>/", views.ScheduleRetrieveUpdateDestroyView.as_view()),
    urls.path("schedule/<int:pk>/attendance/", views.ScheduleAttendanceUpdateView.as_view()),
    urls.path("schedule/group/<int:pk>/", views.ScheduleGroupRetrieveUpdateDestroyView.as_view()),
]
