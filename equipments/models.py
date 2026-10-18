from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    STATUS_CHOICES = [
        ('Imported-New', 'Imported-New'),
        ('Refurbished', 'Refurbished'),
        ('Pre-Owned', 'Pre-Owned'),
        ('Remanufactured Unit', 'Remanufactured Unit'),
        
    ]

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField()
    manufacturer = models.CharField(max_length=150, blank=True, default='')
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Imported - New'
    )
    manufacture_year = models.PositiveSmallIntegerField(null=True, blank=True,validators=[MinValueValidator(1980), MaxValueValidator(2030)])
    price = models.DecimalField(max_digits=12, decimal_places=2)
    

    def __str__(self):
        return self.name

