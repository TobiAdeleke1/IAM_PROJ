from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from utils.constant import BILLING_TIER_LIMITS


class User(AbstractUser):
    BILLING_TIER = [
        ("Basic", "Basic"),
        ("Standard", "Standard"),
        ("Premium", "Premium")
    ]
    email = models.EmailField(db_index=True, unique=True)
    auth0_id = models.CharField(max_length=255, unique=True)
    billing_tier = models.CharField(max_length=15, choices=BILLING_TIER)
    stripe_customer_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class UserApiUse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_allowed = models.IntegerField(default=1000)
    monthly_used = models.IntegerField(default=0)
    last_reset = models.DateField(auto_now_add=True)

    def get_monthly_allowed(self):
        return BILLING_TIER_LIMITS.get(self.user.billing_tier, 0)

    def increment(self, count=1):
        self.reset_month()
        self.monthly_used += count
        self.save()

    def is_maxed(self):
        self.reset_month()
        allowed = self.get_monthly_allowed()
        return self.monthly_used >= allowed

    def reset_month(self):
        today = now().date()
        if (self.last_reset.month != today.month):
            self.monthly_used = 0
            self.last_reset = today
            self.save()

    def __str__(self):
        return f"User {self.user.username} allowed: {self.monthly_allowed}"
