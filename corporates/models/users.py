from django.contrib.auth.models import User
from django.db import models
from .corp import Corporate


class UserProfile(models.Model):

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    allowed_corporates_all = models.BooleanField(blank=True, null=True)
    allowed_corporates = models.ManyToManyField(
        Corporate, related_name="all_users_by_corp", blank=True
    )

    def __str__(self):
        return self.user.username
