from django.db import models
from corporates.models.corp import Corporate
from corporates.models.choices import Options


class MSCIScoreManager(models.Manager):
    def get_last_msci_value(self, company):

        if isinstance(company, int):
            query = self.filter(company__company_id=company).order_by(
                "-last_update", "-id"
            )
        else:
            query = self.filter(company=company).order_by("-last_update", "-id")

        if query.exists():
            return query[0]

    def is_last_msci_value_duplicate(self, msci_value_to_test):

        last_msci_value = self.get_last_msci_value(
            company=msci_value_to_test.company,
        )

        if not last_msci_value:
            return False

        comparable_fields = [
            "ITR",
            "has_decarb_target",
            "decarb_target_in_calc",
            "target_year",
            "comprehensiveness_in_perc",
            "ambition_per_year",
            "target_data_date",
            "rating",
        ]

        for field in comparable_fields:
            equality_test = getattr(last_msci_value, field) == getattr(
                msci_value_to_test, field
            )
            print(
                f"{getattr(last_msci_value, field)} == {getattr(msci_value_to_test, field)}"
            )
            print(
                f"{type(getattr(last_msci_value, field))} == {type(getattr(msci_value_to_test, field))}"
            )
            if not equality_test:
                print(f"FIELD {field} : {equality_test}")

                return False

        return True


class MSCI(models.Model):

    objects = MSCIScoreManager()

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )
    date = models.DateField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    ITR = models.FloatField(blank=True, null=True)
    has_decarb_target = models.CharField(
        verbose_name="Decarbonization target", max_length=10, blank=True, null=True
    )
    decarb_target_in_calc = models.CharField(
        verbose_name="Decarbonization target considered in the calculation of ITR",
        max_length=10,
        blank=True,
        null=True,
    )
    target_year = models.CharField(
        verbose_name="Target Year",
        max_length=10,
        blank=True,
        null=True,
    )
    comprehensiveness_in_perc = models.FloatField(
        verbose_name="Comprehensiveness",
        blank=True,
        null=True,
    )
    ambition_per_year = models.FloatField(
        verbose_name="Ambition",
        blank=True,
        null=True,
    )
    target_data_date = models.DateField(
        verbose_name="Target data date",
        blank=True,
        null=True,
    )
    rating = models.CharField(
        verbose_name="Rating",
        max_length=10,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "MSCI data"
        verbose_name_plural = "MSCI data"

    def __str__(self):
        return self.company.name + "-" + str(self.date)

    def get_new_msci(self, record):

        self.company = Corporate.objects.get(company_id=record.get("company_id"))
        self.date = record.get("date")
        self.ITR = record.get("ITR")
        self.has_decarb_target = record.get("has_decarb_target")
        self.decarb_target_in_calc = record.get("decarb_target_in_calc")
        self.target_year = record.get("target_year")
        self.comprehensiveness_in_perc = record.get("comprehensiveness_in_perc")
        self.ambition_per_year = record.get("ambition_per_year")
        self.target_data_date = record.get("target_data_date")
        self.rating = record.get("rating")

        return self
