import os, sys, copy
from django.conf import settings

from corporates.models import Corporate
from django.core.management import BaseCommand
from corporates.models.ghg import GHGQuant

sys.path.append(os.path.join(settings.SERVER_BASE_DIR, "scripts"))
# from providers.msci_data import MSCIData

TOLERANCE = 0.05


def get_ghg_cdp(query):
    priority_order = ["cdp_2021", "cdp_2020"]
    for cdp_source in priority_order:
        cdp_query = query.filter(source=cdp_source)
        if cdp_query.exists():
            return cdp_query


def compare_build_final_ghg(company, reporting_year, public, cdp, tolerance):

    comments = ""

    categories = [
        "ghg_scope_1",
        "ghg_loc_scope_2",
        "ghg_mkt_scope_2",
        "ghg_purch_scope3",
        "ghg_capital_scope3",
        "ghg_fuel_energy_loc_scope3",
        "ghg_fuel_energy_mkt_scope3",
        "ghg_upstream_td_scope3",
        "ghg_waste_ops_scope3",
        "ghg_bus_travel_scope3",
        "ghg_commute_scope3",
        "ghg_up_leased_scope3",
        "ghg_downstream_td_scope3",
        "ghg_proc_sold_scope3",
        "ghg_use_sold_scope3",
        "ghg_eol_sold_scope3",
        "ghg_down_leased_scope3",
        "ghg_franchises_scope3",
        "ghg_investments_scope3",
        # "ghg_other_upstream_scope3",
        # "ghg_other_downstream_scope3",
    ]
    final_ghg = GHGQuant(company=company, reporting_year=reporting_year, source="final")
    for category in categories:
        if not getattr(cdp, category):
            selected_source = "public"
            setattr(final_ghg, category, getattr(public, category))
        elif not getattr(public, category):
            selected_source = "cdp"
            setattr(final_ghg, category, getattr(cdp, category))

        else:
            selected_ghg, selected_source = choose_ghg(
                cdp_ghg=getattr(cdp, category),
                public_ghg=getattr(public, category),
                tolerance=tolerance,
            )

            setattr(final_ghg, category, selected_ghg)
        comments += f"{category}:{selected_source} (Public: {getattr(public, category)}; CDP: {getattr(cdp, category)})\n "
    final_ghg.comments = comments
    return final_ghg


def choose_ghg(cdp_ghg, public_ghg, tolerance):

    if not cdp_ghg:
        return public_ghg, "public"
    elif not public_ghg:
        return cdp_ghg, "cdp"
    elif cdp_ghg > 0:
        diff = abs(cdp_ghg - public_ghg) / cdp_ghg
        if diff > tolerance:
            return public_ghg, "public"
        else:
            return cdp_ghg, "cdp"


def choose_final_ghg(public, cdp):
    if public.scope_123_loc > cdp.scope_123_loc:
        final_ghg = copy.deepcopy(public)
        final_ghg.comments = "Source: Public"
    else:
        final_ghg = copy.deepcopy(cdp)
        final_ghg.comments = "Source: CDP"
    return final_ghg


class Command(BaseCommand):
    def handle(self, *args, **options):

        final_ghg_records = []

        company_list = Corporate.objects.all()
        # company_list = [Corporate.objects.get(company_id=72)]
        reporting_years = ["2018", "2019", "2020", "2021"]

        for company in company_list:
            for reporting_year in reporting_years:
                query = GHGQuant.objects.filter(
                    company=company,
                    reporting_year=reporting_year,
                    source__in=["cdp_2020", "cdp_2021", "public"],
                ).order_by("-last_update")
                public_query = query.filter(source="public")
                cdp_query = get_ghg_cdp(query)

                if not cdp_query and not public_query:
                    continue

                if not cdp_query or not cdp_query.exists():
                    final_ghg = copy.deepcopy(public_query[0])
                    final_ghg.comments = "Source: Public"
                elif not public_query.exists():
                    final_ghg = copy.deepcopy(cdp_query[0])
                    final_ghg.comments = "Source: CDP"
                else:
                    final_ghg = choose_final_ghg(
                        public=public_query[0],
                        cdp=cdp_query[0],
                    )

                    # final_ghg = compare_build_final_ghg(
                    #     company=company,
                    #     reporting_year=reporting_year,
                    #     public=public_query[0],
                    #     cdp=cdp_query[0],
                    #     tolerance=TOLERANCE,
                    # )
                final_ghg.id = None  # in case of a full copy of a GHGQuant object, it guarantees that a new object will be created and saved in the database
                final_ghg.source = "final"
                final_ghg_records.append(final_ghg)

        filtered_final_ghg_records = filter(
            lambda v: not GHGQuant.objects.is_last_ghg_duplicate(v),
            final_ghg_records,
        )

        count = 0
        for record in filtered_final_ghg_records:
            record.save()
            count += 1
        print(f"Number of new records saved: {count}")
