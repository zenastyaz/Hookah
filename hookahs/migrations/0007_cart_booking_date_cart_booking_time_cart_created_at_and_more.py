# Generated by Django 5.0.7 on 2024-07-28 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hookahs', '0006_order_address_order_booking_date_order_booking_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='booking_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='booking_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
