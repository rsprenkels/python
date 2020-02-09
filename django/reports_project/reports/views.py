from django.shortcuts import render
from django.views.generic import ListView
from .models import Report
from django_tables2 import SingleTableView

from .tables import ReportTable


def home(request):
    reports = Report.objects
    return render(request, 'reports/home.html', {'reports':reports})


class ReportListView(SingleTableView):
    model = Report
    table_class = ReportTable
    template_name = 'reports/reports.html'

class ReportFancyView(SingleTableView):
    model = Report
    table_class = ReportTable
    template_name = 'reports/reports_fancy.html'