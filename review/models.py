from django.db import models
from django.conf import settings
from PIL import Image
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
    description = models.CharField(max_length=2048, verbose_name='description', blank=True)
    author  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='image', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
