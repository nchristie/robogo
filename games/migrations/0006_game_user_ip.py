# Generated by Django 3.2.13 on 2022-06-19 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_alter_game_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='user_ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]