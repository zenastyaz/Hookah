# Generated by Django 5.0.7 on 2024-08-16 13:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hookahs', '0014_orderkeitering'),
        ('users', '0002_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='number_of_people',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.address'),
        ),
    ]
