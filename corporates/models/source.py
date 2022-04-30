from django.db import models


class Source(models.Model):

    id = models.BigAutoField(primary_key=True)
    source = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    website_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.source
