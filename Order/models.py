from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    truck_model = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    file = models.FileField(upload_to='orders/', null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.truck_model}"