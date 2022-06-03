from django.db import models
from corporates.models.corp import Corporate
from corporates.models.choices import Options


class SBTIScoreManager(models.Manager):
    def get_last_sbti_value(self, company):

        last_sbti_value = self.filter(company=company).order_by("-last_update", "-id")

        if last_sbti_value.exists():
            return last_sbti_value[0]

    def is_last_sbti_value_duplicate(self, sbti_value_to_test):

        last_sbti_value = self.get_last_sbti_value(
            company=sbti_value_to_test.company,
        )

        if not last_sbti_value:
            return False

        equality_test = (last_sbti_value.status, last_sbti_value.classification) == (
            sbti_value_to_test.status,
            sbti_value_to_test.classification,
        )

        if not equality_test:
            return False

        return True


class SBTI(models.Model):
    objects = SBTIScoreManager()

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
        return f"{self.company.name}- {self.status} {self.classification}"

    def get_new_sbti(self, company_id, status, classification):

        self.company = Corporate.objects.get(company_id=company_id)
        self.status = status
        self.classification = classification

        return self
