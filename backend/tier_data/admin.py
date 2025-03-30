from django.contrib import admin

from .models import (
    PricePaid,
    PlanningApplications,
    FinanceBorrowing,
    FinanceInvestment,
    QuarterlyRevenue
)

admin.site.register(PricePaid)
admin.site.register(PlanningApplications)
admin.site.register(FinanceBorrowing)
admin.site.register(FinanceInvestment)
admin.site.register(QuarterlyRevenue)
