# Generated by Django 3.2.8 on 2022-04-20 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_orderitem_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriberList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]