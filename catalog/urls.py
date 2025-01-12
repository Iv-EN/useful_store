from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    ContactView,
    ProductCreateView,
    ProductDetailView,
    ProductListView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="products_list"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path(
        "product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "product/create/", ProductCreateView.as_view(), name="product_create"
    ),
]
