from tokenize import String
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Game(models.Model):
    user_ip = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return f"{self.id}, {self.user_ip}"


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.CharField(max_length=6)
    x_coordinate = models.IntegerField()
    y_coordinate = models.IntegerField()

    def __str__(self):
        return f"""
        {self.player} 
        ({self.x_coordinate},{self.y_coordinate}) 
        move#{self.id}"""
