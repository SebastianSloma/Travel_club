# Generated by Django 4.1.5 on 2023-01-30 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel', '0002_alter_venue_email_address_alter_venue_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
