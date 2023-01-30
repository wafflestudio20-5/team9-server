from django import urls

from social import views

urlpatterns = [
    urls.path("search/candidate/", views.FollowCandidateSearchListView.as_view()),
    urls.path("network/follower/", views.NetworkFollowerListView.as_view()),
    urls.path("network/follower/<int:pk>/", views.NetworkFollowerUpdateView.as_view()),
    urls.path("network/followee/", views.NetworkFolloweeListCreateView.as_view()),
    urls.path("network/followee/<int:pk>/", views.NetworkFolloweeDestroyView.as_view()),
    urls.path("network/notification/", views.NetworkNotificationView.as_view()),
]
