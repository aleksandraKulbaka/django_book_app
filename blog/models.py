from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image

class Post(models.Model):
    bookTitle = models.CharField(max_length=100)
    bookAuthor = models.CharField(max_length=100)
    review = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public =  models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.bookTitle + " by " + self.bookAuthor

# redirect takes to the url, 
# reverse returns the url
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
class BookCover(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="book_cover")
    image = models.ImageField(default='default_cover.jpg', upload_to='book_covers')

    def __str__(self) -> str:
        return f'{self.post.bookTitle} Cover'

    # # to rescale the image
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)