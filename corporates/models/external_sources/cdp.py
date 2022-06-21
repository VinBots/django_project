from pyexpat import model
from django.db import models
from ..choices import Options
from django.contrib.auth.models import User
import pathlib


def user_directory_path(instance, filename):
    folder = "cdp"
    filename = f"{folder}/{instance.questionnaire_year}_{instance.company.name}_{pathlib.Path(filename).suffix}"
    return filename


class CDP(models.Model):

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE)

    submitter = models.ForeignKey(
        User, related_name="cdp_sub", blank=True, null=True, on_delete=models.CASCADE
    )
    verifier = models.ForeignKey(
        User,
        related_name="cdp_verif",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    last_update = models.DateTimeField(auto_now=True)

    questionnaire_year = models.CharField(
        verbose_name="Please select the reference year for the CDP Climate Change Questionnaire",
        help_text="Note it can be different from the reporting year",
        max_length=10,
        default=Options.YEAR_DEFAULT_CDP,
        choices=Options.YEAR_CHOICES,
        blank=True,
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

    made_public = models.BooleanField(
        verbose_name="CDP Climate Change Questionnaire made publicly-available",
        default=False,
        blank=True,
        null=True,
    )
    score = models.CharField(
        verbose_name="CDP Score",
        choices=Options.CDP_SCORE_OPTIONS,
        default=Options.CDP_SCORE_DEFAULT,
        max_length=10,
        null=True,
        blank=True,
    )
    comments = models.TextField(
        verbose_name="Comments",
        null=True,
        blank=True,
    )

    upload_1 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_2 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_3 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_4 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_5 = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "CDP"

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
                desc = "desc"  # f"{self.source} - {self.reporting_year}"
                dict = {"path": path, "desc": desc}
                uploads.append(dict)
        return uploads

    def __str__(self):
        return f"{self.company.short_name}"
