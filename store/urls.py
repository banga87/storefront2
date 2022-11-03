from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.products_list),
    path('products/<int:id>', views.product_details)
]