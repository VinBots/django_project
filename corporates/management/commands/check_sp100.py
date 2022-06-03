import os, sys, logging
from django.conf import settings

from django.core.management import BaseCommand
from corporates.models.grouping import CorporateGrouping
from corporates.models.external_sources.matching import Matching


sys.path.append(os.path.join(settings.SERVER_BASE_DIR, "scripts"))
from providers.tradingview_data import TradingviewData


class Command(BaseCommand):
    def handle(self, *args, **options):

        tv = TradingviewData(requested_fields=["a"], list_key=[1])
        sp100_from_tv_list = tv.get_sp_100_constituents()
        double_tickers = ["NASDAQ-GOOG"]
        for ticker in double_tickers:
            sp100_from_tv_list.remove(ticker)

        sp100_company_ids = CorporateGrouping.objects.get_sp100_company_ids()
        sp100_from_db_list = list(
            Matching.objects.filter(
                company__company_id__in=sp100_company_ids
            ).values_list("tradingview_symbol", flat=True)
        )

        sp100 = Matching.objects.filter(company__company_id__in=sp100_company_ids)
        for comp in sp100:
            if comp.tradingview_symbol == "":
                print(comp.company.name)

        # print(sp100_from_db_list)
        # print(sp100_from_tv_list)

        # number_sp100_companies = len(sp100_from_db_list)
        not_found_list = []
        for company in sp100_from_tv_list:
            if company in sp100_from_db_list:
                sp100_from_db_list.remove(company)
            else:
                not_found_list.append(company)

        if not_found_list:
            logging.critical(
                f"List of companies not found in SP100 Index: {not_found_list}"
            )
        if sp100_from_db_list:
            logging.critical(
                f"List of companies in database in SP100 Index but not in tradingview: {sp100_from_db_list}"
            )
