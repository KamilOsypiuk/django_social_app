# Generated by Django 4.2.1 on 2023-06-15 13:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("relations", "0003_block_friendship_relation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="friendshiprelation",
            name="friends",
        ),
        migrations.RemoveField(
            model_name="friendshiprelation",
            name="user",
        ),
        migrations.RemoveField(
            model_name="friendshiprequest",
            name="from_user",
        ),
        migrations.RemoveField(
            model_name="friendshiprequest",
            name="to_user",
        ),
        migrations.DeleteModel(
            name="Block",
        ),
        migrations.DeleteModel(
            name="FriendshipRelation",
        ),
        migrations.DeleteModel(
            name="FriendshipRequest",
        ),
    ]
