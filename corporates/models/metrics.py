from django.db import models


class IntensityMetrics(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Investment(models.Model):

    EURO = "eur"
    USD = "usd"
    GBP = "gbp"

    CURRENCY_OPTIONS = [(EURO, "EUROS"), (USD, "USD"), (GBP, "GBP")]

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE)

    name = models.CharField(max_length=100, blank=False, null=False)
    update_date = models.DateField(auto_now=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.CharField(
        max_length=5, choices=CURRENCY_OPTIONS, default=USD, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Investments"
        ordering = ["update_date"]

    def __str__(self):
        return f"{self.company.short_name}-{self.name}"
