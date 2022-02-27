from rest_framework import routers
from main.views import *

router = routers.DefaultRouter()

router.register('client', ClientView)
router.register('product', ProductView)
router.register('production', ProductionView)
router.register('shop', ShopView)
router.register('shopitem', ShopItemView)
router.register('cash', CashView)