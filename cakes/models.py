from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cake(models.Model):
    cake_name=models.CharField(max_length=150)
    cake_weight=models.PositiveIntegerField()
    cake_price=models.PositiveIntegerField()
    cake_image=models.ImageField(upload_to="images")

    def __str__(self) -> str:
        return self.cake_name