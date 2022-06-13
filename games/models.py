from django.contrib.postgres.fields import ArrayField
from django.db import models

class BoardState(models.Model):
    board = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=9,
        ),
        size=9,
    )