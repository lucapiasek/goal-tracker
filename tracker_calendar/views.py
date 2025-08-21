from django.shortcuts import render, get_object_or_404
from django.views import View
import calendar
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from django.template import Template
from tracker.models import Goal, Practice
from django.conf import settings

UserModel = get_user_model()

class MyHTMLCalendar(calendar.LocaleHTMLCalendar):
    def __init__(self, goals=Goal.objects.none(), practice=Practice.objects.none()):
        super().__init__()
        self.goals = goals
        self.practice = practice

    def add_tasks(self, y, m, d):
        datetime.date(year=y, month=m, day=d)
        goals_filtered = self.goals.filter(date=datetime.date(year=y, month=m, day=d))
        practices_filtered=self.practice.filter(date=datetime.date(year=y, month=m, day=d))
        result = ''
        for goal in goals_filtered:
            result += goal.__str__()
        for practice in practices_filtered:
            result += practice.__str__()
        return result

    def monthlen(self, year, month):
        return calendar.mdays[month] + (month == calendar.FEBRUARY and calendar.isleap(year))

    def prevmonth(self, year, month):
        if month == 1:
            return year - 1, 12
        else:
            return year, month - 1

    def nextmonth(self, year, month):
        if month == 12:
            return year + 1, 1
        else:
            return year, month + 1

    def itermonthdays5(self, year, month):
        """
        Like itermonthdates(), but will yield (year, month, day) tuples.
        For days outside the specified month the day number is 0.
        """
        day1, ndays = calendar.monthrange(year, month)
        days_before = (day1 - self.firstweekday) % 7
        days_after = (self.firstweekday - day1 - ndays) % 7
        y, m = self.prevmonth(year, month)
        end = self.monthlen(y, m) + 1
        for d in range(end - days_before, end):
            yield y, m, 0
        for d in range(1, ndays + 1):
            yield year, month, d
        y, m = self.nextmonth(year, month)
        for d in range(1, days_after + 1):
            yield y, m, 0

    def itermonthdays6(self, year, month):
        """
        Like itermonthdates(), but will yield (year, month, day, weekday) tuples.
        For days outside the specified month the day number is 0.
        """
        for i, (y, m, d) in enumerate(self.itermonthdays5(year, month)):
            yield y, m, d, (self.firstweekday + i) % 7

    def itermonthdays2(self, year, month):
        """
        Return d, m, y, week_day in monthdays2calendar instead of day, weekday.
        Used in self.monthdays2calendar in self.formatmonth
        """
        return self.itermonthdays6(year, month)

    def formatday(self, d, m, y, wd):
        if d == 0:
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            return f'<td class="{self.cssclasses[wd]}"><a href="{m}/{d}">{d}</a>{self.add_tasks(y, m, d)}</td>'

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, m, y, wd) for (y, m, d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Same as calendar.HTMLCalendar.formatmonth, with removed newlines
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a(self.formatweekheader())
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
        a('</table>')
        return ''.join(v)

    def formatyear(self, theyear, width=3):
        """
        Same as calendar.HTMLCalendar.formatyear, with removed newlines
        Return a formatted year as a table of tables.
        """
        v = []
        a = v.append
        width = max(width, 1)
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' %
          self.cssclass_year)
        a('<tr><th colspan="%d" class="%s">%s</th></tr>' % (
            width, self.cssclass_year_head, theyear))
        for i in range(calendar.JANUARY, calendar.JANUARY+12, width):
            # months in this row
            months = range(i, min(i+width, 13))
            a('<tr>')
            for m in months:
                a('<td>')
                a(self.formatmonth(theyear, m, withyear=False))
                a('</td>')
            a('</tr>')
        a('</table>')
        return ''.join(v)

class YearView(View):
    def get(self, request, username, year):
        owner = get_object_or_404(UserModel, username=username)
        goals = goals=Goal.objects.filter(user=owner)
        practice=Practice.objects.filter(task__user=owner) if request.user == owner else Practice.objects.none()
        c = MyHTMLCalendar(goals=goals, practice=practice)
        html_calendar = c.formatyear(year)
        return render(request, 'tracker_calendar/year_view.html', {'cal': html_calendar})

class DayView(View):
    def get(self, request, username, year, month, day):
        owner = get_object_or_404(UserModel, username=username)
        date = datetime.date(year=year, month=month, day=day)
        goal_list = Goal.objects.filter(user=owner).filter(date=date)
        if request.user == owner:
            practice_list = Practice.objects.filter(task__user=owner).filter(date=date)
        else:
            practice_list = None
        return render(
            request,
            'tracker_calendar/day_view.html',
            {
                'date': date,
                'goal_list': goal_list,
                'practice_list': practice_list
            })

