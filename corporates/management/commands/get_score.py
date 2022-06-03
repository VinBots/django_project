from django.core.management import BaseCommand

from corporates.models import CompanyScore


class Command(BaseCommand):
    """
    Displays the score value for a given company_id
    """

    def add_arguments(self, parser):
        parser.add_argument("company_id", type=str)
        parser.add_argument("score_name", type=str)

    def handle(self, *args, **options):

        company_id = options["company_id"]
        score_name = options["score_name"]

        queryset = CompanyScore.objects.filter(
            company__company_id=company_id, score__name=score_name
        ).order_by("-last_update", "-score_value")

        if queryset.exists():
            print(
                f"The Score {score_name} for company id {company_id} is {queryset[0].score_value}"
            )
        else:
            print(f"no score {score_name} for company id {company_id} found")
