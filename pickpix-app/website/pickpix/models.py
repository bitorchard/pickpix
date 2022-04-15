from django.db import models

class PickToken(models.Model):
    token_id = models.CharField(max_length=200)

class Pixel(models.Model):
    token = models.ForeignKey(PickToken, on_delete=models.SET_NULL)
    pixel_index = models.IntegerField(default=0, unique=True)
    color = models.CharField(max_length=7, default="#FFFFFF")
