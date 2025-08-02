from django.db import models
from django.core.exceptions import ValidationError

class Goal(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    is_concluded = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True, null=True)

    def clean(self):
        super().clean()
        if not (self.name or self.additional_info):
            raise ValidationError("At least one of the fields must be filled.")

class Piece(models.Model):
    goal = models.ManyToManyField("Goal", blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    name_to_display = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=60, blank=True, null=True) # todo: model Color - choices
    opus = models.CharField(max_length=30, blank=True, null=True)
    number = models.CharField(max_length=30, blank=True, null=True)
    genre = models.CharField(max_length=60, blank=True, null=True)
    collection_set = models.CharField(max_length=120, blank=True, null=True) # todo: model set - one to many
    period = models.CharField(max_length=100, blank=True, null=True)
    pitch = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=70, blank=True, null=True) # todo?: model Type // M2M choices
    time_to_master = models.DurationField(blank=True, null=True, help_text="Sugerowany czas opanowania utworu")
    is_mastered = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_cleared = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if not (self.name or self.goal or (self.collection_set and self.number)):
            raise ValidationError("At least one of the fields must be filled")

class Composer(models.Model):
    piece = models.ManyToMany("Piece")
    name = models.CharField(max_length=49)
    surname = models.CharField(30)
    display_name = models.CharField(maxlength=80)

class Task(models.Model):
    goal = models.ForeignKey("Goal", blank=True, null=True)
    piece = models.ForeignKey("Piece", blank=True, null=True, on_delete=models.CASCADE)
    part = models.ManyToMany("Part", blank=True, null=True)
    element = models.CharField(max_length=80, blank=True, null=True)
    method = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    repetitions_in_task = models.DecimalField(blank=True, null=True)
    is_completed = models.NullBooleanField()
    completeness_percentage = models.IntegerField(blank=True, null=True)

class Part(models.Model):
    piece = models.ForeignKey("Piece", blank=True, null=True, on_delete=models.CASCADE)
    master_part = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="inside_parts")
    number_of_main_parts = models.IntegerField(blank=True, null=True)
    order_number = models.IntegerField(blank=True, null=True)

class Challenge(models.Model):
    task = models.ManyToMany("Task")
    minimum_number_of_days = models.IntegerField(min_number=1)
    is_completed = models.NullBooleanField()

