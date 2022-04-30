from django.db import models


class Library(models.Model):

    id = models.IntegerField(primary_key=True)
    folder_name = models.CharField(max_length=100, blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, null=True)
    company_id = models.ForeignKey(
        "Corporate", blank=True, null=True, on_delete=models.CASCADE
    )
    category = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField()
    part = models.CharField(max_length=100, blank=True, null=True)
    desc = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Library"
        verbose_name_plural = "Library records"

    def __str__(self):
        return self.company_id.name + "-" + self.desc
