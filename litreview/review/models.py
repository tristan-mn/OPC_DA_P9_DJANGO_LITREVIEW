from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

from PIL import Image

class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Ticket(models.Model):
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    photo = models.ForeignKey(Photo, null=True, on_delete=models.CASCADE, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    #contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BlogContributor', related_name='contributions')



class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0),
        MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name='following',
                            null=True, blank=True)

    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                        on_delete=models.CASCADE,
                                        related_name='followed_by',
                                        null=True,
                                        blank=True)
    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )

