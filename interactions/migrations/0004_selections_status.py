# Generated by Django 5.0.6 on 2024-07-05 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0003_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='selections',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('completed', 'Completed')], default='active', max_length=10),
        ),
    ]
