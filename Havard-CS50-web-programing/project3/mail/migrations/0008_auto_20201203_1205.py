# Generated by Django 3.1.4 on 2020-12-03 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0007_auto_20201203_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='./media/default_user.png', upload_to='profile_pics'),
        ),
    ]