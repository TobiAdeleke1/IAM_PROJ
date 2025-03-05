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
