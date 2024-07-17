from django.db import models
from django.conf import settings

class Drone(models.Model):
    CATEGORY_CHOICES = [
        ('armed', 'Armed'),
        ('unarmed', 'Unarmed'),
    ]
    
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight = models.FloatField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)


    def __str__(self):
        return f"{self.brand} {self.model}"

class Rental(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rental of {self.drone} by {self.user} from {self.start_datetime} to {self.end_datetime}"
