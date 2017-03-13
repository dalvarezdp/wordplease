from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):

    class Meta:
        verbose_name_plural = "Posts"

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='post', verbose_name='image')
    categories = models.ManyToManyField(Category)
    date_public = models.DateTimeField(db_index=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Añade automáticamente la fecha de creación
    modified_at = models.DateTimeField(auto_now=True)  # Actualiza la fecha al guardar automáticamente
    owner = models.ForeignKey(User, related_name="owned_posts")

    def __str__(self):
        return self.name

