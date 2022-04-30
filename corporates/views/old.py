from django.conf import UserSettingsHolder
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from corporates.forms import GHGForm
from .models import GHGQuant, UserProfile
from django.urls import reverse_lazy
from django.shortcuts import render
from typing import Any, Dict

from django.shortcuts import render, redirect
from corporates.models import Corporate, MSCI
from django.urls import reverse
from corporates.utilities import (
    get_library_data,
    get_path_to_chart,
    check_validity,
    get_ghg,
    get_path_to_img,
    get_score_data,
    get_scores_summary,
    get_targets,
    file_exist,
    get_scores_details,
    get_all_data_from_csv,
    AllowedCorporateMixin,
    get_company_id_from_name,
)

from pathlib import Path
import os
from config import Config as c


def corporates_search(request, corp_name=None):

    if request.GET.get("query") is not None:
        path = reverse("corporates_home") + request.GET.get("query")
        return redirect(path)

    if check_validity(corp_name):

        selected_corp = Corporate.objects.get(name=corp_name)
        metadata = (
            MSCI.objects.filter(company_id=selected_corp.company_id)
            .order_by("date")
            .reverse()
        )

        sheet_names = [
            c.DATA_FROM_XLSX.GHG_QUANT,
            c.DATA_FROM_XLSX.CORP_SCORES,
            c.DATA_FROM_XLSX.SCORES_SUMMARY,
            c.DATA_FROM_XLSX.TARGETS_QUANT,
            c.DATA_FROM_XLSX.SCORES_DETAILS,
            c.LIBRARY.LIST_CSV,
            c.DATA_FROM_XLSX.REPORTING,
        ]

        all_data = get_all_data_from_csv(sheet_names)

        db_corp = {"corp_scores_details": metadata}

        xls_corp = {
            "ghg": get_ghg(
                company_id=selected_corp.company_id,
                all_data=all_data[c.DATA_FROM_XLSX.GHG_QUANT],
                reporting_year_data=all_data[c.DATA_FROM_XLSX.REPORTING],
            ),
            "score_data": get_score_data(
                company_id=selected_corp.company_id,
                all_data=all_data[c.DATA_FROM_XLSX.CORP_SCORES],
            ),
            "corp_scores_summary": get_scores_summary(
                company_id=selected_corp.company_id,
                all_data=all_data[c.DATA_FROM_XLSX.SCORES_SUMMARY],
            ),
            "corp_scores_details": get_scores_details(
                company_id=selected_corp.company_id,
                all_data=all_data[c.DATA_FROM_XLSX.SCORES_DETAILS],
            ),
            "targets": get_targets(
                company_id=selected_corp.company_id,
                all_data=all_data[c.DATA_FROM_XLSX.TARGETS_QUANT],
            ),
        }

        library_corp = get_library_data(
            company_id=selected_corp.company_id, all_data=all_data[c.LIBRARY.LIST_CSV]
        )

        corp_data = {
            "selected_corp": selected_corp,
            "xls_corp": xls_corp,
            "db": db_corp,
            "library_corp": library_corp,
            "selected_corp_bullet_chart": {
                "html": get_path_to_chart(selected_corp.company_id, "bullet"),
                "img": get_path_to_img(selected_corp.company_id, "bullet"),
            },
            "selected_corp_bubble_chart": {
                "html": get_path_to_chart(selected_corp.company_id, "bubble"),
                "img": get_path_to_img(selected_corp.company_id, "bubble"),
                "exist": file_exist(
                    get_path_to_img(selected_corp.company_id, "bubble")
                ),
            },
            "selected_corp_ghg_bar_chart": {
                "html": get_path_to_chart(selected_corp.company_id, "ghg_bar"),
                "img": get_path_to_img(selected_corp.company_id, "ghg_bar"),
                "exist": file_exist(
                    get_path_to_img(selected_corp.company_id, "ghg_bar")
                ),
            },
            "selected_corp_ghg_scope3_pie_chart": {
                "html": get_path_to_chart(selected_corp.company_id, "ghg_pie_chart"),
                "img": get_path_to_img(selected_corp.company_id, "ghg_pie_chart"),
                "exist": file_exist(
                    get_path_to_img(selected_corp.company_id, "ghg_pie_chart")
                ),
            },
        }

        return render(request, "django_project/corporates/main.html", corp_data)
    else:
        return render(
            request,
            "django_project/corporates/home.html",
            {
                "error_msg": "No match found",
                "corporates_names": Corporate.objects.all(),
                "random_logos": Corporate.objects.random(),
            },
        )


def corporates_home(request):

    if request.GET.get("query") is not None:
        path = reverse("corporates_home") + request.GET.get("query")
        return redirect(path)

    return render(
        request,
        "django_project/corporates/home.html",
        {
            "error_msg": "",
            "corporates_names": Corporate.objects.all(),
            "random_logos": Corporate.objects.random(),
        },
    )


def show_html(request, folder_name=None, file_name=None):

    BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")

    DIR_TO_CORP_CHARTS_TEMPLATES = (
        "templates/django_project/corporates/charts/html_exports/"
    )

    path = os.path.join(BASE_DIR, DIR_TO_CORP_CHARTS_TEMPLATES, folder_name, file_name)

    return render(
        request,
        "django_project/corporates/show_interactive.html",
        {
            "path": path,
        },
    )


def home(request):

    return render(request, "django_project/input/main.html")


def input_home(request):

    return render(request, "django_project/input/main.html")


class ChooseCorporateList(LoginRequiredMixin, ListView):

    model = UserProfile
    template_name = "django_project/input/main.html"
    context_object_name = "data"

    def dispatch(self, request, *args, **kwargs):

        if self.request.GET.get("corp") is not None:
            path = reverse(
                "input_by_corp_general",
                kwargs={"corp_name": self.request.GET.get("corp")},
            )
            print("NOT GET QUERY")
            return redirect(path)

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        if not self.is_allowed_corporates_all():
            corp_list_query = (
                super()
                .get_queryset()
                .filter(user=self.request.user)
                .values_list("allowed_corporates__name")
            )
            return [corp[0] for corp in corp_list_query]
        else:
            return Corporate.objects.all()

    def is_allowed_corporates_all(self):

        test1 = UserProfile.objects.filter(
            user=self.request.user, allowed_corporates_all=True
        ).exists()
        # print(test1)
        return test1


class InputGeneral(AllowedCorporateMixin, View):

    template_name = "django_project/input/corp_general.html"

    def get(self, request, *args, **kwargs):
        kwargs["category"] = "general"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)


class GHGListCreate(AllowedCorporateMixin, CreateView):

    initial = {}
    form_class = GHGForm
    template_name = "django_project/input/corp_ghg.html"

    def get(self, request, *args, **kwargs):

        form = self.form_class(initial=self.initial)
        kwargs["form"] = form
        kwargs["category"] = "ghg"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = reverse(
            "input_by_corp_general", kwargs={"corp_name": context["corp_name"]}
        )

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        if self.request.user != "django":
            form.instance.submitter = self.request.user
            # form.instance.verifier = "pending"
            form.instance.status = "submitted"
        return super(GHGListCreate, self).form_valid(form)


class GHGListUpdate(AllowedCorporateMixin, UpdateView):

    initial = {}
    form_class = GHGForm
    template_name = "django_project/input/corp_ghg.html"

    def get(self, request, *args, **kwargs):

        form = self.form_class(initial=self.initial)
        kwargs["form"] = form
        kwargs["category"] = "ghg"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = reverse(
            "input_by_corp_general", kwargs={"corp_name": context["corp_name"]}
        )

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        if self.request.user != "django":
            form.instance.submitter = self.request.user
            # form.instance.verifier = "pending"
            form.instance.status = "submitted"
        return super(GHGListCreate, self).form_valid(form)


class InputVerification(AllowedCorporateMixin, View):

    template_name = "django_project/input/corp_general.html"

    def get(self, request, *args, **kwargs):
        kwargs["category"] = "verification"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)


class InputTargets(AllowedCorporateMixin, View):

    template_name = "django_project/input/corp_general.html"

    def get(self, request, *args, **kwargs):
        kwargs["category"] = "targets"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)


class InputComments(AllowedCorporateMixin, View):

    template_name = "django_project/input/corp_general.html"

    def get(self, request, *args, **kwargs):
        kwargs["category"] = "comments"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)


# class GHGListUpdate(AllowedCorporateMixin, UpdateView):
#     model = GHGQuant
#     fields = "__all__"
#     success_url = reverse_lazy("ghg")
#     template_name = "django_project/input/ghg/update.html"

#     # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#     #     context = super().get_context_data(**kwargs)
#     #     context["ghg"] = context["ghg"].filter(status="verified")
#     #     return context
