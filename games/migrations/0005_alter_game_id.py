# Generated by Django 3.2.13 on 2022-06-19 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_rename_move_player_move_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]