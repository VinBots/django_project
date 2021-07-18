from django.db import models

class Corporate(models.Model):
    name = models.CharField(max_length=250)
    filename = models.CharField(
        max_length=20,
        default="dummy"
        )

    def __str__(self):
        return self.name
"""
class Entry(models.Model):
    name = models.CharField(max_length=124)
    corporate_name = models.ForeignKey(Corporates, on_delete=models.CASCADE, verbose_name="Find out about a corporate")

    def __str__(self):
        return self.name
"""
