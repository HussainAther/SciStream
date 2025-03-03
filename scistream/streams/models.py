from django.db import models
from django.contrib.auth.models import User

class Stream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title

