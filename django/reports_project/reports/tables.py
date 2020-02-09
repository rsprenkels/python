import django_tables2 as tables
from .models import Report

class ReportTable(tables.Table):
    class Meta:
        model = Report
        template_name = "django_tables2/bootstrap.html"
        fields = ("title", "created", "query", )