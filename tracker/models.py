from django.db import models

class Goal(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    is_concluded = models.BooleanField(default=False)

class Piece(models.Model):
    goal = models.ManyToManyField("Goal", blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    name_to_display = models.CharField(max_length=200, blank=True, null=True)
    composer = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=60, blank=True, null=True)
    opus = models.CharField(max_length=30, blank=True, null=True)
    number = models.CharField(max_length=30, blank=True, null=True)
    genre = models.CharField(max_length=60, blank=True, null=True)
    period = models.CharField(max_length=100, blank=True, null=True)
    pitch = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=70, blank=True, null=True)
    time_to_master = models.DurationField(blank=True, null=True, help_text="Sugerowany czas opanowania utworu")
    is_mastered = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_cleared = models.BooleanField(default=False)


