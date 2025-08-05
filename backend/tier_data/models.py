from django.db import models


class PricePaid(models.Model):
    PROPERTY_TYPES = [
        ("D", "Detached"),
        ("S", "Semi-Detached"),
        ("T", "Terraced"),
        ("F", "Flats/Maisonettes"),
        ("O", "Other"),
    ]

    CATEGORIES = [
        ("A", "Standard Price Paid entry"),
        ("B", "Additional Price Paid entry"),
    ]
    price = models.FloatField(blank=False)
    date_of_transfer = models.DateTimeField()
    postcode = models.CharField(max_length=12)
    property_type = models.CharField(max_length=25, choices=PROPERTY_TYPES)
    locality = models.CharField(max_length=128)
    town_or_city = models.CharField(max_length=128)
    district = models.CharField(max_length=128)
    county = models.CharField(max_length=128)
    category = models.CharField(max_length=128, choices=CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["postcode"]
        indexes = [
            models.Index(fields=["postcode"])
        ]

    def __str__(self):
        return f"[Price Paid at {self.postcode}, {self.town_or_city}]"


class PlanningApplications(models.Model):
    region = models.CharField(max_length=128)
    local_planning_authority_name = models.CharField(max_length=128)
    local_planning_authority_code = models.CharField(max_length=128)
    quarter = models.CharField(max_length=20)
    fiscal_year = models.CharField(max_length=20)
    total_decisions_grand_total_all = models.IntegerField()
    total_granted_grand_total_all = models.IntegerField()
    total_refused_grand_total_all = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["local_planning_authority_name"]
        indexes = [
            models.Index(fields=["local_planning_authority_name"])
        ]

    def __str__(self):
        return (f"[Planning Applications at"
                f"{self.local_planning_authority_name}, {self.quarter}]")


class FinanceInvestment(models.Model):
    local_government_finance_code = models.CharField(max_length=128)
    local_authority_name = models.CharField(max_length=128)
    bank_deposits_thousands = models.FloatField(blank=True)
    building_societies_deposits_thousands = models.FloatField(blank=True)
    treasury_bills_thousands = models.FloatField(blank=True)
    banks_cert_of_deposit_thousands = models.FloatField(blank=True)
    building_societies_cert_of_deposit_thousands = models.FloatField(blank=True)
    british_government_securities_thousands = models.FloatField(blank=True)
    other_financial_intermediaries_thousands = models.FloatField(blank=True)
    public_corporations_thousands = models.FloatField(blank=True)
    debt_management_account_deposit_facility_thousands = models.FloatField(blank=True)
    money_market_funds_thousands = models.FloatField(blank=True)
    externally_managed_funds_thousands = models.FloatField(blank=True)
    other_investments_thousands = models.FloatField(blank=True)
    loans_local_government_thousands = models.FloatField(blank=True)
    country = models.CharField(max_length=128)
    class_of_authority = models.CharField(max_length=128)
    ons_code = models.CharField(max_length=128)
    sheet_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"[Finance Investment at"
                f"{self.local_authority_name}, {self.bank_deposits_thousands}]")


class FinanceBorrowing(models.Model):
    local_government_finance_code = models.CharField(max_length=128)
    local_authority_name = models.CharField(max_length=128)
    loans_short_term_banks_in_uk_thousands = models.FloatField(blank=True)
    loans_short_term_building_societies_thousands = models.FloatField(blank=True)
    loans_short_term_other_financial_intermediaries_thousands = models.FloatField(blank=True)
    loans_short_term_public_corporations_thousands = models.FloatField(blank=True)
    loans_short_term_private_nonfinancial_corporations_thousands = models.FloatField(blank=True)
    loans_short_term_central_government_thousands = models.FloatField(blank=True)
    loans_short_term_households_sector_thousands = models.FloatField(blank=True)
    loans_short_term_other_sources_thousands = models.FloatField(blank=True)
    securities_negotiable_bonds_commercial_thousands = models.FloatField(blank=True)
    securities_other_stock_issues_thousands = models.FloatField(blank=True)
    loans_longerterm_pwlb_thousands = models.FloatField(blank=True)
    loans_longerterm_banks_in_uk_thousands = models.FloatField(blank=True)
    loans_longerterm_building_societies_thousands = models.FloatField(blank=True)
    loans_longerterm_other_financial_intermediaries_thousands = models.FloatField(blank=True)
    loans_longerterm_public_corporations_thousands = models.FloatField(blank=True)
    loans_longerterm_private_nonfinancial_corporations_thousands = models.FloatField(blank=True)
    loans_longerterm_central_government_thousands = models.FloatField(blank=True)
    loans_longerterm_households_sector_thousands = models.FloatField(blank=True)
    loans_longerterm_other_sources_thousands = models.FloatField(blank=True)
    short_term_loans_local_authorities_thousands = models.FloatField(blank=True)
    longer_term_loans_local_authorities_thousands = models.FloatField(blank=True)
    country = models.CharField(max_length=128)
    class_of_authority = models.CharField(max_length=128)
    ons_code = models.CharField(max_length=128)
    sheet_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"[Finance Borrowing at"
                f"{self.local_authority_name}, {self.class_of_authority}]")


class QuarterlyRevenue(models.Model):
    e_code = models.CharField(max_length=50)
    ons_code = models.CharField(max_length=50)
    local_authority = models.CharField(max_length=128)
    region = models.CharField(max_length=128)
    class_of_authority = models.CharField(max_length=128)
    public_order_and_safety_total = models.FloatField(blank=True)
    economic_affairs_total = models.FloatField(blank=True)
    housing_and_community_amenities_total = models.FloatField(blank=True)
    health_total = models.FloatField(blank=True)
    education_total = models.FloatField(blank=True)
    social_protection_total = models.FloatField(blank=True)
    net_current_expenditure_including_education_non_pay_element = models.FloatField(blank=True)
    total_service_expenditure_including_education_non_pay_element = models.FloatField(blank=True)
    housing_revenue_account_income_total = models.FloatField(blank=True)
    housing_revenue_account_expenditure_total = models.FloatField(blank=True)
    sheet_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"[Quarterly Revenue at"
                f"{self.local_authority}, {self.region}]")
