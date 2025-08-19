from django.shortcuts import render
from django.views import View
import datetime

class MonthsView(View):
    def get(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month

        return render('months_view.html', )
