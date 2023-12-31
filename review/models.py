from django.db import models
from django.conf import settings
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class Ticket(models.Model):
    def __str__(self):
        return self.title
    IMAGE_MAX_SIZE = (70, 70)
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
    title = models.CharField(max_length=128, verbose_name='titre')
    description = models.TextField(max_length=2048, verbose_name='description', blank=True)
    author  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='image', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    def __str__(self):
        return self.headline
    
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    """
    field hearts is for average and representations
    average = {average:{ 
                        average:value --> average of all ratings
                        full:value,   --> number of full hearts for average
                        empty:value,  --> number of empty hearts for average
                        half:value    --> number of half hearts for average
                        },
               author_rating:{
                              rating:value  --> rating of the author
                              full:value,   --> number of full hearts for author rating
                              empty:value,  --> number of empty hearts for author rating
                              half:value    --> number of half hearts for author rating
                              }
                }
    """
    hearts = models.JSONField(blank=True)
    headline = models.CharField(max_length=128, verbose_name='titre')
    body = models.TextField(max_length=8192, blank=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class UserFollows(models.Model):
    def __str__(self):
        return f'{self.user} suit {self.followed_user}'
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='user_connected')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='followed_user')
    
    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user')