import pathlib, os

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Case, When, Value

from .choices import Options


def user_directory_path(instance, filename):
    folder = "ghg"
    filename_str = f"{folder}/{instance.reporting_year}_{instance.company.name}_{instance.source}{pathlib.Path(filename).suffix}"
    return filename_str


class CustomManager(models.Manager):
    @staticmethod
    def map_scope_to_property(scope):
        mapping = {
            Options.SCOPE12_LOC: "scope_12_loc",
            Options.SCOPE12_MKT: "scope_12_mkt",
            Options.SCOPE12_BEST: "scope_12_best",
            Options.SCOPE3_BEST: "scope_3_best",
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
            custom_order, "last_update"
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

    def get_last_ghg(self, company, source, reporting_year):

        if isinstance(company, int):
            query = self.filter(
                company__company_id=company,
                source=source,
                reporting_year=reporting_year,
            ).order_by("-last_update", "-id")
        else:
            query = self.filter(
                company=company,
                source=source,
                reporting_year=reporting_year,
            ).order_by("-last_update", "-id")

        if query.exists():
            return query[0]

    def is_last_ghg_duplicate(self, ghg_to_test):

        last_ghg = self.get_last_ghg(
            company=ghg_to_test.company,
            source=ghg_to_test.source,
            reporting_year=ghg_to_test.reporting_year,
        )

        if not last_ghg:
            return False

        comparable_fields = [
            "ghg_scope_1",
            "ghg_loc_scope_2",
            "ghg_mkt_scope_2",
            "ghg_purch_scope3",
            "ghg_capital_scope3",
            "ghg_fuel_energy_loc_scope3",
            "ghg_fuel_energy_mkt_scope3",
            "ghg_upstream_td_scope3",
            "ghg_waste_ops_scope3",
            "ghg_bus_travel_scope3",
            "ghg_commute_scope3",
            "ghg_up_leased_scope3",
            "ghg_downstream_td_scope3",
            "ghg_proc_sold_scope3",
            "ghg_use_sold_scope3",
            "ghg_eol_sold_scope3",
            "ghg_down_leased_scope3",
            "ghg_franchises_scope3",
            "ghg_investments_scope3",
            "ghg_other_upstream_scope3",
            "ghg_other_downstream_scope3",
            "comments",
        ]

        for field in comparable_fields:
            equality_test = getattr(last_ghg, field) == getattr(ghg_to_test, field)
            # print(f"{getattr(last_ghg, field)} == {getattr(ghg_to_test, field)}")
            # print(
            #     f"{type(getattr(last_ghg, field))} == {type(getattr(ghg_to_test, field))}"
            # )
            if not equality_test:
                # print(f"FIELD {field} : {equality_test}")
                return False

        return True


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

    last_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    reporting_year = models.CharField(
        max_length=10,
        default=Options.YEAR_DEFAULT_GHG,
        choices=Options.YEAR_CHOICES,
        blank=True,
        null=True,
    )
    cdp_override = models.BooleanField(
        verbose_name="Does this GHG Inventory override GHG Inventory reported to CDP",
        editable=True,
        default=False,
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

    ghg_other_upstream_scope3 = models.PositiveIntegerField(blank=True, null=True)
    ghg_other_downstream_scope3 = models.PositiveIntegerField(blank=True, null=True)

    purch_ghg_offsets = models.PositiveIntegerField(blank=True, null=True)

    comments = models.TextField(blank=True, null=True)

    upload_1 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_2 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_3 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_4 = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    upload_5 = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "GHG Quantitative"
        # ordering = ["last_update"]

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
        empty_fields_count = fields.count("") + fields.count(None)
        return 5 - empty_fields_count

    @property
    def size_of_uploads(self):
        file_size = 0
        fields = self.get_upload_fields()
        for field in fields:
            if field and os.path.exists(field.path):
                file_size += field.file.size
        return f"{file_size / 1000000:.2f}Mb"

    @property
    def get_uploads(self):
        uploads = []
        fields = self.get_upload_fields()
        for field in fields:
            if field:
                path = f"/download/{field}"
                desc = f"GHG_emissions_{self.reporting_year}"
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
    def scope_12_best(self):
        if self.ghg_loc_scope_2 and self.ghg_mkt_scope_2:
            return min(self.scope_12_mkt, self.scope_12_loc)
        elif self.ghg_loc_scope_2:
            return self.scope_12_loc
        elif self.ghg_mkt_scope_2:
            return self.scope_12_mkt
        else:
            return self.ghg_scope_1

    @property
    def scope_3_loc_agg(self):

        categories = [
            self.ghg_purch_scope3,
            self.ghg_capital_scope3,
            self.ghg_fuel_energy_loc_scope3,
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
            self.ghg_other_upstream_scope3,
            self.ghg_other_downstream_scope3,
        ]
        if self.ghg_fuel_energy_loc_scope3 == 0:
            categories.append(self.ghg_fuel_energy_mkt_scope3)

        return sum(filter(bool, categories))

    @property
    def scope_3_mkt_agg(self):
        categories = [
            self.ghg_purch_scope3,
            self.ghg_capital_scope3,
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
            self.ghg_other_upstream_scope3,
            self.ghg_other_downstream_scope3,
        ]

        return sum(filter(bool, categories))

    @property
    def scope_3_best(self):
        if self.scope_3_mkt_agg and self.scope_3_loc_agg:
            return min(self.scope_3_mkt_agg, self.scope_3_loc_agg)
        elif self.scope_3_loc_agg:
            return self.scope_3_loc_agg
        elif self.scope_3_mkt_agg:
            return self.scope_3_mkt_agg
        else:
            return None

    @property
    def scope_123_loc(self):
        elements_to_sum = [self.scope_12_loc, self.scope_3_loc_agg]
        # print(elements_to_sum)

        return sum(filter(bool, elements_to_sum))

    @property
    def scope_123_mkt(self):
        elements_to_sum = [self.scope_12_mkt, self.scope_3_mkt_agg]
        # print(elements_to_sum)
        return sum(filter(bool, elements_to_sum))

    def __str__(self):
        return f"{self.company.short_name}-{self.reporting_year}-{self.source}"

    def save(self, *args, **kwargs):

        # if self.submitter.username != "django":
        #     self.id = None
        #     self.status = "submitted"
        super(GHGQuant, self).save(*args, **kwargs)
