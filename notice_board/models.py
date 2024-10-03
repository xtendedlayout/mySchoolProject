from django.db import models
from django.contrib.auth.models import AbstractUser

#create your models here

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Announcement(models.Model):
    TITLE_CHOICES = (
        ('general', 'General'),
        ('class', 'Class'),
        ('course', 'Course'),
        ('intake', 'Intake'),
        ('event', 'Event')
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    type = models.CharField(max_length=20, choices=TITLE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)

class Comments(models.Model):
    comment = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment_for = models.ForeignKey(Announcement, on_delete=models.CASCADE)
