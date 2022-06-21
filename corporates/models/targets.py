import pathlib
import copy

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from .choices import Options

from corporates.models import GHGQuant


def user_directory_path(instance, filename):
    folder = "target"
    filename_str = f"{folder}/{instance.company.name}_{instance.scope_coverage}_{pathlib.Path(filename).suffix}"
    return filename_str


def remove_null_values(valid_target):
    cleaned_valid_target = copy.deepcopy(valid_target)
    for field, values in valid_target.items():
        if not values:
            cleaned_valid_target.pop(field)
    return cleaned_valid_target


class CustomManager(models.Manager):
    def get_earliest_highest(
        self,
        company_id,
        valid_target=None,
    ):
        queryset = self.filter(
            Q(company__company_id=company_id) & Q(reduction_obj__gt=0)
        ).order_by("target_year", "reduction_obj")

        if valid_target:
            valid_target = remove_null_values(valid_target)
            queryset = queryset.filter(Q(**valid_target))

        return queryset


class TargetQuant(models.Model):

    objects = CustomManager()
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey("Corporate", blank=True, on_delete=models.CASCADE)

    submitter = models.ForeignKey(
        User, related_name="target_sub", blank=True, null=True, on_delete=models.CASCADE
    )
    verifier = models.ForeignKey(
        User,
        related_name="target_verif",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    last_update = models.DateTimeField(auto_now=True)

    type = models.CharField(
        verbose_name="What is the type of target?",
        help_text="",  # Options.TARGET_DEFINITIONS,
        max_length=20,
        choices=Options.TARGET_TYPES_OPTIONS,
        default=Options.GROSS_ABSOLUTE,
        blank=False,
        null=True,
    )

    source = models.CharField(
        max_length=20, choices=Options.TARGET_SOURCES_OPTIONS, default=Options.PUBLIC
    )

    scope_coverage = models.CharField(
        verbose_name="Scope Coverage",
        max_length=10,
        choices=Options.SCOPE_OPTIONS,
        default=Options.SCOPE12_LOC,
        blank=False,
        null=True,
    )
    scope_3_coverage = models.CharField(
        verbose_name="Does the net zero target fully include all the scope 3 emissions (15 categories)?",
        max_length=10,
        choices=Options.COVERAGE_OPTIONS,
        default=Options.NOT_COVERED,
        blank=False,
        null=True,
    )

    start_year = models.CharField(
        verbose_name="Start Year",
        max_length=10,
        default=Options.YEAR_DEFAULT_TARGET,
        choices=Options.YEAR_CHOICES,
        blank=True,
        null=True,
    )
    reduction_obj = models.FloatField(
        verbose_name="Reduction objectives (in %)",
        help_text="A positive number is a decrease of emissions, i.e. for a 20% reduction, input 20. A negative number is an increase of emissions",
        blank=True,
        null=True,
    )
    base_year = models.CharField(
        verbose_name="Base Year",
        default=Options.YEAR_DEFAULT_TARGET,
        max_length=10,
        choices=Options.YEAR_CHOICES,
        blank=True,
        null=True,
    )
    baseline = models.PositiveIntegerField(
        verbose_name="Baseline Emissions",
        help_text="Emissions (in Mt CO2e) in base year",
        blank=True,
        null=True,
    )
    auto_baseline = models.FloatField(
        verbose_name="Automatically-calculated baseline emissions",
        help_text="Emissions (in Mt CO2e) in base year",
        blank=True,
        null=True,
    )
    target_year = models.CharField(
        verbose_name="Target Year",
        max_length=10,
        default=Options.YEAR_DEFAULT_TARGET,
        choices=Options.YEAR_CHOICES,
        blank=True,
        null=True,
    )

    upload_1 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_2 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_3 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_4 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_5 = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    class Meta:
        verbose_name = "Target Quantitative Data"
        verbose_name_plural = "Target Quantitative Data"

    def get_upload_fields(self):
        return [
            self.upload_1,
            self.upload_2,
            self.upload_3,
            self.upload_4,
            self.upload_5,
        ]

    @property
    def get_categories(self):
        fields = [
            self.cov_s1,
            self.cov_s2_loc,
            self.cov_s2_mkt,
            self.cov_s3_1,
            self.cov_s3_2,
        ]
        return fields

    @property
    def number_of_uploads(self):
        fields = self.get_upload_fields()
        return 5 - fields.count("")

    @property
    def size_of_uploads(self):
        file_size = 0
        fields = self.get_upload_fields()
        for field in fields:
            if field:
                file_size += field.file.size
        return f"{file_size / 1000000:.2f}Mb"

    @property
    def get_uploads(self):
        uploads = []
        fields = self.get_upload_fields()
        for field in fields:
            if field:
                path = f"/download/{field}"
                desc = f"Targets_{self.target_year}"
                dict = {"path": path, "desc": desc}
                uploads.append(dict)
        return uploads

    # @property
    # def get_fl_red_by_year(self):

    #     last_reporting_year_ghg = GHGQuant.objects.get_last_reporting_year(
    #         self.company_id
    #     )
    #     last_year = "2020"
    #     target_ghg = self.baseline * (1 - (self.reduction_obj / 100))
    #     fl_reduction = (1 - (target_ghg / last_reporting_year_ghg)) * 100
    #     period = int(self.target_year) - int(last_year)
    #     meta = {
    #         "Baseline": self.baseline,
    #         "Reduction Objectives": self.reduction_obj,
    #         "Target emissions": target_ghg,
    #         "Target Year": self.target_year,
    #         "Error msg": "",
    #     }
    #     fl_red_by_year = fl_reduction / period
    #     return fl_red_by_year, meta

    def fl_red_data_check(self, last_reporting_year):

        test1 = {
            "desc": "Reduction objectives (in percent) is a positive number",
            "test": (self.reduction_obj is not None and self.reduction_obj > 0),
        }

        test2 = {
            "desc": "Target year exists and is later than the last reporting year",
            "test": self.target_year is not None
            and (int(self.target_year) > int(last_reporting_year)),
        }
        test3 = {
            "desc": "Baseline emissions is a positive number",
            "test": (self.baseline is not None and self.baseline > 0)
            or (self.auto_baseline is not None and self.auto_baseline > 0),
        }
        all_tests = test1, test2, test3
        test_result = all([case["test"] for case in all_tests])

        return test_result, all_tests

    def get_auto_baseline(self):

        result = GHGQuant.objects.get_ghg(
            self.company.company_id, self.scope_coverage, self.base_year
        )
        self.auto_baseline = result
        self.save()

    def get_baseline(self):

        if all([not self.baseline, not self.auto_baseline]):
            return None
        elif not self.baseline:
            return self.auto_baseline
        else:
            return self.baseline

    def __str__(self):
        return f"{self.company.short_name} - reduction: {self.reduction_obj}% \
             by {self.target_year} vs. {self.base_year} "

    # intensity_metric = models.ForeignKey(
    #     "IntensityMetrics",
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
    # cov_s1 = models.CharField(
    #     verbose_name="Scope 1",
    #     max_length=10,
    #     choices=Options.COVERAGE_OPTIONS,
    #     default=Options.FULL,
    # )

    # cov_s2_mkt = models.CharField(
    #     verbose_name="Scope 2 (market-based)",
    #     max_length=10,
    #     choices=Options.COVERAGE_OPTIONS,
    #     default=Options.FULL,
    # )

    # cov_s2_loc = models.CharField(
    #     verbose_name="Scope 2 (location-based)",
    #     max_length=10,
    #     choices=Options.COVERAGE_OPTIONS,
    #     default=Options.FULL,
    # )

    # cov_s3 = models.CharField(
    #     verbose_name="Scope 3",
    #     max_length=10,
    #     choices=Options.COVERAGE_OPTIONS,
    #     default=Options.NOT_COVERED,
    # )
    # cov_s3_1 = models.CharField(
    #     verbose_name="Scope 3 - Category 1",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_2 = models.CharField(
    #     verbose_name="Scope 3 - Category 2",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_3 = models.CharField(
    #     verbose_name="Scope 3 - Category 3",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_4 = models.CharField(
    #     verbose_name="Scope 3 - Category 4",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_5 = models.CharField(
    #     verbose_name="Scope 3 - Category 5",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_6 = models.CharField(
    #     verbose_name="Scope 3 - Category 6",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_7 = models.CharField(
    #     verbose_name="Scope 3 - Category 7",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_8 = models.CharField(
    #     verbose_name="Scope 3 - Category 8",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_9 = models.CharField(
    #     verbose_name="Scope 3 - Category 9",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_10 = models.CharField(
    #     verbose_name="Scope 3 - Category 10",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_11 = models.CharField(
    #     verbose_name="Scope 3 - Category 11",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_12 = models.CharField(
    #     verbose_name="Scope 3 - Category 12",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_13 = models.CharField(
    #     verbose_name="Scope 3 - Category 13",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_14 = models.CharField(
    #     verbose_name="Scope 3 - Category 14",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
    # cov_s3_15 = models.CharField(
    #     verbose_name="Scope 3 - Category 15",
    #     max_length=10,
    #     choices=COVERAGE_OPTIONS,
    #     default=FULL,
    # )
