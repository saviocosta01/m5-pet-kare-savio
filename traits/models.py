from django.db import models
from pets.models import Pet

# Create your models here.


class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)

    pet = models.ManyToManyField(Pet, related_name="traits")
