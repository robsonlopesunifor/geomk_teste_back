from django.db import models


class Parking(models.Model):
    plate = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    left = models.BooleanField(default=False)
    start = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=100,default="")
    