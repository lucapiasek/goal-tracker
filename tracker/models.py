from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import dateparse, timezone
from django.core.mail import send_mail

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, default='')
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    is_concluded = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.name}{' - ' if self.date or self.time else ''}{self.date if self.date else ''}{', ' if self.date and self.time else ''}{self.time if self.time else ''}"

class Piece(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goals = models.ManyToManyField("Goal", blank=True, related_name="pieces")
    name = models.CharField(max_length=200, blank=True, default='')
    composers = models.ManyToManyField("Composer", blank=True, related_name="pieces")
    name_to_display = models.CharField(max_length=200, blank=True, default='')
    color = models.CharField(max_length=60, blank=True, default='') # todo: model Color - choices
    is_mastered = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_cleared = models.BooleanField(default=False)

    def __str__(self):
        return self.name_to_display if self.name_to_display else self.name

class Composer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    names = models.CharField(max_length=49, blank=True, default='')
    surname = models.CharField(max_length=30, blank=True, default='')
    display_name = models.CharField(max_length=80, blank=True, default='')

    def __str__(self):
        return self.display_name if self.display_name else self.names + ' ' + self.surname

class Collection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    composer = models.ForeignKey("Composer", blank=True, null=True, on_delete=models.CASCADE)
    opus = models.CharField(max_length=10)
    pieces = models.ManyToManyField("Piece", blank=True, related_name="collections")

    def __str__(self):
        return self.name

class PieceInformation(models.Model):
    piece = models.OneToOneField("Piece", on_delete=models.CASCADE, related_name="piece_information")
    opus = models.CharField(max_length=30, blank=True, default='')
    number = models.CharField(max_length=30, blank=True, default='')
    pitch = models.CharField(max_length=30, blank=True, default='')
    types = models.ManyToManyField("Type", blank=True, related_name="pieces_information")
    genres = models.ManyToManyField("Genre", blank=True, related_name="pieces_information")
    styles = models.ManyToManyField("Style", blank=True, related_name="pieces_information")
    time_to_master = models.DurationField(blank=True, null=True, help_text="Sugerowany czas opanowania utworu")

class Type(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class Genre(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.genre

class Style(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    style = models.CharField(max_length=30, default='')

    def get_absolute_url(self):
        return reverse('tracker:style_update', args=[self.user.username, self.pk])

    def __str__(self):
        return self.style

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal = models.ForeignKey("Goal", blank=True, null=True, on_delete=models.CASCADE)
    piece = models.ForeignKey("Piece", blank=True, null=True, on_delete=models.CASCADE)
    parts = models.ManyToManyField("Part", blank=True, related_name="tasks")
    element = models.CharField(max_length=80, blank=True, default='')
    method = models.CharField(max_length=100, blank=True, default='')
    are_suggestions_enabled = models.BooleanField(default=True)
    is_suggested = models.BooleanField(default=False)
    was_practiced = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.piece if self.piece else self.goal} -- {self.element if self.element else ''} -- {self.method if self.method else ''}"

    def timedeltas(self):
        initial = [3, 4, 7, 28, 84]
        return [dateparse.parse_duration(f"{value} 00:00:00.000000") for value in initial]

    def set_is_suggested(self):
        today = timezone.localdate(timezone.now())
        practiced_at = self.practice_set.earliest('date').date
        if today - practiced_at in self.timedeltas():
            self.is_suggested = True
        else:
            self.is_suggested = False

    def send_email_suggestion(self):
        if self.are_suggestions_enabled and hasattr(self.user, 'email'):
            last_practice = self.practice_set.latest('date')
            send_mail(
                "Practice suggestion",
                f"You practiced {self.__str__()} at {last_practice}. Practice now!",
                recipient_list=[f'{self.user.email}']
            )


class Practice(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.DurationField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    repetitions = models.DecimalField(decimal_places=1, max_digits=3, blank=True, null=True)
    is_summarized = models.BooleanField(null=True)
    is_completed = models.BooleanField(null=True)
    completion_percentage = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.date}, {self.start_time if self.start_time else ''} {self.end_time if self.end_time else ''}"

class Part(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=True, default='')
    piece = models.ForeignKey("Piece", blank=True, null=True, on_delete=models.CASCADE)
    master_part = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="inside_parts")
    number_of_main_parts = models.IntegerField(blank=True, null=True)
    order_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name if self.name else ''} {self.order_number if self.order_number else ''} - {self.piece if self.piece else ''}"

class Challenge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey("Task", related_name="challenges", on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    start_date = models.DateField(blank=True, null=True)
    minimum_number_of_days = models.IntegerField(default=0)
    minimum_number_of_repetitions = models.IntegerField(default=0)
    minimum_total_repetitions = models.IntegerField(default=0)
    are_requirements_fulfilled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task} - added: {self.start_date if self.start_date else self.date_added}"

    def check_number_of_days(self):
        if self.task.was_practiced:
            task = Task.objects.select_related('practice').get(task=self.task)
            if self.minimum_number_of_days <= 0:
                return True
            else:
                required_repetitions = self.minimum_number_of_repetitions if self.minimum_number_of_repetitions >= 0 else 0
                if self.minimum_number_of_days < len(task.practice_set.filter(repetitons__gte=required_repetitions).dates('date', 'day')):
                    return True
        return False

    def check_repetitions(self):
        if self.task.was_practiced:
            if self.minimum_total_repetitions <= 0:
                return True
            else:
                total_repetitions = Practice.objects.filter(task=self.task).aggregate(total_repetitions=models.Sum("repetitions"))[0]
                return self.minimum_total_repetitions <= total_repetitions
        return False

    def check_if_fulfilled(self):
        return self.check_number_of_days() and self.check_repetitions()

    def set_are_requirements_fulfilled(self):
        self.are_requirements_fulfilled = self.check_if_fulfilled()
        return self.are_requirements_fulfilled