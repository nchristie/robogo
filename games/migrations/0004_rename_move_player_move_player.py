# Generated by Django 3.2.13 on 2022-06-18 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20220618_0342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='move',
            old_name='move_player',
            new_name='player',
        ),
    ]
