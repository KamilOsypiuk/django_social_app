# Generated by Django 4.2.1 on 2023-06-18 13:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_alter_user_blocks_alter_user_friend_requests_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="friend_requests",
        ),
        migrations.AddField(
            model_name="user",
            name="friend_invitations",
            field=models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="user",
            name="blocks",
            field=models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="user",
            name="friends",
            field=models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]