# Generated by Django 4.0.1 on 2022-02-07 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
