from django.db import models


class CustomMatchingManager(models.Manager):
    def get_tv_symb_from_company_id(self, company_id):
        query = self.filter(company__company_id=company_id)
        if query.exists():
            return query.values_list("tradingview_symbol", flat=True)[0]


class Matching(models.Model):

    objects = CustomMatchingManager()

    company = models.OneToOneField(
        "Corporate", on_delete=models.CASCADE, primary_key=True
    )
    tradingview_symbol = models.CharField(max_length=100, blank=True, null=True)
    sbti_company_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Matching"

    def __str__(self):
        return self.company.name
