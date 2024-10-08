# Generated by Django 5.0.7 on 2024-08-04 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hookahs', '0013_order_hookah_master_order_number_of_people'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderKeitering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard_qty', models.PositiveIntegerField(default=0, verbose_name='Количество стандарт кальянов')),
                ('premium_qty', models.PositiveIntegerField(default=0, verbose_name='Количество премиум кальянов')),
                ('hours', models.PositiveIntegerField(default=1, verbose_name='Количество часов')),
                ('delivery', models.BooleanField(default=False, verbose_name='Доставка')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес доставки')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Итого')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
        ),
    ]
