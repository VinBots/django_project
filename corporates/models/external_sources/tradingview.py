from django.db import models

from corporates.models.corp import Corporate

# from corporates.models.choices import Options


class TradingviewScoreManager(models.Manager):
    def get_last_tv_value(self, company, account, period):

        if isinstance(company, int):
            query = self.filter(
                company__company_id=company, account=account, period=period
            ).order_by("-last_update", "-id")
        else:
            query = self.filter(
                company=company, account=account, period=period
            ).order_by("-last_update", "-id")

        if query.exists():
            return query[0]

    def get_value(self, company, account, period):
        last_value = self.get_last_tv_value(company, account, period)
        if last_value:
            return last_value.value
        else:
            return None

    def is_last_tv_value_duplicate(self, tv_value_to_test):

        last_tv_value = self.get_last_tv_value(
            company=tv_value_to_test.company,
            account=tv_value_to_test.account,
            period=tv_value_to_test.period,
        )
        if not last_tv_value or last_tv_value.value != tv_value_to_test.value:
            return False

        return True


class Tradingview(models.Model):

    objects = TradingviewScoreManager()

    id = models.BigAutoField(primary_key=True)
    last_update = models.DateTimeField(auto_now=True)
    # symbol = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )
    account = models.CharField(max_length=200, blank=True, null=True)

    period = models.CharField(
        verbose_name="Period",
        max_length=10,
        blank=True,
        null=True,
    )
    value = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Tradingview financial"

    def __str__(self):
        return f"{self.company.name} - {self.account} - {self.period}"

    def get_new_tv(self, company_id, account, period, value):

        self.company = Corporate.objects.get(company_id=company_id)

        self.account = account
        self.period = period
        self.value = value

        return self
