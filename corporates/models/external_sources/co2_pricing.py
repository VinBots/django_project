from django.db import models
from corporates.models.corp import Corporate
from corporates.models.choices import Options


class CO2PricingScoreManager(models.Manager):
    def get_last_co2_price(self, date):

        last_co2_price = self.filter(date=date).order_by("-last_update", "-id")

        if last_co2_price.exists():
            return last_co2_price[0]

    def is_last_co2_price_duplicate(self, co2_price_to_test):

        last_co2_price = self.get_last_co2_price(
            date=co2_price_to_test.date,
        )

        if not last_co2_price:
            return False

        comparable_fields = ["date", "price"]

        for field in comparable_fields:
            equality_test = getattr(last_co2_price, field) == getattr(
                co2_price_to_test, field
            )
            print(
                f"{getattr(last_co2_price, field)} == {getattr(co2_price_to_test, field)}"
            )
            print(
                f"{type(getattr(last_co2_price, field))} == {type(getattr(co2_price_to_test, field))}"
            )
            if not equality_test:
                print(f"FIELD {field} : {equality_test}")

                return False

        return True


class CO2Pricing(models.Model):

    objects = CO2PricingScoreManager()

    id = models.BigAutoField(primary_key=True)

    date = models.DateField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    price = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "CO2 Pricing data"
        verbose_name_plural = "CO2 Pricing data"

    def __str__(self):
        return str(self.date) + "-" + str(self.price)

    def get_new_ihs(self, record):

        self.date = record.get("date")
        self.price = record.get("price")

        return self
