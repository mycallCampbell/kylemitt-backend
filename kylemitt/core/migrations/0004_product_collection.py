# Generated by Django 3.2.8 on 2021-11-09 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_product_videoamount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]