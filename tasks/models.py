from django.db import models

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

