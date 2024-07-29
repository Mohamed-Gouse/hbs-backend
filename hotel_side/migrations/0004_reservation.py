# Generated by Django 5.0.6 on 2024-07-19 07:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_side', '0003_alter_booking_payment_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('payment_status', models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending'), ('processing', 'Processing'), ('cancelled', 'Cancelled'), ('initiated', 'Initiated'), ('failed', 'Failed'), ('refunding', 'Refunding'), ('refunded', 'Refunded'), ('unpaid', 'Unpaid'), ('expired', 'Expired')], default='pending', max_length=100)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('total_days', models.PositiveIntegerField(default=1)),
                ('guests', models.PositiveIntegerField(default=1)),
                ('checked_in', models.BooleanField(default=False)),
                ('checked_out', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel_side.hotel')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel_side.room')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
