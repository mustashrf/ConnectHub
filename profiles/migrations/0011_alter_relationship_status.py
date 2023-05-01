# Generated by Django 4.2 on 2023-04-18 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_alter_relationship_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='status',
            field=models.CharField(choices=[('send', 'send'), ('accept', 'accept'), ('remove', 'remove')], max_length=8),
        ),
    ]