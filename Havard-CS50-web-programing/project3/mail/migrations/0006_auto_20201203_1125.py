# Generated by Django 3.1.4 on 2020-12-03 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0005_auto_20201203_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='./images/default_user.png', upload_to=''),
        ),
    ]
