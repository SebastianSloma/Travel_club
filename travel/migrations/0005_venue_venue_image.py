# Generated by Django 4.1.5 on 2023-02-03 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_venue_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='venue_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
