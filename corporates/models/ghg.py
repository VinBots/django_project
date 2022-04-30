import pathlib

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Case, When, Value
from django.forms import IntegerField

from .choices import Options


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    folder = "ghg2"
    # FORMAT '[reporting_year]_[company_name]_[source]_[submitter]

    filename = f"{folder}/{instance.reporting_year}_{instance.company.name}_{instance.source}_{instance.submitter.username}{pathlib.Path(filename).suffix}"
    return filename


class CustomManager(models.Manager):
    @staticmethod
    def map_scope_to_property(scope):
        mapping = {
            Options.SCOPE12_LOC: "scope_12_loc",
            Options.SCOPE12_MKT: "scope_12_mkt",
            Options.SCOPE123_LOC: "scope_123_loc",
            Options.SCOPE123_MKT: "scope_123_mkt",
        }
        return mapping.get(scope)

    def get_ghg(self, id, scope_coverage, year):

        custom_order = Case(
            When(source=Options.FINAL, then=Value(1)),
            When(source=Options.PUBLIC, then=Value(2)),
            When(source=Options.CDP, then=Value(3)),
        )

        queryset = self.filter(company__company_id=id, reporting_year=year).order_by(
            custom_order, "update_date"
        )
        if queryset.exists():
            result = getattr(
                queryset[0], CustomManager.map_scope_to_property(scope_coverage)
            )
            return result

    def get_last_reporting_year(self, company_id):

        """
        Look for the most recent GHG Inventory and returns the corresponding year
        Returns None if no GHG Inventory is recorded
        """

        queryset = self.filter(company_id=company_id).order_by("-reporting_year")
        if queryset.exists():
            last_reporting_year = queryset.values("reporting_year")[0].get(
                "reporting_year", None
            )
            return last_reporting_year


class GHGQuant(models.Model):

    objects = CustomManager()

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE, blank=True)
    source = models.CharField(
        choices=Options.GHG_SOURCES_OPTIONS,
        default=Options.PUBLIC,
        max_length=50,
        blank=True,
        null=True,
    )
    category = models.CharField(
        choices=Options.GHG_CATEGORY_OPTIONS, max_length=100, blank=True, null=True
    )

    submitter = models.ForeignKey(
        User, related_name="ghg_sub", blank=True, null=True, on_delete=models.CASCADE
    )
    verifier = models.ForeignKey(
        User, related_name="ghg_ver", blank=True, null=True, on_delete=models.CASCADE
    )

    update_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    reporting_year = models.CharField(
        max_length=10,
        default=Options.YEAR_DEFAULT_GHG,
        choices=Options.YEAR_CHOICES,
        blank=True,
        null=True,
    )

    ghg_scope_1 = models.PositiveIntegerField(blank=True, null=True)
    ghg_loc_scope_2 = models.PositiveIntegerField(blank=True, null=True)
    ghg_mkt_scope_2 = models.PositiveIntegerField(blank=True, null=True)
    ghg_purch_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_capital_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_fuel_energy_loc_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_fuel_energy_mkt_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_upstream_td_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_waste_ops_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_bus_travel_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_commute_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_up_leased_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_downstream_td_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_proc_sold_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_use_sold_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_eol_sold_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_down_leased_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_franchises_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_investments_scope3 = models.PositiveIntegerField(blank=True, null=True)

    ghg_other = models.PositiveIntegerField(blank=True, null=True)
    purch_ghg_offsets = models.PositiveIntegerField(blank=True, null=True)

    upload_1 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_2 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_3 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_4 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_5 = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "GHG Quantitative"
        # ordering = ["update_date"]

    def get_upload_fields(self):
        return [
            self.upload_1,
            self.upload_2,
            self.upload_3,
            self.upload_4,
            self.upload_5,
        ]

    @property
    def number_of_uploads(self):
        fields = self.get_upload_fields()
        return 5 - fields.count("")

    @property
    def size_of_uploads(self):
        file_size = 0
        fields = self.get_upload_fields()
        for field in fields:
            if field:
                file_size += field.file.size
        return f"{file_size / 1000000:.2f}Mb"

    @property
    def get_uploads(self):
        uploads = []
        fields = self.get_upload_fields()
        for field in fields:
            if field:
                path = f"/download/{field}"
                desc = f"{self.source.source} - {self.reporting_year}"
                dict = {"path": path, "desc": desc}
                uploads.append(dict)
        return uploads

    @property
    def scope_12_loc(self):

        categories = [self.ghg_scope_1, self.ghg_loc_scope_2]
        return sum(filter(bool, categories))

    @property
    def scope_12_mkt(self):

        categories = [self.ghg_scope_1, self.ghg_mkt_scope_2]
        return sum(filter(bool, categories))

    @property
    def scope_3_loc_agg(self):

        categories = [
            self.ghg_purch_scope3,
            self.ghg_capital_scope3,
            self.ghg_fuel_energy_loc_scope3,
            # self.ghg_fuel_energy_mkt_scope3,
            self.ghg_upstream_td_scope3,
            self.ghg_waste_ops_scope3,
            self.ghg_bus_travel_scope3,
            self.ghg_commute_scope3,
            self.ghg_up_leased_scope3,
            self.ghg_downstream_td_scope3,
            self.ghg_proc_sold_scope3,
            self.ghg_use_sold_scope3,
            self.ghg_eol_sold_scope3,
            self.ghg_down_leased_scope3,
            self.ghg_franchises_scope3,
            self.ghg_investments_scope3,
        ]

        return sum(filter(bool, categories))

    @property
    def scope_3_mkt_agg(self):
        categories = [
            self.ghg_purch_scope3,
            self.ghg_capital_scope3,
            # self.ghg_fuel_energy_loc_scope3,
            self.ghg_fuel_energy_mkt_scope3,
            self.ghg_upstream_td_scope3,
            self.ghg_waste_ops_scope3,
            self.ghg_bus_travel_scope3,
            self.ghg_commute_scope3,
            self.ghg_up_leased_scope3,
            self.ghg_downstream_td_scope3,
            self.ghg_proc_sold_scope3,
            self.ghg_use_sold_scope3,
            self.ghg_eol_sold_scope3,
            self.ghg_down_leased_scope3,
            self.ghg_franchises_scope3,
            self.ghg_investments_scope3,
        ]
        return sum(filter(bool, categories))

    @property
    def scope_123_loc(self):
        elements_to_sum = [self.scope_12_loc, self.scope_3_loc_agg]
        return sum(filter(bool, elements_to_sum))

    @property
    def scope_123_mkt(self):
        elements_to_sum = [self.scope_12_mkt, self.scope_3_mkt_agg]
        return sum(filter(bool, elements_to_sum))

    def __str__(self):
        return f"{self.company.short_name}-{self.reporting_year}"

    def save(self, *args, **kwargs):

        # if self.submitter.username != "django":
        #     self.id = None
        #     self.status = "submitted"
        super(GHGQuant, self).save(*args, **kwargs)
