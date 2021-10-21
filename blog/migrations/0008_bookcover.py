# Generated by Django 3.2.8 on 2021-10-21 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20211020_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='book_covers')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
        ),
    ]