from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
class Post(models.Model):
    bookTitle = models.TextField()
    bookAuthor = models.TextField()
    review = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.bookTitle + " by " + self.bookAuthor

# redirect takes to the url, 
# reverse returns the url
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    