# Generated by Django 5.1.1 on 2024-09-30 15:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0005_alter_auction_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
