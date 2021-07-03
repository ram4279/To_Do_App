from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User #using djangos built in model


class TaskModel(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # one to many mapping, if user is deleted delete every task of the User
    title       = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    complete    = models.BooleanField(default=False)
    created     = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
