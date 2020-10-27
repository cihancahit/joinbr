import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView

from companies.models import Company, CompanyProduct
from expert.models import Expert
from events.models import Event
from fec_app.views import BaseContext
from .models import *
from users.models import UserProfileModel
from .serializers import PostedReviewSerializer


class ReportReviewView(BaseContext, TemplateView):
    template_name = "pages/report_review.html"

    def get_context_data(self, **kwargs):
        context = super(ReportReviewView, self).get_context_data(**kwargs)
        context["categories"] = ReportCategories.objects.filter(active=True)
        context["review_id"] = self.kwargs['id']
        return context


def submit_company_report(request, id):
    if request.method == "POST":
        print(request.POST)
        print(id)
        print(request.POST.get('rr-category'))
        print(request.POST.get('rr-description'))
        ReviewReports.objects.create(
            title=request.POST.get('rr-title'),
            description=request.POST.get('rr-description'),
            category=ReportCategories.objects.get(pk=1),
            review=ReviewModel.objects.get(pk=id),
        )
        return redirect("report_review", id=id)


@login_required
def submit_generic_review(request, content, pk):
    if request.method == "POST":
        print(request.POST.get('anon'))
        if content == "expert":
            model = Expert.objects.get(id=pk)
            avg_model = Expert.objects.filter(id=pk)
            query_name = "expert__pk"
        elif content == "company":
            model = Company.objects.get(id=pk)
            avg_model = Company.objects.filter(id=pk)
            query_name = "company__pk"
        elif content == "product":
            model = CompanyProduct.objects.get(id=pk)
            avg_model = CompanyProduct.objects.filter(id=pk)
            query_name = "product__pk"
        elif content == "event":
            model = Event.objects.get(id=pk)
            avg_model = Event.objects.filter(id=pk)
            query_name = "event__pk"
        user = UserProfileModel.objects.get(user=request.user)
        score = request.POST.get('stars')
        if score:
            rating_flag = True
        else:
            rating_flag = False
            score = None
        anon = False
        if request.POST.get('anon'):
            anon = True
        if content == "event":
            instance = ReviewModel.objects.create(
                content_object=model,
                user=user,
                position=request.POST.get('r-company-position'),
                content=request.POST.get('r-review'),
                content_title=request.POST.get('r-title'),
                anon=anon,
            )
        else:
            instance = ReviewModel.objects.create(
                content_object=model,
                user=user,
                reviewer_name=request.POST.get('r-name'),
                position=request.POST.get('r-company-position'),
                tags=request.POST.get('r-tag'),
                content=request.POST.get('r-review'),
                content_title=request.POST.get('r-title'),
                rating_flag=rating_flag,
                anon=anon,
                score=score,
            )
        # serialize created review instance
        queryset = ReviewModel.objects.filter(pk=instance.pk)
        serialized = PostedReviewSerializer(queryset, many=True,)
        if content != "event":
            if RatingModel.objects.filter(**{query_name: pk}).exists() is False:
                RatingModel.objects.create(
                    content_object=model,
                )
        if content != "event" and score:
            # TODO user type will be added
            score = int(score)
            if score == 1:
                RatingModel.objects.filter(**{query_name: pk}).update(
                    bad=RatingModel.objects.get(**{query_name: pk}).bad + 1
                )
            elif score == 2:
                RatingModel.objects.filter(**{query_name: pk}).update(
                    poor=RatingModel.objects.get(**{query_name: pk}).poor + 1
                )
            elif score == 3:
                RatingModel.objects.filter(**{query_name: pk}).update(
                    average=RatingModel.objects.get(**{query_name: pk}).average + 1
                )
            elif score == 4:
                RatingModel.objects.filter(**{query_name: pk}).update(
                    great=RatingModel.objects.get(**{query_name: pk}).great + 1
                )
            elif score == 5:
                RatingModel.objects.filter(**{query_name: pk}).update(
                    excellent=RatingModel.objects.get(**{query_name: pk}).excellent + 1
                )
            if RatingModel.objects.filter(**{query_name: pk}).exists():
                avg_model.update(avg_rating=round((RatingModel.objects.get(
                    **{query_name: pk}).excellent * 5 + RatingModel.objects.get(
                    **{query_name: pk}).great * 4 + RatingModel.objects.get(
                    **{query_name: pk}).average * 3 + RatingModel.objects.get(
                    **{query_name: pk}).poor * 2 + RatingModel.objects.get(
                    **{query_name: pk}).bad) / ReviewModel.objects.filter(**{query_name: pk}).filter(
                    rating_flag=True
                    ).count() * 20, 1))
        if content == "expert":
            return HttpResponse(json.dumps(serialized.data), content_type="application/json")
        elif content == "company":
            return HttpResponse(json.dumps(serialized.data), content_type="application/json")
        elif content == "product":
            company = model.company.all()[0]
            slug = Company.objects.get(id=company.id)
            return redirect("/company/" + str(slug))
        elif content == "event":
            return HttpResponse(json.dumps(serialized.data), content_type="application/json")
        else:
            return HttpResponse("Error")
