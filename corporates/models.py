from django.db import models
import random
from django.db.models import Count


class CorporatesManager(models.Manager):

    def random(self):
        count = self.aggregate(count = Count('company_id'))['count']
        random_index = random.randint(0, count - 1)
        return self.all()[random_index]

class Corporate(models.Model):
    objects = CorporatesManager()
    company_id = models.IntegerField(default = 0)
    name = models.CharField(max_length=250)
    filename = models.CharField(
        max_length=20,
        default="dummy"
        )

    def __str__(self):
        return self.name




