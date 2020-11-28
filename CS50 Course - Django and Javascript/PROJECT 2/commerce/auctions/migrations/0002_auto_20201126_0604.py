# Generated by Django 3.1.2 on 2020-11-26 06:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='createdOn',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auction',
            name='image',
            field=models.ImageField(blank=True, default='default.png', upload_to='images/'),
        ),
    ]
