# Generated by Django 3.2.5 on 2021-09-10 01:52

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_customuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(upload_to=accounts.models.Uplaod_user_image),
        ),
    ]
