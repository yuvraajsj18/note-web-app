from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    """
        Represents a user with:
        username, email, password
    """
    email = models.EmailField(blank=False)
    
    def __str__(self):
        return f"{self.username}"

    
class Note(models.Model):
    """Represent a note"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    text = models.TextField(blank=False)
    color = models.CharField(max_length=64, blank=True)
    labels = models.ManyToManyField("Label", blank=True, related_name="notes")
    is_archived = models.BooleanField(default=False)
    # datetime when post last updated or post for the first time
    datetime = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        allowed_colors = ('red', 'green', 'blue', 'purple', 'white', '')

        if self.color not in allowed_colors:
            return
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for label in self.labels.all():
            if label.notes.count() == 1:
                label.delete()
        
        super().delete(*args, **kwargs)
            

    def __str__(self):
        return f"Note {self.id} : {self.text[ : 20]}"

    def serializer(self):
        return {
            'noteId': self.id,
            'username': self.user.username,
            'text': self.text,
            'color': self.color,
            'labels': [label.serializer() for label in self.labels.all()],
            'isArchived': self.is_archived,
            'datetime': self.datetime.strftime("%b %d %Y, %I:%M %p"),
        }

class Label(models.Model):
    """Represent labels"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="labels")
    label = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"Label {self.id} : {self.label}"

    def serializer(self):
        return {
            'labelId': self.id,
            'username': self.user.username,
            'label': self.label,
        }

