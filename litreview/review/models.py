from wsgiref.validate import validator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

from PIL import Image

class Photo(models.Model):
    """
    on créé le model photo
    Args:
        models (object): on hérite de l'objet Model des models de database de django 
    """
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (400, 400)

    def resize_image(self):
        """
        on défini la taille maximum des images du model Photo
        """
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """
        on redéfini la fonction save du model Photo
        """
        super().save(*args, **kwargs)
        self.resize_image()


class Ticket(models.Model):
    """
    on créé le model ticket

    Args:
        models (object): on hérite de l'objet Model des models de database de django 
    """
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=2048, blank=True)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, null=True, on_delete=models.CASCADE, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)



class Review(models.Model):
    """
    on créé le model review

    Args:
        models (object): on hérite de l'objet Model des models de database de django 
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    """
    on créé le model UserFollows

    Args:
        models (object): on hérite de l'objet Model des models de database de django 
    """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')
