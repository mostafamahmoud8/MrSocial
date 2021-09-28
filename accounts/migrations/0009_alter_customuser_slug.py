# Generated by Django 3.2.5 on 2021-09-09 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_customuser_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(allow_unicode=True, error_messages={'unique': 'A user with username aleardy exists.'}, unique=True),
        ),
    ]
