from django.db import models


class Finnhub(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=100, blank=True, null=True)
    company_id = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Finnhub matching"
        verbose_name_plural = "Finnhub matchings"

    def __str__(self):
        return self.name
