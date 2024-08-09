from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]



    title = models.CharField(max_length=150) #Post title
    content = models.TextField() # Post Content
    created_at = models.DateTimeField(auto_now_add=True) #creation time
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    
    def __str__(self):
        return self.title #display title to admin interface