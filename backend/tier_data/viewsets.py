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
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

    @action(detail=False, methods=['get'], url_path='ons_code_lookup')
    def ons_code_lookup(self, request):
        request_ons_code = request.query_params.get('ons_code')
        if not request_ons_code:
            return Response({'error': 'ons_code is missing'}, status=400)
        queryset = self.get_queryset().filter(ons_code=request_ons_code)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FinanceInvestmentViewSet(viewsets.GenericViewSet,
                               mixins.ListModelMixin,
                               mixins.RetrieveModelMixin):
    queryset = FinanceInvestment.objects.all()
    serializer_class = FinanceInvestmentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='ons_code_lookup')
    def ons_code_lookup(self, request):
        request_ons_code = request.query_params.get('ons_code')
        if not request_ons_code:
            return Response({'error': 'ons_code is missing'}, status=400)
        queryset = self.get_queryset().filter(ons_code=request_ons_code)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class QuarterlyRevenueViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin):
    queryset = QuarterlyRevenue.objects.all()
    serializer_class = QuarterlyRevenueSerializer
