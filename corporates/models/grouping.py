import logging

from django.db import models


class CorporateGroupingManager(models.Manager):
    def get_sp100_company_ids(self):
        return self.filter(primary_benchmark__name="SP100").values_list(
            "company__company_id", flat=True
        )

    def get_sector_name(self, company_id):
        query = self.filter(company__company_id=company_id)
        if (
            not query.exists()
            or not query.values_list("gics_sub_industry_name__sector_name")[0][0]
        ):
            logging.warning(
                f"No gics_sub_industry_name was found for company with company_id = {company_id}"
            )
            return
        return query.values_list("gics_sub_industry_name__sector_name")[0][0]

    def get_corporates_in_sector(self, sector_name):
        sub_industry_in_sector = GICS.objects.filter(sector_name=sector_name)
        return self.filter(
            gics_sub_industry_name__in=sub_industry_in_sector
        ).values_list("company", flat=True)


class CorporateGrouping(models.Model):
    """
    A Grouping represents a higher-level group for analysis purpose (e.g. aggregation)
    """

    objects = CorporateGroupingManager()

    id = models.BigAutoField(primary_key=True)

    company = models.OneToOneField(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )

    ##############################################################
    # all_industries_1 = models.ManyToManyField(
    #     "Industry_1", related_name="all_industries_1", blank=True
    # )
    # primary_industry_1 = models.ForeignKey(
    #     "Industry_1",
    #     related_name="primary_industry_1",
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE,
    # )
    ##############################################################
    # all_activities = models.ManyToManyField(
    #     "Activity", related_name="all_activities", blank=True
    # )
    # primary_activity = models.ForeignKey(
    #     "Activity",
    #     related_name="primary_activity",
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE,
    # )
    ##############################################################
    # all_sectors = models.ManyToManyField(
    #     "Sector", related_name="all_sectors", blank=True
    # )
    gics_sub_industry_name = models.ForeignKey(
        "GICS",
        related_name="GICS",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    # ##############################################################
    # all_industries_2 = models.ManyToManyField(
    #     "Industry_2", related_name="all_industries_2", blank=True
    # )
    # primary_industry_2 = models.ForeignKey(
    #     "Industry_2",
    #     related_name="primary_industry_2",
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE,
    # )
    # ##############################################################
    # all_benchmarks = models.ManyToManyField(
    #     "Benchmark", related_name="all_benchmarks", blank=True
    # )
    primary_benchmark = models.ForeignKey(
        "Benchmark",
        related_name="primary_benchmark",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.company.name


# class Country(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=250, unique=True)

#     class Meta:
#         verbose_name = "Country"
#         verbose_name_plural = "Countries"

#     def __str__(self):
#         return self.name


# class Industry_1(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=250, unique=True)
#     description = models.TextField(blank=True, null=True)

#     class Meta:
#         verbose_name = "Industry_1"
#         verbose_name_plural = "Industries_1"

#     def __str__(self):
#         return self.name


# class Industry_2(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=250, unique=True)
#     description = models.TextField(blank=True, null=True)

#     class Meta:
#         verbose_name = "Industry_2"
#         verbose_name_plural = "Industries_2"

#     def __str__(self):
#         return self.name


# class Activity(models.Model):
#     id = models.BigAutoField(primary_key=True)

#     name = models.CharField(max_length=250, unique=True)
#     description = models.TextField(blank=True, null=True)

#     class Meta:
#         verbose_name = "Activity"
#         verbose_name_plural = "Activities"

#     def __str__(self):
#         return self.name


class GICS(models.Model):
    id = models.BigAutoField(primary_key=True)

    sub_industry_name = models.CharField(max_length=250, unique=True)
    industry_name = models.CharField(max_length=250)
    industry_group_name = models.CharField(max_length=250)
    sector_name = models.CharField(max_length=250)

    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "GICS sector"

    def __str__(self):
        return f"{self.sub_industry_name} / {self.sector_name}"


class Benchmark(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    web_URL = models.URLField("Web Address")

    class Meta:
        verbose_name = "Benchmark"
        verbose_name_plural = "Benchmarks"

    def __str__(self):
        return self.name
