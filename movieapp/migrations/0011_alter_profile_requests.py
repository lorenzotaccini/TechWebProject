# Generated by Django 5.0.6 on 2024-07-02 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0010_alter_profile_requests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='requests',
            field=models.ManyToManyField(blank=True, default=None, related_name='requests', through='movieapp.Request', to='movieapp.movie'),
        ),
    ]