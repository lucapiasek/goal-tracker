from django.db import models
from django.core.exceptions import ValidationError

class Goal(models.Model):
    name = models.CharField(max_length=200, blank=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    is_concluded = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True)

    def clean(self):
        super().clean()
        if not (self.name or self.additional_info):
            raise ValidationError("At least one of the fields must be filled.")

class Piece(models.Model):
    goals = models.ManyToManyField("Goal", blank=True, related_name="pieces")
    name = models.CharField(max_length=200, blank=True)
    composers = models.ManyToManyField("Composer", blank=True, related_name="pieces")
    name_to_display = models.CharField(max_length=200, blank=True)
    color = models.CharField(max_length=60, blank=True) # todo: model Color - choices
    is_mastered = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_cleared = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if not (self.name or self.goal or (self.collection and self.number)):
            raise ValidationError("At least one of the fields must be filled")

class Composer(models.Model):
    name = models.CharField(max_length=49)
    surname = models.CharField(30)
    display_name = models.CharField(max_length=80)

class Collection(models.Model):
    name = models.CharField(max_length=50)
    composer = models.ForeignKey("Composer", blank=True, null=True, on_delete=models.CASCADE)
    opus = models.CharField(max_length=10)
    pieces = models.ManyToManyField("Piece", blank=True, related_name="collections")

class PieceAdditionalInfo(models.Model):
    piece = models.OneToOneField("Piece", on_delete=models.CASCADE)
    opus = models.CharField(max_length=30, blank=True)
    number = models.CharField(max_length=30, blank=True)
    genre = models.CharField(max_length=60, blank=True)
    pitch = models.CharField(max_length=30, blank=True)
    type = models.CharField(max_length=70, blank=True)
    time_to_master = models.DurationField(blank=True, null=True, help_text="Sugerowany czas opanowania utworu")

class Style(models.Model):
    name = models.CharField(max_length=30)
    pieces = models.ManyToManyField("PieceAdditionalInfo", blank=True, related_name="pieces_additional_info")

class Task(models.Model):
    goal = models.ForeignKey("Goal", blank=True, null=True)
    piece = models.ForeignKey("Piece", blank=True, null=True, on_delete=models.CASCADE)
    parts = models.ManyToManyField("Part", blank=True, related_name="tasks")
    element = models.CharField(max_length=80, blank=True)
    method = models.CharField(max_length=100, blank=True)
    is_suggested = models.BooleanField(default=False)

class Practice(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.DurationField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    repetitions = models.DecimalField(blank=True, null=True)
    is_completed = models.BooleanField(null=True)
    completion_percentage = models.IntegerField(blank=True, null=True)

class Part(models.Model):
    piece = models.ForeignKey("Piece", blank=True, null=True, on_delete=models.CASCADE)
    master_part = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="inside_parts")
    number_of_main_parts = models.IntegerField(blank=True, null=True)
    order_number = models.IntegerField(blank=True, null=True)

class Challenge(models.Model):
    tasks = models.ManyToManyField("Task", related_name="challenges")
    minimum_number_of_days = models.IntegerField()
    is_completed = models.BooleanField(null=True)

