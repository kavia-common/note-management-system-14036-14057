from django.db import models
from django.contrib.auth.models import User

# PUBLIC_INTERFACE
class Note(models.Model):
    """
    Represents a note belonging to a user.
    """
    user = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
