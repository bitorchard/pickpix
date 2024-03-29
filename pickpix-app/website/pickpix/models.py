from django.db import models

class GlobalConfig(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=200)

class PickToken(models.Model):
    owner = models.CharField(max_length=200)
    token_id = models.CharField(max_length=200)

class Pixel(models.Model):
    token = models.ForeignKey(PickToken, null=True, on_delete=models.SET_NULL)
    pixel_index = models.IntegerField(default=0, unique=True)
    color = models.CharField(max_length=7, default="#FFFFFF")
