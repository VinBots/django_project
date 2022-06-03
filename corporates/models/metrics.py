from django.db import models
from django.db.models import Avg

from corporates.models.grouping import CorporateGrouping
from corporates.models.grouping import GICS


class Investment(models.Model):

    EURO = "eur"
    USD = "usd"
    GBP = "gbp"

    CURRENCY_OPTIONS = [(EURO, "EUROS"), (USD, "USD"), (GBP, "GBP")]

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE)

    name = models.CharField(max_length=100, blank=False, null=False)
    last_update = models.DateTimeField(auto_now=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.CharField(
        max_length=5, choices=CURRENCY_OPTIONS, default=USD, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Investments"
        ordering = ["last_update"]

    def __str__(self):
        return f"{self.company.short_name}-{self.name}"


class StatsManager(models.Manager):
    def get_last_stats(self, stats, perimeter, year):
        query = self.filter(stats=stats, perimeter=perimeter, year=year).order_by(
            "-last_update", "-id"
        )
        if query.exists():
            return query[0]

    def is_last_stats_duplicate(self, stats_to_test):

        last_stats = self.get_last_stats(
            stats=stats_to_test.stats,
            perimeter=stats_to_test.perimeter,
            year=stats_to_test.year,
        )

        if not last_stats:
            return False

        comparable_fields = ["value"]

        for field in comparable_fields:
            equality_test = getattr(last_stats, field) == getattr(stats_to_test, field)
            # print(f"{getattr(last_stats, field)} == {getattr(stats_to_test, field)}")
            # print(
            #     f"{type(getattr(last_stats, field))} == {type(getattr(stats_to_test, field))}"
            # )
            if not equality_test:
                # print(f"FIELD {field} : {equality_test}")

                return False

        return True

    def calc_average_intensity(self, year):

        res = list(GHGMetrics.objects.aggregate(Avg("intensity")).values())[0]
        obj = Stats(year=year, stats="intensity_calculated", perimeter="all", value=res)
        return obj

    def calc_sector_intensity(self, year):

        obj_list = []

        sector_names = (
            GICS.objects.all()
            .distinct("sector_name")
            .values_list("sector_name", flat=True)
        )
        for sector_name in sector_names:
            corporates_in_sector = CorporateGrouping.objects.get_corporates_in_sector(
                sector_name
            )
            if sector_name:
                query = (
                    GHGMetrics.objects.filter(company__in=corporates_in_sector)
                    .all()
                    .aggregate(Avg("intensity"))
                )
                if query:
                    obj = Stats(
                        year=year,
                        stats="intensity_calculated",
                        perimeter=sector_name,
                        value=list(query.values())[0],
                    )
                    obj_list.append(obj)
        return obj_list

    def get_average_stats(self, year, stats):
        query = self.filter(year=year, stats=stats, perimeter="all")
        if query.exists() and query[0].value:
            return query[0].value

    def get_sector_stats(self, company, year, stats):
        sector_name = CorporateGrouping.objects.get_sector_name(company.company_id)
        query = self.filter(year=year, stats=stats, perimeter=sector_name)
        if query.exists() and query[0].value:
            return query[0].value


class Stats(models.Model):

    objects = StatsManager()

    id = models.BigAutoField(primary_key=True)
    last_update = models.DateTimeField(auto_now=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    stats = models.CharField(max_length=100, blank=True, null=True)
    perimeter = models.CharField(max_length=100, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Statistics"

    def __str__(self):
        if not self.value:
            value = "NA"
        else:
            value = str(int(self.value))

        return f"{self.stats}({self.perimeter}/{self.year}): {value}"


class CalcMetricsManager(models.Manager):
    def get_last_metrics(self, company, year, metrics):

        if isinstance(company, int):
            query = self.filter(
                company__company_id=company, year=year, metrics=metrics
            ).order_by("-last_update", "-id")
        else:
            query = self.filter(company=company, year=year, metrics=metrics).order_by(
                "-last_update", "-id"
            )

        if query.exists():
            return query[0]

    def is_last_metrics_duplicate(self, metrics_to_test):

        last_metrics = self.get_last_metrics(
            company=metrics_to_test.company,
            year=metrics_to_test.year,
            metrics=metrics_to_test.metrics,
        )

        if not last_metrics:
            return False

        comparable_fields = ["method", "value", "meta_data"]

        for field in comparable_fields:
            equality_test = getattr(last_metrics, field) == getattr(
                metrics_to_test, field
            )
            # print(
            #     f"{getattr(last_metrics, field)} == {getattr(metrics_to_test, field)}"
            # )
            # print(
            #     f"{type(getattr(last_metrics, field))} == {type(getattr(metrics_to_test, field))}"
            # )
            if not equality_test:
                # print(f"FIELD {field} : {equality_test}")

                return False

        return True


class CalcMetrics(models.Model):

    objects = CalcMetricsManager()

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    metrics = models.CharField(max_length=100, blank=True, null=True)
    method = models.CharField(max_length=100, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    meta_data = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = "Calculated Metrics"

    def __str__(self):
        return f"{self.company.name} - {self.metrics} - {self.year}: {self.value}"


class GHGMetricsManager(models.Manager):
    def get_last_metrics(self, company, year):

        if isinstance(company, int):
            query = self.filter(company__company_id=company, year=year).order_by(
                "-last_update", "-id"
            )
        else:
            query = self.filter(company=company, year=year).order_by(
                "-last_update", "-id"
            )

        if query.exists():
            return query[0]

    def is_last_metrics_duplicate(self, metrics_to_test):

        last_metrics = self.get_last_metrics(
            company=metrics_to_test.company, year=metrics_to_test.year
        )

        if not last_metrics:
            return False

        comparable_fields = [
            "intensity",
            "s3_intensity",
            "s3_to_s1s2_ratio",
        ]

        for field in comparable_fields:
            equality_test = getattr(last_metrics, field) == getattr(
                metrics_to_test, field
            )
            # print(
            #     f"{getattr(last_metrics, field)} == {getattr(metrics_to_test, field)}"
            # )
            # print(
            #     f"{type(getattr(last_metrics, field))} == {type(getattr(metrics_to_test, field))}"
            # )
            if not equality_test:
                # print(f"FIELD {field} : {equality_test}")

                return False

        return True


class GHGMetrics(models.Model):

    objects = GHGMetricsManager()

    id = models.BigAutoField(primary_key=True)
    last_update = models.DateTimeField(auto_now=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE, blank=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    intensity = models.FloatField(blank=True, null=True)
    s3_intensity = models.FloatField(blank=True, null=True)
    s3_to_s1s2_ratio = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.company.name + "-" + self.year

    class Meta:
        verbose_name_plural = "GHG Metrics"
