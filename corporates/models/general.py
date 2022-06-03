import pathlib

from django.db import models
from django.contrib.auth.models import User

from .choices import Options


def user_directory_path(instance, filename):

    if instance._meta.model.__name__ == "GeneralInfo":
        folder = "general2"

    filename = f"{folder}/{instance.year}_{instance.company.name}\
        _{instance.submitter.username}\
            {pathlib.Path(filename).suffix}"
    print(f"FILE TO SAVE: {filename}")
    return filename


class GeneralInfo(models.Model):

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE)
    submitter = models.ForeignKey(
        User,
        related_name="generalinfo_sub",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    verifier = models.ForeignKey(
        User,
        related_name="generalinfo_verif",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    last_update = models.DateTimeField(auto_now_add=True)
    document = models.CharField(
        verbose_name="Type of Documents",
        default=Options.DEFAULT_DOCUMENT,
        choices=Options.DOCUMENT_CHOICES,
        max_length=100,
        blank=False,
        null=True,
    )
    year = models.CharField(
        verbose_name="Year",
        default=Options.YEAR_DEFAULT_TARGET,
        choices=Options.YEAR_CHOICES,
        max_length=10,
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True, null=True)
    upload = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "General Info"

    def __str__(self):
        return f"{self.company.short_name}"

    def get_upload_fields(self):
        return [
            self.upload,
        ]

    @property
    def number_of_uploads(self):
        fields = self.get_upload_fields()
        return 1 - fields.count("")

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
                desc = f"{self.document}_{self.year}"
                dict = {"path": path, "desc": desc}
                uploads.append(dict)
        return uploads
