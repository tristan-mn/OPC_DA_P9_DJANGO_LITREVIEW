from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# on utilise AbstractUser pour créer un utilisateur personnalisé
class User(AbstractUser):
    """
    on créé nôtre model user

    Args:
        AbstractUser (object): on hérite du model d'authentification 
    """

    pass
