# Generated by Django 3.1.7 on 2021-04-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210405_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='photo',
            field=models.ImageField(upload_to='author/'),
        ),
    ]
