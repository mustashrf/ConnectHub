# Generated by Django 4.2 on 2023-04-03 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profile_first_name_alter_profile_last_name'),
        ('posts', '0004_alter_post_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='liked',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='profiles.profile'),
        ),
    ]
