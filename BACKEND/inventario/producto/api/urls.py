from rest_framework.routers import DefaultRouter
from producto.api.views import productoViewSet

router= DefaultRouter()
router.register('producto', productoViewSet, basename='producto')
urlpatterns = router.urls
