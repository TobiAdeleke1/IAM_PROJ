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
