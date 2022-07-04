from datetime import datetime, tzinfo
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from pytz import UTC

from corporates.models import UserProfile, Corporate, GeneralInfo, CorporateGrouping
from corporates.models.external_sources.cdp import CDP
from corporates.models.ghg import GHGQuant
from corporates.models.targets import TargetQuant
from corporates.models.verification import Verification


def days_ago(last_update):
    today = datetime.now(tz=UTC)
    delta = today - last_update
    return delta.days


def get_input_status_general(corp):

    query = GeneralInfo.objects.filter(
        company=corp,
        year__in=["2021", "2022"],
    ).order_by("-year", "-last_update")
    if query.exists():
        return query[0].year
    else:
        return "Missing"


def get_input_status_disclosures(corp):
    query = Verification.objects.filter(
        company=corp,
        reporting_year__in=["2021", "2022"],
    ).order_by("-reporting_year", "-last_update")
    if query.exists():
        return query[0].reporting_year
    else:
        return "Missing"


def get_input_status_net0(corp):

    query = Verification.objects.filter(
        company=corp,
    ).order_by("-last_update")
    if query.exists():
        return f"last: {days_ago(query[0].last_update)} days ago"
    else:
        return "no record"


def get_input_status_ghg(corp):
    query = GHGQuant.objects.filter(company=corp, source="public").order_by(
        "-reporting_year", "-last_update"
    )

    if query.exists() and query[0].last_update:
        print(query[0].last_update)
        msg = f"last: {days_ago(query[0].last_update)} days ago"
        # query_year = query.filter(reporting_year__in=["2021", "2022"])
        # if query_year.exists():
        #     msg += f" / Recent: {query_year[0].reporting_year}"
        return msg
    else:
        return "no record"


def get_input_status_recent_ghg(corp):
    query = GHGQuant.objects.filter(
        company=corp, source="public", reporting_year__in=["2021", "2022"]
    ).order_by("-reporting_year", "-last_update")

    if query.exists():
        return query[0].scope_123_loc
    else:
        return "no record"


def get_input_status_targets(corp):
    query = TargetQuant.objects.filter(
        company=corp,
    ).order_by("-last_update")
    if query.exists():
        return f"last: {days_ago(query[0].last_update)} days ago"
    else:
        return "no record"


def get_input_status_cdp(corp):
    query = CDP.objects.filter(
        company=corp,
        questionnaire_year__in=["2020", "2021"],
    ).order_by("-questionnaire_year", "-last_update")
    if query.exists():
        return f"{query[0].questionnaire_year} - {query[0].score}"
    else:
        return "Missing"


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
            return redirect(path)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        input_dict = {}
        for corp in context["data"]:
            input_dict[corp] = {
                "general": get_input_status_general(corp),
                "disclosures": get_input_status_disclosures(corp),
                "net0": get_input_status_net0(corp),
                "ghg": get_input_status_ghg(corp),
                "ghg_value": get_input_status_recent_ghg(corp),
                "targets": get_input_status_targets(corp),
                "cdp": get_input_status_cdp(corp),
            }

        context["input_status"] = input_dict
        return context

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
            sp100_company_ids = CorporateGrouping.objects.get_sp100_company_ids()
            return Corporate.objects.filter(company_id__in=sp100_company_ids)

    def is_allowed_corporates_all(self):

        test1 = UserProfile.objects.filter(
            user=self.request.user, allowed_corporates_all=True
        ).exists()
        return test1
