from django.urls import include, path
from rest_framework import routers
from .viewsets import (
    PricePaidViewSet,
    PlanningApplicationsViewSet,
    FinanceBorrowingViewSet,
    FinanceInvestmentViewSet,
    QuarterlyRevenueViewSet,
)

router = routers.DefaultRouter()
router.register(r'pricepaid', PricePaidViewSet, basename='pricepaid')
router.register(r'planningapplication',
                PlanningApplicationsViewSet,
                basename='planningapplication')
router.register(r'financeborrowing',
                FinanceBorrowingViewSet,
                basename='financeborrowing')
router.register(r'financeinvestment',
                FinanceInvestmentViewSet,
                basename='financeinvestment')
router.register(r'quarterlyrevenue',
                QuarterlyRevenueViewSet,
                basename='quarterlyrevenue')

urlpatterns = [
    path('', include(router.urls)),
]
