# Generated by Django 3.2.8 on 2021-10-21 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_delete_booktype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default_cover.jpg', upload_to='profile_pics'),
        ),
    ]
