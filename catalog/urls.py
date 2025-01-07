from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product_create, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("product/<int:pk>/", product_detail, name="product_detail"),
    path("product/create/", product_create, name="product_create"),
]
