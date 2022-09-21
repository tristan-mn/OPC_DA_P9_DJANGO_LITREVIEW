from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# on utilise AbstractUser pour créer un utilisateur personnalisé
class User(AbstractUser):
    USER = "USER"
    follows = models.ManyToManyField(
        'self',
        verbose_name='suit',
        symmetrical=False
    )