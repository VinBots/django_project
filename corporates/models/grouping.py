from django.db import models


class CorporateGroupingManager(models.Manager):
    def get_sp100_company_ids(self):
        return self.filter(primary_benchmark__name="SP100").values_list(
            "company__company_id", flat=True
        )


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
    all_industries_1 = models.ManyToManyField(
        "Industry_1", related_name="all_industries_1", blank=True
    )
    primary_industry_1 = models.ForeignKey(
        "Industry_1",
        related_name="primary_industry_1",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    ##############################################################
    all_activities = models.ManyToManyField(
        "Activity", related_name="all_activities", blank=True
    )
    primary_activity = models.ForeignKey(
        "Activity",
        related_name="primary_activity",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    ##############################################################
    all_sectors = models.ManyToManyField(
        "Sector", related_name="all_sectors", blank=True
    )
    primary_sector = models.ForeignKey(
        "Sector",
        related_name="primary_sector",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    ##############################################################
    all_industries_2 = models.ManyToManyField(
        "Industry_2", related_name="all_industries_2", blank=True
    )
    primary_industry_2 = models.ForeignKey(
        "Industry_2",
        related_name="primary_industry_2",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    ##############################################################
    all_benchmarks = models.ManyToManyField(
        "Benchmark", related_name="all_benchmarks", blank=True
    )
    primary_benchmark = models.ForeignKey(
        "Benchmark",
        related_name="primary_benchmark",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.company.name


class Country(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Industry_1(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Industry_1"
        verbose_name_plural = "Industries_1"

    def __str__(self):
        return self.name


class Industry_2(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Industry_2"
        verbose_name_plural = "Industries_2"

    def __str__(self):
        return self.name


class Activity(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.name


class Sector(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"

    def __str__(self):
        return self.name


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
