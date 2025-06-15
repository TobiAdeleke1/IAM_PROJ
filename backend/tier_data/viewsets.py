from .models import (
    PricePaid,
    PlanningApplications,
    FinanceBorrowing,
    FinanceInvestment,
    QuarterlyRevenue
)
from .serializers import (
    PricePaidSerializer,
    PlanningApplicationsSerializer,
    FinanceBorrowingSerializer,
    FinanceInvestmentSerializer,
    QuarterlyRevenueSerializer
)
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from tier_auth.permissions import HasScope


class PricePaidViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin):
    queryset = PricePaid.objects.all()
    serializer_class = PricePaidSerializer
    permission_classes = [IsAuthenticated, HasScope]

    HasScope.required_scopes = ['read:pricepaid']


class PlanningApplicationsViewSet(viewsets.GenericViewSet,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin):
    queryset = PlanningApplications.objects.all()
    serializer_class = PlanningApplicationsSerializer
    permission_classes = [IsAuthenticated]


class FinanceBorrowingViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin):

    queryset = FinanceBorrowing.objects.all()
    serializer_class = FinanceBorrowingSerializer
    permission_classes = [IsAuthenticated]


class FinanceInvestmentViewSet(viewsets.GenericViewSet,
                               mixins.ListModelMixin,
                               mixins.RetrieveModelMixin):
    queryset = FinanceInvestment.objects.all()
    serializer_class = FinanceInvestmentSerializer
    permission_classes = [IsAuthenticated]


class QuarterlyRevenueViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin):
    queryset = QuarterlyRevenue.objects.all()
    serializer_class = QuarterlyRevenueSerializer
