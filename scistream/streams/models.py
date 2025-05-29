import uuid
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

class StreamKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, unique=True, default=uuid.uuid4)

    def regenerate_key(self):
        self.key = uuid.uuid4()
        self.save()

