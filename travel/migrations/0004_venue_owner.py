# Generated by Django 4.1.5 on 2023-02-02 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_alter_travel_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='owner',
            field=models.IntegerField(default=1, verbose_name='Venue Owner'),
        ),
    ]