from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):

    CATEGORY_CHOICES = [
        ('Lab', 'Lab'),
        ('Hostel', 'Hostel'),
        ('Classroom', 'Classroom'),
        ('Library', 'Library'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.FileField(upload_to='complaints/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
