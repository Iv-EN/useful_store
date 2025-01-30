from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (ContactView, ProductDeleteView, ProductDetailView,
                           ProductListView, ProductView)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="products_list"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path(
        "product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "product/create/", ProductView.as_view(), name="product_create"
    ),
    path(
        "product/<int:pk>/update/",
        ProductView.as_view(),
        name="product_update",
    ),
    path(
        "product/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
]
