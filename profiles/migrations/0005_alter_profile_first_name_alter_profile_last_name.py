# Generated by Django 4.2 on 2023-04-03 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_first_name_alter_profile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
    ]
