from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.permissions import is_owner_or_is_teacher
from tracker.models import Goal, Practice
from tracker_calendar.utils import MyHTMLCalendar
from django.utils.dateparse import parse_date

UserModel = get_user_model()

class YearView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, year):
        owner = get_object_or_404(UserModel, username=username)
        goals = Goal.objects.filter(user=owner)
        practice = Practice.objects.filter(task__user=owner) if request.user == owner else Practice.objects.none()
        c = MyHTMLCalendar(goals=goals, practice=practice)
        html_calendar = c.formatyear(year)
        return render(request, 'tracker_calendar/year_view.html', {'cal': html_calendar, 'owner': owner})

class DayView(UserPassesTestMixin, View):
    def test_func(self):
        return is_owner_or_is_teacher(self.request.user, self.kwargs['username'])

    def get(self, request, username, year, month, day):
        owner = get_object_or_404(UserModel, username=username)
        date = parse_date("%s.%s.%s" % (day, month, year))
        goal_list = Goal.objects.filter(user=owner).filter(date=date)
        if request.user == owner:
            practice_list = Practice.objects.filter(task__user=owner).filter(date=date)
        else:
            practice_list = Practice.objects.none()
        return render(
            request,
            'tracker_calendar/day_view.html',
            {
                'date': "%s.%s.%s" % (day, month, year),
                'goal_list': goal_list,
                'practice_list': practice_list,
                'owner': owner
            })

