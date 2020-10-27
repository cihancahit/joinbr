from django.urls import path

from .views import  ReportReviewView, submit_company_report, submit_generic_review

urlpatterns = [
    path('report/<int:id>', ReportReviewView.as_view(), name="report_review"),
    path('submit-report/<int:id>', submit_company_report, name="submit_company_report"),
    path('submit-review/<str:content>/<int:pk>', submit_generic_review, name="submit_generic_review"),
]
