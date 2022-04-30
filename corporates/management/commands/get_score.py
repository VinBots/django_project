from corporates.models import Verification, CompanyScore, Corporate, Score
from django.core.management import BaseCommand
from django.db.models import Q


def score_duplicate(score_details):

    my_filter = Q()
    for item in score_details:
        my_filter &= Q(**{item: score_details[item]})

    return CompanyScore.objects.filter(my_filter).exists()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):

        score_name = "Score_6_2"
        company_name = options["company_name"]

        queryset = CompanyScore.objects.filter(
            company__company_id=company_name, score__name=score_name
        ).order_by("-update_date", "-score_value")
        print(queryset.values())

        if queryset.exists():
            print(f"The Score is {queryset[0].score_value}")
        else:
            print(f"no score {score_name} for {company_name} found")
