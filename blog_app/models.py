from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

def validate_content_length(value):
    if len(value.split()) < 20:
        raise ValidationError("Content must be at least 20 words.")

class Post(models.Model): 
    id = models.AutoField(primary_key=True)
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)]
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField(validators=[validate_content_length])
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} - {self.title}'
