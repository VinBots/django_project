import logging

from corporates.models.external_sources.tradingview import Tradingview
from corporates.models.grouping import CorporateGrouping
from corporates.models.choices import Options
from corporates.utilities import get_last_x_years
from corporates.models.metrics import Stats, CalcMetrics
from corporates.management.utilities import *


class TotalCarbonEmissions:
    def __init__(self, company_id, year):
        self.company_id = company_id
        self.company = Corporate.objects.get(company_id=self.company_id)
        self.year = year
        self.preceding_year = str(int(self.year) - 1)
        self.methods_by_priority = self.get_methods_by_priority()
        self.calc_metrics = CalcMetrics(
            company=self.company,
            year=self.year,
            metrics="total_ghg_estimate",
            method=None,
            value=None,
            meta_data={},
        )
        self.init()

    def init(self):
        self.revenue = Tradingview.objects.get_value(
            company=self.company, account="Total revenue", period=self.year
        )
        self.scope_12_best = get_s1s2_best(self.company, self.year)
        self.scope_3_best = get_s3_best(self.company, self.year)
        total = [self.scope_12_best, self.scope_3_best]
        self.total_reported = sum(list(filter(bool, total)))

    def get_methods_by_priority(self):

        return [
            self.total_co2_as_reported,
            self.total_co2_estimate_with_s1s2_fully_reported,
            self.total_co2_estimate_with_prec_year_intensity,
            self.total_co2_estimate_with_most_recent_intensity,
            self.total_co2_estimate_with_sector_s3_intensity_manual,
            self.total_co2_estimate_with_sector_s3_intensity_calculated,
            self.total_co2_estimate_with_sector_intensity_manual,
            self.total_co2_estimate_with_sector_intensity_calculated,
            self.no_method,
        ]

    def calculate(self):

        for method in self.methods_by_priority:
            self.meta_id = self.meta = {}
            result = method()
            if self.meta_id:
                self.calc_metrics.meta_data.update({self.meta_id: self.meta})

            if result:
                self.calc_metrics.method = result.get("method", "")
                self.calc_metrics.value = result.get("value", None)
                self.apply_minimum_value()
                self.convert_into_integer()
                break

    def apply_minimum_value(self):
        tests = [
            self.total_reported,
            self.calc_metrics.value,
            self.total_reported > self.calc_metrics.value,
        ]
        if all(tests):
            self.calc_metrics.value = self.total_reported
            self.calc_metrics.method = (
                "as_reported"  # f"as_reported > {self.calc_metrics.method}"
            )

    def convert_into_integer(self):
        if self.calc_metrics.value:
            self.calc_metrics.value = int(round(self.calc_metrics.value))

    def save(self):
        if (
            self.calc_metrics.value
            and not CalcMetrics.objects.is_last_metrics_duplicate(self.calc_metrics)
        ):
            self.calc_metrics.save()

    def total_co2_as_reported(self):

        self.meta_id = "total_co2_as_reported"
        self.meta = {}

        if is_ghg_fully_reported(self.company, [self.year]):
            self.meta.update({"is_ghg_fully_reported": "yes"})

            if self.scope_12_best and self.scope_3_best:
                self.meta.update({"scope_12_best and scope_3_best": "yes"})
                self.meta.update(
                    {
                        "scope_12_best": self.scope_12_best,
                        "scope_3_best": self.scope_3_best,
                    }
                )
                total_co2_estimate = self.scope_12_best + self.scope_3_best

                return {"method": Options.AS_REPORTED, "value": total_co2_estimate}
            else:
                self.meta.update({"scope_12_best and scope_3_best": "no"})
        else:
            self.meta.update({"is_ghg_fully_reported": "no"})

    def total_co2_estimate_with_s1s2_fully_reported(self):

        self.meta_id = "total_co2_estimate_with_s1s2_fully_reported"
        self.meta = {}

        if is_s1s2_fully_reported(self.company, self.year):
            self.meta.update({"is_s1s2_fully_reported": "yes"})

            scope_3_estimate = (
                self.get_s3_estimate_based_on_preceding_year_with_s1s2_fully_reported()
            )
            if scope_3_estimate:
                self.meta.update(
                    {
                        "is_get_s3_estimate_based_on_preceding_year_with_s1s2_fully_reported": "yes"
                    }
                )
                self.meta.update(
                    {
                        "scope_3_estimate_based_on_preceding_year_with_s1s2_fully_reported": scope_3_estimate
                    }
                )
                total_co2_estimate = self.scope_12_best + scope_3_estimate
                return {
                    "method": Options.S3_PRECEDING_YEAR,
                    "value": total_co2_estimate,
                }

    def get_s3_estimate_based_on_preceding_year_with_s1s2_fully_reported(self):

        tests = [
            is_ghg_fully_reported(self.company, [self.preceding_year]),
            is_attribute(self.company, self.preceding_year, "s3_to_s1s2_ratio"),
            is_attribute(self.company, self.preceding_year, "s3_intensity"),
        ]

        if all(tests):
            self.meta.update({"is_all(tests)": "yes"})
            self.meta.update({"tests": tests})

            s3_to_s1s2_ratio_preceding_year = get_metrics_attribute(
                self.company, self.preceding_year, "s3_to_s1s2_ratio"
            )
            s3_intensity_preceding_year = get_metrics_attribute(
                self.company, self.preceding_year, "s3_intensity"
            )
            self.meta.update(
                {
                    "s3_to_s1s2_ratio_preceding_year": s3_to_s1s2_ratio_preceding_year,
                    "s3_intensity_preceding_year": s3_intensity_preceding_year,
                }
            )
            result = self.get_s3_estimate_based_on_preceding_year(
                s3_to_s1s2_ratio_preceding_year,
                s3_intensity_preceding_year,
            )
            if result:
                self.meta.update({"is_get_s3_estimate_based_on_preceding_year": "yes"})
                return result
        else:
            self.meta.update({"is_all(tests)": "no"})
            self.meta.update({"tests": tests})

    def total_co2_estimate_with_prec_year_intensity(self):

        self.meta_id = "total_co2_estimate_with_prec_year_intensity"
        self.meta = {}

        tests = [
            is_ghg_fully_reported(self.company, [self.preceding_year]),
            is_attribute(self.company, self.preceding_year, "intensity"),
            self.revenue,
        ]

        if all(tests):
            self.meta.update({"is_all(tests)": "yes"})
            self.meta.update({"tests": tests})

            prec_year_intensity = get_metrics_attribute(
                self.company, self.preceding_year, "intensity"
            )
            total_co2_estimate = self.revenue * prec_year_intensity / 1e6

            # estimates = [res, self.total_reported]
            # total_co2_estimate = max(list(filter(bool, estimates)))

            self.meta.update(
                {"revenue": self.revenue, "prec_year_intensity": prec_year_intensity}
            )
            return {
                "method": Options.PRECEDING_YEAR_INTENSITY,
                "value": total_co2_estimate,
            }

    def total_co2_estimate_with_most_recent_intensity(self):

        self.meta_id = "total_co2_estimate_with_most_recent_intensity"
        self.meta = {}

        res_list = []
        intensity_list = []
        years = get_last_x_years(x=3)

        for recent_year in years:

            tests = [
                is_ghg_fully_reported(self.company, [recent_year]),
                is_attribute(self.company, recent_year, "intensity"),
                self.revenue,
            ]
            if all(tests):

                intensity = get_metrics_attribute(
                    self.company, recent_year, "intensity"
                )
                intensity_list.append(intensity)
                res_list.append(self.revenue * intensity / 1e6)

        if res_list:
            self.meta.update(
                {
                    "is_res_list": "yes",
                    "intensity_list": intensity_list,
                    "res_list": res_list,
                }
            )
            total_co2_estimate = max(res_list)
            # estimates = [res, self.total_reported]
            # total_co2_estimate = max(list(filter(bool, estimates)))

            return {
                "method": Options.RECENT_YEAR_INTENSITY,
                "value": total_co2_estimate,
            }

    def total_co2_estimate_with_sector_s3_intensity_manual(self):
        self.meta_id = "total_co2_estimate_with_sector_s3_intensity_manual"
        self.meta = {}
        sector_name = CorporateGrouping.objects.get_sector_name(self.company.company_id)
        query = Stats.objects.filter(
            perimeter=sector_name,
            stats="s3_intensity_manual",
        ).order_by("-year", "-last_update")

        tests = [
            is_s1s2_fully_reported(self.company, self.year),
            query.exists() and query[0].value,
            self.scope_12_best,
            self.revenue,
        ]
        if all(tests):
            self.meta.update({"is_all(tests)": "yes"})
            self.meta.update({"tests": tests})

            s3_intensity = query[0].value
            self.meta.update(
                {
                    "scope_12_best": self.scope_12_best,
                    "revenue": self.revenue,
                    "s3_intensity": s3_intensity,
                }
            )
            total_co2_estimate = self.scope_12_best + self.revenue * s3_intensity
            return {
                "method": Options.RECENT_YEAR_INTENSITY,
                "value": total_co2_estimate,
            }

    def total_co2_estimate_with_sector_s3_intensity_calculated(self):

        self.meta_id = "total_co2_estimate_with_sector_s3_intensity_calculated"
        self.meta = {}

        if not self.scope_12_best:
            return

        sector_s3_intensity = Stats.objects.get_sector_stats(
            self.company, self.year, "s3_intensity"
        )
        sector_s3_to_s1s2_ratio = Stats.objects.get_sector_stats(
            self.company, self.year, "s3_to_s1s2_ratio"
        )

        tests = [sector_s3_intensity, sector_s3_to_s1s2_ratio, self.revenue]
        if all(tests):

            self.meta.update({"is_all(tests)": "yes"})
            self.meta.update({"tests": tests})

            estimate_sector_s3_intensity = self.revenue * sector_s3_intensity / 1e6
            estimate_sector_s3_to_s1s2_ratio = (
                sector_s3_to_s1s2_ratio * self.scope_12_best
            )
            self.meta.update(
                {
                    "estimate_sector_s3_intensity": estimate_sector_s3_intensity,
                    "estimate_sector_s3_to_s1s2_ratio": estimate_sector_s3_to_s1s2_ratio,
                }
            )
            total_co2_estimate = self.scope_12_best + max(
                estimate_sector_s3_intensity, estimate_sector_s3_to_s1s2_ratio
            )

            return {
                "method": Options.MAX_SECTOR_S3_INTENSITY_S3_to_S1S2_RATIO,
                "value": total_co2_estimate,
            }
        elif sector_s3_intensity and self.revenue:
            self.meta.update({"is_all(tests)": "no"})
            self.meta.update({"tests": tests})

            estimate_sector_s3_intensity = self.revenue * sector_s3_intensity / 1e6
            self.meta.update(
                {
                    "estimate_sector_s3_intensity": estimate_sector_s3_intensity,
                }
            )
            total_co2_estimate = self.scope_12_best + estimate_sector_s3_intensity
            return {
                "method": Options.SECTOR_S3_INTENSITY,
                "value": total_co2_estimate,
            }
        elif sector_s3_to_s1s2_ratio and self.revenue:
            estimate_sector_s3_to_s1s2_ratio = (
                sector_s3_to_s1s2_ratio * self.scope_12_best
            )
            self.meta.update(
                {
                    "estimate_sector_s3_to_s1s2_ratio": estimate_sector_s3_to_s1s2_ratio,
                }
            )
            total_co2_estimate = self.scope_12_best + estimate_sector_s3_to_s1s2_ratio
            return {
                "method": Options.SECTOR_S3_to_S1S2_RATIO,
                "value": total_co2_estimate,
            }

    def total_co2_estimate_with_sector_intensity_manual(self):
        self.meta_id = "total_co2_estimate_with_sector_intensity_manual"
        self.meta = {}

        sector_name = CorporateGrouping.objects.get_sector_name(self.company.company_id)
        query = Stats.objects.filter(
            perimeter=sector_name,
            stats="intensity_manual",
        ).order_by("-year", "-last_update")

        tests = [query.exists() and query[0].value, self.revenue]
        if all(tests):
            self.meta.update({"is_all(tests)": "yes"})
            self.meta.update({"tests": tests})
            intensity_manual = query[0].value
            self.meta.update(
                {"intensity_manual": intensity_manual, "revenue": self.revenue}
            )

            total_co2_estimate = self.revenue * intensity_manual / 1e6
            return {
                "method": Options.SECTOR_INTENSITY_MANUAL,
                "value": total_co2_estimate,
            }

    def total_co2_estimate_with_sector_intensity_calculated(self):
        self.meta_id = "total_co2_estimate_with_sector_intensity_calculated"
        self.meta = {}

        sector_intensity = Stats.objects.get_sector_stats(
            self.company, self.year, "intensity_calculated"
        )

        tests = [sector_intensity, self.revenue]

        if all(tests):
            self.meta.update({"is_all(tests)": "yes"})
            self.meta.update({"tests": tests})
            self.meta.update(
                {
                    "sector_intensity": sector_intensity,
                    "revenue": self.revenue,
                }
            )
            method = Options.SECTOR_INTENSITY_CALC
            res = self.revenue * sector_intensity / 1e6
            if res:
                return {"method": method, "value": res}
        else:
            self.meta.update(
                {
                    "sector_intensity": sector_intensity,
                    "revenue": self.revenue,
                }
            )

    def get_s3_estimate_based_on_preceding_year(
        self,
        s3_to_s1s2_ratio_preceding_year,
        s3_intensity_preceding_year,
    ):

        if not self.scope_12_best:
            return
        scope_3_estimate_1 = s3_to_s1s2_ratio_preceding_year * self.scope_12_best

        scope_3_estimate_2 = self.revenue * s3_intensity_preceding_year / 1e6

        return max(scope_3_estimate_1, scope_3_estimate_2)

    def no_method(self):
        logging.critical(
            f"Carbon emissions could not be estimated for {self.company.name} and year {self.year}. meta_data: {self.calc_metrics.meta_data}"
        )
        return {"method": "no method", "value": self.total_reported}
