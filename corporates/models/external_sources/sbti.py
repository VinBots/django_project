from django.db import models
from corporates.models.choices import Options


class SBTI(models.Model):

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )
    date = models.DateField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=Options.NT_STATUS_OPTIONS, max_length=100, blank=True, null=True
    )

    classification = models.CharField(
        choices=Options.NT_CLASSIFICATION_OPTIONS, max_length=100, blank=True, null=True
    )

    class Meta:
        verbose_name = "SBTi data"
        verbose_name_plural = "SBTi data"

    def __str__(self):
        return self.company.name + "-" + str(self.date)
