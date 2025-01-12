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
    path("blog/<int:pk>/", BlogPostDetailView.as_view(), name="post_detail"),
    path(
        "blog/<int:pk>/edit/", BlogPostUpdateView.as_view(), name="post_edit"
    ),
    path(
        "blog/<int:pk>/delete/",
        BlogPostDeleteView.as_view(),
        name="post_delete",
    ),
]
