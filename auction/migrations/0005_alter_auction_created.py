# Generated by Django 5.1.1 on 2024-09-27 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0004_alter_category_options_rename_bid_auction_start_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='created',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
