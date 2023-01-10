from django import urls

from social import views

urlpatterns = [
    urls.path("search/candidate/", views.FollowCandidateSearchListView.as_view()),
    urls.path("network/", views.NetworkListCreateView.as_view()),
    urls.path("network/<int:pk>/", views.NetworkRetrieveUpdateDestroyView.as_view()),
]
