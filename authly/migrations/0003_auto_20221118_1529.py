# Generated by Django 3.1 on 2022-11-18 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authly', '0002_auto_20221118_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='prifile_picture'),
        ),
    ]