from .models import (
    PricePaid,
    PlanningApplications,
    FinanceBorrowing,
    FinanceInvestment,
    QuarterlyRevenue
)

from rest_framework import serializers


class PricePaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePaid
        fields = [
            'postcode', 'property_type', 'locality', 'district',
            'category', 'price', 'date_of_transfer'
        ]


class PlanningApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningApplications
        fields = '__all__'


class FinanceInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceInvestment
        fields = [
            'local_government_finance_code', 'local_authority_name',
            'bank_deposits_thousands', 'loans_local_government_thousands',
            'class_of_authority', 'ons_code', 'sheet_name'
        ]


class FinanceBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceBorrowing
        fields = [
            'local_government_finance_code', 'local_authority_name',
            'loans_short_term_banks_in_uk_thousands',
            'loans_longerterm_banks_in_uk_thousands',
            'short_term_loans_local_authorities_thousands',
            'longer_term_loans_local_authorities_thousands',
            'class_of_authority', 'ons_code', 'sheet_name'
        ]


class QuarterlyRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterlyRevenue
        fields = '__all__'
