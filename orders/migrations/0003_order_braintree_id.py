# Generated by Django 2.1.5 on 2021-03-08 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210301_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='braintree_id',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
