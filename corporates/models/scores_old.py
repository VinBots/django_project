from django.db import models
from .choices import Options


class Score(models.Model):

    id = models.BigAutoField(primary_key=True)
    update_date = models.DateField(auto_now=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE)

    #########################################################################
    rat_1_1 = models.CharField(
        choices=Options.YESNO, default=Options.NO, max_length=5, blank=True, null=True
    )
    sco_1_1 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_1_2 = models.CharField(
        choices=Options.COVERAGE_OPTIONS,
        default=Options.NOT_COVERED,
        max_length=25,
        blank=True,
        null=True,
    )
    sco_1_2 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_2_1 = models.CharField(
        choices=Options.COVERAGE_OPTIONS,
        default=Options.NOT_COVERED,
        max_length=25,
        blank=True,
        null=True,
    )
    sco_2_1 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_2_2 = models.CharField(
        choices=Options.COVERAGE_OPTIONS,
        default=Options.NOT_COVERED,
        max_length=25,
        blank=True,
        null=True,
    )
    sco_2_2 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_3_1 = models.FloatField(blank=True, null=True)

    sco_3_1 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_3_2 = models.FloatField(blank=True, null=True)
    sco_3_2 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_4_1 = models.CharField(
        choices=Options.YESNO, default=Options.NO, max_length=5, blank=True, null=True
    )
    sco_4_1 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_4_2 = models.CharField(
        choices=Options.YESNO, default=Options.NO, max_length=5, blank=True, null=True
    )
    sco_4_2 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_4_3 = models.CharField(
        choices=Options.YESNO, default=Options.NO, max_length=5, blank=True, null=True
    )
    sco_4_3 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_5_1 = models.PositiveSmallIntegerField(
        default=0, choices=[(x, x) for x in range(0, 30, 1)], blank=True, null=True
    )
    sco_5_1 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_5_2 = models.PositiveSmallIntegerField(
        default=0, choices=[(x, x) for x in range(0, 30, 1)], blank=True, null=True
    )
    sco_5_2 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_6_1 = models.FloatField(blank=True, null=True)
    sco_6_1 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_6_2 = models.FloatField(blank=True, null=True)
    sco_6_2 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_7_1 = models.CharField(
        choices=Options.SBTI_CHOICES, max_length=25, blank=True, null=True
    )
    sco_7_1 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_8_1 = models.FloatField(blank=True, null=True)
    sco_8_1 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_8_2 = models.FloatField(blank=True, null=True)
    sco_8_2 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_9_1 = models.FloatField(blank=True, null=True)
    sco_9_1 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_9_2 = models.FloatField(blank=True, null=True)
    sco_9_2 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_10_1 = models.FloatField(blank=True, null=True)
    sco_10_1 = models.FloatField(blank=True, null=True)
    #########################################################################
    rat_10_2 = models.FloatField(blank=True, null=True)
    sco_10_2 = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Score details"
        verbose_name_plural = "Score details"

    def __str__(self):
        return f"{self.company.short_name} - score as of {self.update_date} "
