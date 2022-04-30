from django.db import models


class MSCI(models.Model):

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )
    date = models.DateField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    ITR = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "MSCI data"
        verbose_name_plural = "MSCI data"

    def __str__(self):
        return self.company.name + "-" + str(self.date)
