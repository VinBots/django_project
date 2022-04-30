from django.db import models


class Tradingview(models.Model):
    id = models.BigAutoField(primary_key=True)

    ticker = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=100, blank=True, null=True)
    company_id = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Tradingview matching"
        verbose_name_plural = "Tradingview matchings"

    def __str__(self):
        return self.name
