# Generated by Django 2.1.5 on 2021-03-01 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='post_code',
            new_name='postal_code',
        ),
    ]
