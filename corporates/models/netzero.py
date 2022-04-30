from django.db import models
from django.contrib.auth.models import User
from .choices import Options
import pathlib


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    folder = "netzero2"
    # FORMAT '[target_year]_[company_name]_[source]_[submitter]

    filename = f"{folder}/{instance.target_year}-{instance.company.name}_{pathlib.Path(filename).suffix}"
    return filename


class NetZero(models.Model):

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE, blank=True)

    submitter = models.ForeignKey(
        User,
        related_name="netzero_sub",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    verifier = models.ForeignKey(
        User,
        related_name="netzero_verif",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    update_date = models.DateField(auto_now=True)

    stated = models.CharField(
        choices=Options.YESNO,
        default=Options.NO,
        max_length=25,
        verbose_name="Did the company publicly commit to a net zero target by 2050?",
        blank=False,
        null=True,
    )
    coverage = models.CharField(
        verbose_name="What is the scope of this net zero target",
        choices=Options.SCOPE_OPTIONS,
        default=Options.SCOPE12_LOC,
        max_length=50,
        blank=False,
        null=False,
    )
    scope_3_coverage = models.CharField(
        verbose_name="Does the net zero target fully include all the scope 3 emissions (15 categories)?",
        choices=Options.COVERAGE_OPTIONS,
        default=Options.NOT_COVERED,
        max_length=50,
        blank=False,
        null=False,
    )

    target_year = models.CharField(
        verbose_name="What is the target year for reaching net zero?",
        help_text="Please fill in the target year only in case the company has not reached its net zero target yet",
        max_length=10,
        default=Options.YEAR_DEFAULT_VERIFICATION,
        choices=Options.YEAR_CHOICES,
        blank=True,
        null=True,
    )
    already_reached = models.CharField(
        choices=Options.YESNO,
        default=Options.NO,
        max_length=25,
        verbose_name="Did the company reach net zero?",
        blank=False,
        null=True,
    )
    ongoing = models.CharField(
        choices=Options.YESNO,
        max_length=25,
        verbose_name="Did the company commit to remain net zero in the future?",
        blank=True,
        null=True,
    )
    ongoing_coverage = models.CharField(
        verbose_name="What is the scope of this ongoing net zero commitment?",
        choices=Options.SCOPE_OPTIONS,
        default=Options.SCOPE12_LOC,
        max_length=50,
        blank=False,
        null=False,
    )

    ongoing_scope_3_coverage = models.CharField(
        verbose_name="Does the net zero target fully include all the scope 3 emissions (15 categories)?",
        choices=Options.COVERAGE_OPTIONS,
        default=Options.NOT_COVERED,
        max_length=50,
        blank=False,
        null=False,
    )

    year_since = models.CharField(
        verbose_name="What year did the company reach net zero?",
        help_text="Please fill in this field in case the company has already reached its net zero target, \
            For example, Google state that net zero was reached since 2007",
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
        verbose_name_plural = "Net Zero Targets"
        # ordering = ["update_date"]

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
                desc = f"{self.source.source} - {self.reporting_year}"
                dict = {"path": path, "desc": desc}
                uploads.append(dict)
        return uploads

    def __str__(self):
        return f"{self.company.short_name}-by {self.target_year}"
