from rest_framework import routers

from .views import (
    OrderViewSet,
    OptimizedOrderViewSet,
    OptimizedOrderViewSet2,
    OptimizedOrderViewSet3,
    OptimizedOrderViewSet4,
    OptimizedOrderViewSet5,
    OrderItemViewSet,
    OptimizedOrderItemViewSet,
    CursorOrderItemViewSet,
)

router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet)
router.register(r'optimized-orders', OptimizedOrderViewSet)
router.register(r'optimized-orders-2', OptimizedOrderViewSet2)
router.register(r'optimized-orders-3', OptimizedOrderViewSet3)
router.register(r'optimized-orders-4', OptimizedOrderViewSet4)
router.register(r'optimized-orders-5', OptimizedOrderViewSet5)
router.register(r'optimized-orders-cursor-pagination', OptimizedOrderViewSet2)
router.register(r'order-items', OrderItemViewSet)
router.register(r'optimized-order-items', OptimizedOrderItemViewSet)
router.register(r'cursor-order-items', CursorOrderItemViewSet)
urlpatterns = router.urls
