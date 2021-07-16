from django.db import models

class Corporates(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Entry(models.Model):
    name = models.CharField(max_length=124)
    corporate_name = models.ForeignKey(Corporates, on_delete=models.CASCADE, verbose_name="Find out about a corporate")

    def __str__(self):
        return self.name

