# Generated by Django 3.1.4 on 2020-12-03 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0009_auto_20201203_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='image',
        ),
    ]
