import django
from django.db import models

from django.contrib.auth.models import User

# from accounts.models import CustomUser


class Source(models.Model):

    source = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=250)
    website_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.source


class Company(models.Model):

    company_name = models.CharField(max_length=250, unique=True)
    company_short_name = models.CharField(max_length=50, blank=True, null=True)
    primary_ISIN = models.CharField(max_length=12, blank=True, null=True, unique=True)
    primary_ticker = models.CharField(max_length=10, blank=True, null=True, unique=True)
    website_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "companies"


class GHGQuant(models.Model):

    company = models.ForeignKey("Company", on_delete=models.DO_NOTHING)
    source = models.ForeignKey(
        "Source", blank=True, null=True, on_delete=models.DO_NOTHING
    )
    submitter = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    update_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    reporting_year = models.PositiveIntegerField()

    ghg_scope_1 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_loc_scope_2 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_mkt_scope_2 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_purch_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_capital_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_fuel_energy_loc_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_fuel_energy_mkt_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_upstream_td_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_wate_ops_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_bus_travel_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_commute_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_up_leased_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_downstream_td_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_proc_sold_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_use_sold_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_eol_sold_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_down_leased_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_franchises_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_investments_scope3 = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    ghg_other = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )
    purch_ghg_offsets = models.DecimalField(
        max_digits=12, decimal_places=1, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "GHG Quantitative"
        ordering = ["update_date"]

    def __str__(self):
        return f"{self.company.company_short_name}-{self.reporting_year}"

    def save(self, *args, **kwargs):

        if self.submitter.username != "django":
            self.id = None
            self.status = "submitted"
        super(GHGQuant, self).save(*args, **kwargs)
