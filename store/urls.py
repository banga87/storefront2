from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls

# URLConf
# urlpatterns = [
#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:pk>', views.ProductDetails.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path('collections/<int:pk>', views.CollectionDetails.as_view(), name='collection-detail')
# ]