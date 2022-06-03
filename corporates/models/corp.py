from django.db import models
from corporates.models.grouping import CorporateGrouping
import random
from django.db.models import Count
from django.contrib.auth.models import User


class CorporatesManager(models.Manager):
    def random(self, SP100=True):
        if SP100:
            company_ids = CorporateGrouping.objects.get_sp100_company_ids()
        else:
            company_ids = self.all().values_list("company_id", flat=True)
        random_indexes = random.sample(list(company_ids), 5)
        return self.filter(company_id__in=random_indexes)


class Corporate(models.Model):
    objects = CorporatesManager()
    company_id = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    web_URL = models.URLField("Web Address", blank=True, null=True)
    cdp_account = models.IntegerField(default=0)
    # primary_country = models.ForeignKey(
    #     "Country", blank=True, null=True, on_delete=models.CASCADE
    # )

    class Meta:
        db_table = "Corporate"
        verbose_name = "Corporate"
        verbose_name_plural = "Corporates"

    def __str__(self):
        return self.name


class ISIN(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=100, unique=True)
    company_id = models.ForeignKey(
        Corporate, blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "ISIN"
        verbose_name_plural = "ISINs"

    def __str__(self):
        return self.name


class Ticker(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=100, unique=True)
    company_id = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Ticker"
        verbose_name_plural = "Tickers"

    def __str__(self):
        return self.name


class Site(models.Model):
    """Client sites description"""

    id = models.BigAutoField(primary_key=True)

    company_id = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Sites"

    def __str__(self):
        return self.name


"""
https://medium.com/@DoorDash/tips-for-building-high-quality-django-apps-at-scale-a5a25917b2b5
https://doordash.engineering/2020/12/02/how-doordash-transitioned-from-a-monolith-to-microservices/

https://steelkiwi.com/blog/best-practices-working-django-models-python/
17. Getting the earliest/latest object
You can use ModelName.objects.earliest('created'/'earliest') instead of order_by('created')[0] 
and you can also put get_latest_by in Meta model. You should keep in mind that latest/earliest 
as well as get can cause an exception DoesNotExist. Therefore, order_by('created').first() is
the most useful variant
"""
