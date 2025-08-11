from django.db import models

class Goal(models.Model):
    name = models.CharField(max_length=200, blank=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    is_concluded = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}{' - ' if self.date or self.time else ''}{self.date if self.date else ''}{', ' if self.date and self.time else ''}{self.time if self.time else ''}"

class Piece(models.Model):
    goals = models.ManyToManyField("Goal", blank=True, related_name="pieces")
    name = models.CharField(max_length=200, blank=True)
    composers = models.ManyToManyField("Composer", blank=True, related_name="pieces")
    name_to_display = models.CharField(max_length=200, blank=True)
    color = models.CharField(max_length=60, blank=True) # todo: model Color - choices
    is_mastered = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_cleared = models.BooleanField(default=False)

    def __str__(self):
        return self.name_to_display if self.name_to_display else self.name

class Composer(models.Model):
    names = models.CharField(max_length=49, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    display_name = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.display_name if self.display_name else self.names + ' ' + self.surname

class Collection(models.Model):
    name = models.CharField(max_length=50)
    composer = models.ForeignKey("Composer", blank=True, null=True, on_delete=models.CASCADE)
    opus = models.CharField(max_length=10)
    pieces = models.ManyToManyField("Piece", blank=True, related_name="collections")

    def __str__(self):
        return self.name

class PieceInformation(models.Model):
    piece = models.OneToOneField("Piece", on_delete=models.CASCADE)
    opus = models.CharField(max_length=30, blank=True)
    number = models.CharField(max_length=30, blank=True)
    pitch = models.CharField(max_length=30, blank=True)
    type = models.CharField(max_length=70, blank=True)
    time_to_master = models.DurationField(blank=True, null=True, help_text="Sugerowany czas opanowania utworu")

    def __str__(self):
        return self.opus + ' ' + self.number

class Type(models.Model):
    type = models.CharField(max_length=50)
    pieces = models.ManyToManyField("PieceInformation", blank=True, related_name="types")

    def __str__(self):
        return self.type

class Genre(models.Model):
    genre = models.CharField(max_length=50)
    pieces = models.ManyToManyField("PieceInformation", blank=True, related_name="genres")

    def __str__(self):
        return self.genre

class Style(models.Model):
    style = models.CharField(max_length=30)
    pieces = models.ManyToManyField("PieceInformation", blank=True, related_name="styles")

    def __str__(self):
        return self.style

class Task(models.Model):
    goal = models.ForeignKey("Goal", blank=True, null=True, on_delete=models.CASCADE)
    piece = models.ForeignKey("Piece", blank=True, null=True, on_delete=models.CASCADE)
    parts = models.ManyToManyField("Part", blank=True, related_name="tasks")
    element = models.CharField(max_length=80, blank=True)
    method = models.CharField(max_length=100, blank=True)
    is_suggested = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.piece if self.piece else self.goal} {self.parts if self.parts else ''} {self.element if self.element else ''} {self.method if self.method else ''}"

class Practice(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.DurationField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    repetitions = models.DecimalField(decimal_places=1, max_digits=3, blank=True, null=True)
    is_completed = models.BooleanField(null=True)
    completion_percentage = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.task}, {self.date}, {self.start_time if self.start_time else ''} {self.end_time if self.end_time else ''}"

class Part(models.Model):
    name = models.CharField(max_length=80, blank=True)
    piece = models.ForeignKey("Piece", blank=True, null=True, on_delete=models.CASCADE)
    master_part = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="inside_parts")
    number_of_main_parts = models.IntegerField(blank=True, null=True)
    order_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name if self.name else ''} {self.order_number if self.order_number else ''} - {self.piece if self.piece else ''}"

class Challenge(models.Model):
    tasks = models.ManyToManyField("Task", related_name="challenges")
    minimum_number_of_days = models.IntegerField()
    is_completed = models.BooleanField(null=True)

