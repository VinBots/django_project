from corporates.models import (
    Corporate,
    GHGQuant,
    TargetQuant,
    CDP,
    Verification,
    CompanyScore,
    NetZero,
    Score,
    Benchmark,
    CorporateGrouping,
    Matching,
    GICS,
)
from django.core.management import BaseCommand


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):

        models_to_delete = [
            Corporate,
            GHGQuant,
            TargetQuant,
            CDP,
            Verification,
            CompanyScore,
            NetZero,
            Score,
            Benchmark,
            CorporateGrouping,
            Matching,
            GICS,
        ]

        for mod in models_to_delete:
            mod.objects.all().delete()
