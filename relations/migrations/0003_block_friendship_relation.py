# Generated by Django 4.2.1 on 2023-06-14 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("relations", "0002_remove_friendshiprelation_user1_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="block",
            name="friendship_relation",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blocks",
                to="relations.friendshiprelation",
            ),
        ),
    ]