from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from multiselectfield import MultiSelectField

BOOK_TYPES = (
    ('FANTASY', 'Fantasy'),
    ('ADVENTURE', 'Adventure'),
    ('SCI_FI', 'Science Fiction'),
    ('BIOGRAPHY', 'Biography'),
    ('HORROR', 'Horror'),
    ('HISTORY', 'History'),
    ('NOVEL', 'Novel'),
    ('ROMANCE', 'Romance'),
    ('NON_FIC', 'Non fiction'),
    ('SCIENCE', 'Science'),
    ('ECONOMICS', 'Novel'),
    ('CLASSICS', 'Classics')
    )

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self) -> str:
        return f'{self.user.username} Profile'

    # to rescale the image
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class BookInterest(models.Model):
    interests = MultiSelectField(choices=BOOK_TYPES)
    user = models.OneToOneField(User, related_name="book_interests", on_delete=models.CASCADE)
    
    def __str__(self):
        return ", ".join(self.interests)
    