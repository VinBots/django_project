from django.db import models

from corporates.models import Corporate


class FinnhubMatching(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=100, blank=True, null=True)
    symbol = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Finnhub matching"
        verbose_name_plural = "Finnhub matchings"

    def __str__(self):
        return self.name


class StockDataManager(models.Manager):
    def get_last_stock_data(self, company, current_date):

        if isinstance(company, int):
            query = self.filter(
                company__company_id=company,
                current_date=current_date,
            ).order_by("-last_update", "-id")
        else:
            query = self.filter(company=company, current_date=current_date).order_by(
                "-last_update", "-id"
            )

        if query.exists():
            return query[0]

    def is_last_stock_data_duplicate(self, stock_data_to_test):

        last_stock_data = self.get_last_stock_data(
            company=stock_data_to_test.company,
            current_date=stock_data_to_test.current_date,
        )

        if not last_stock_data:
            return False

        comparable_fields = [
            "company_id",
            "last_date",
            "last_c",
            "current_date",
            "current_c",
            "pre_pct_chg",
        ]

        for field in comparable_fields:
            equality_test = getattr(last_stock_data, field) == getattr(
                stock_data_to_test, field
            )
            print(
                f"{getattr(last_stock_data, field)} == {getattr(stock_data_to_test, field)}"
            )
            print(
                f"{type(getattr(last_stock_data, field))} == {type(getattr(stock_data_to_test, field))}"
            )
            if not equality_test:
                print(f"FIELD {field} : {equality_test}")

                return False

        return True


class StockData(models.Model):

    objects = StockDataManager()

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )
    last_update = models.DateTimeField(auto_now=True)

    current_date = models.DateField(blank=True, null=True)
    current_c = models.FloatField(blank=True, null=True)
    last_date = models.DateField(blank=True, null=True)
    last_c = models.FloatField(blank=True, null=True)
    pre_pct_chg = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Stock data"
        verbose_name_plural = "Stock data"

    def __str__(self):
        return (
            self.company.name
            + "-"
            + str(self.current_date)
            + "- Closing: "
            + str(self.current_c)
        )

    def get_new_stock(self, record):

        self.company = Corporate.objects.get(company_id=record.get("company_id"))
        self.current_date = record.get("current_date")
        self.last_date = record.get("last_date")
        self.current_c = record.get("current_c")
        self.last_c = record.get("last_c")
        self.pre_pct_chg = record.get("pre_pct_chg")
        return self
