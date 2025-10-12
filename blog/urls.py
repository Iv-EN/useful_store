from django.urls import path

from blog.views import (
    BlogPostCreateView,
    BlogPostDeleteView,
    BlogPostDetailView,
    BlogPostListView,
    BlogPostUpdateView,
)

app_name = "blog"

urlpatterns = [
    path("create/", BlogPostCreateView.as_view(), name="post_create"),
    path("", BlogPostListView.as_view(), name="post_list"),
    path("blogs/<int:pk>/", BlogPostDetailView.as_view(), name="post_detail"),
    path(
        "blogs/<int:pk>/edit/", BlogPostUpdateView.as_view(), name="post_edit"
    ),
    path(
        "blogs/<int:pk>/delete/",
        BlogPostDeleteView.as_view(),
        name="post_delete",
    ),
]
