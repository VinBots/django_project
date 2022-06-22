from django.db import models
from django.contrib.auth.models import User
from .choices import Options
import pathlib


def user_directory_path(instance, filename):
    folder = "verification"
    filename_str = f"{folder}/{instance.company.name}_{instance.reporting_year}{pathlib.Path(filename).suffix}"
    return filename_str


class Verification(models.Model):

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE, blank=True)

    submitter = models.ForeignKey(
        User, related_name="verif_sub", blank=True, null=True, on_delete=models.CASCADE
    )
    verifier = models.ForeignKey(
        User,
        related_name="verif_verif",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    last_update = models.DateTimeField(auto_now=True)

    scope12_reporting_2_years = models.CharField(
        verbose_name="At least the last 2 years of Scope 1-2 emissions are provided",
        choices=Options.YESNO,
        default=Options.YES,
        max_length=50,
        blank=False,
        null=True,
    )
    scope12_reporting_completeness = models.CharField(
        verbose_name="Scope 1-2 reported company-wide",
        choices=Options.COVERAGE_OPTIONS,
        default=Options.FULL,
        max_length=50,
        blank=False,
        null=True,
    )

    scope12_verification_completeness = models.CharField(
        verbose_name="How much of scope 1-2 emissions are verified by a 3rd-party?",
        choices=Options.COVERAGE_OPTIONS,
        default=Options.FULL,
        max_length=50,
        blank=False,
        null=True,
    )
    scope12_assurance_type = models.CharField(
        verbose_name="What is the level of assurance (provided by a 3rd-party) for scope 1-2 emissions?",
        choices=Options.ASSURANCE_TYPE_OPTIONS,
        default=Options.LIMITED,
        max_length=50,
        blank=False,
        null=True,
    )

    scope3_reporting_completeness = models.CharField(
        verbose_name="How much of scope 3 emissions are reported?",
        choices=Options.COVERAGE_OPTIONS,
        default=Options.PARTLY,
        max_length=20,
        blank=False,
        null=True,
    )

    scope3_verification_completeness = models.CharField(
        verbose_name="How much of scope 3 emissions are verified by a 3rd-party?",
        choices=Options.COVERAGE_OPTIONS,
        default=Options.NOT_COVERED,
        max_length=50,
        blank=False,
        null=True,
    )

    scope3_assurance_type = models.CharField(
        verbose_name="What is the level of assurance (provided by a 3rd-party) for scope 3 emissions?",
        choices=Options.ASSURANCE_TYPE_OPTIONS,
        default=Options.NO_ASSURANCE,
        max_length=50,
        blank=False,
        null=True,
    )

    reporting_year = models.CharField(
        verbose_name="Please select the current reporting year",
        max_length=10,
        default=Options.YEAR_DEFAULT_VERIFICATION,
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
        verbose_name_plural = "Verifications"
        # ordering = ["last_update"]

    def get_upload_fields(self):
        return [
            self.upload_1,
            self.upload_2,
            self.upload_3,
            self.upload_4,
            self.upload_5,
        ]

    @property
    def number_of_uploads(self):
        fields = self.get_upload_fields()
        empty_fields_count = fields.count("") + fields.count(None)
        return 5 - empty_fields_count

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
                desc = f"Disclosures/Verification_{self.reporting_year}"
                dict = {"path": path, "desc": desc}
                uploads.append(dict)
        return uploads

    def __str__(self):
        return f"{self.company.short_name}-{self.reporting_year}"
