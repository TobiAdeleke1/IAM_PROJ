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

    @action(detail=False, methods=['get'], url_path='search')
    def postcode_lookup(self, request):
        request_postcode = request.query_params.get('postcode')
        if not request_postcode:
            return Response({'error': 'Postcode is missing'}, status=400)
        queryset = self.get_queryset().filter(postcode=request_postcode.upper())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PlanningApplicationsViewSet(viewsets.GenericViewSet,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin):
    queryset = PlanningApplications.objects.all()
    serializer_class = PlanningApplicationsSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='search')
    def authority_code_lookup(self, request):
        request_local_authority_code = request.query_params.get('authority_code')
        request_local_authority_name = request.query_params.get('authority_name')
        
        if not request_local_authority_code and not request_local_authority_name:
            return Response({'error': 'Authority code and Authority name is missing'}, status=400)
        
        if request_local_authority_code:
            queryset = self.get_queryset().filter(local_planning_authority_code=request_local_authority_code)  
        else:
            queryset = self.get_queryset().filter(local_planning_authority_name=request_local_authority_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class FinanceBorrowingViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin):

    queryset = FinanceBorrowing.objects.all()
    serializer_class = FinanceBorrowingSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='search')
    def ons_code_lookup(self, request):
        request_ons_code = request.query_params.get('ons_code')
        request_local_authority_name = request.query_params.get('local_authority_name')
        
        if not request_ons_code and not request_local_authority_name :
            return Response({'error': 'ons_code and local authority name is missing'}, status=400)
        
        if request_ons_code:
            queryset = self.get_queryset().filter(ons_code=request_ons_code)
        else:
            queryset = self.get_queryset().filter(local_authority_name=request_local_authority_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class FinanceInvestmentViewSet(viewsets.GenericViewSet,
                               mixins.ListModelMixin,
                               mixins.RetrieveModelMixin):
    queryset = FinanceInvestment.objects.all()
    serializer_class = FinanceInvestmentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='search')
    def ons_code_lookup(self, request):
        request_ons_code = request.query_params.get('ons_code')
        request_local_authority_name = request.query_params.get('local_authority_name')
        
        if not request_ons_code and not request_local_authority_name :
            return Response({'error': 'ons_code and local authority name is missing'}, status=400)
        
        if request_ons_code:
            queryset = self.get_queryset().filter(ons_code=request_ons_code)
        else:
            queryset = self.get_queryset().filter(local_authority_name=request_local_authority_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class QuarterlyRevenueViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin):
    queryset = QuarterlyRevenue.objects.all()
    serializer_class = QuarterlyRevenueSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='search')
    def ons_code_lookup(self, request):
        request_ons_code = request.query_params.get('ons_code')
        request_local_authority_name = request.query_params.get('local_authority_name')
        
        if not request_ons_code and not request_local_authority_name :
            return Response({'error': 'ons_code and local authority name is missing'}, status=400)
        
        if request_ons_code:
            queryset = self.get_queryset().filter(ons_code=request_ons_code)
        else:
            queryset = self.get_queryset().filter(local_authority=request_local_authority_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
