from django.db import models
from django.db.models import F, Window, Subquery, OuterRef
from django.db.models.functions import Rank

from corporates.models.corp import Corporate


class ScoreManager(models.Manager):
    def get_max_score(self, score_name):
        return self.get(name=score_name).max_score

    def get_all_base_scores(self):
        return self.filter(name__startswith="Score_")


class Score(models.Model):

    objects = ScoreManager()

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    max_score = models.FloatField(blank=True, null=True)
    rating_description = models.CharField(max_length=250, blank=True, null=True)

    meta_1_desc = models.CharField(max_length=250, blank=True, null=True)
    meta_2_desc = models.CharField(max_length=250, blank=True, null=True)
    meta_3_desc = models.CharField(max_length=250, blank=True, null=True)
    meta_4_desc = models.CharField(max_length=250, blank=True, null=True)
    meta_5_desc = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class CompanyScoreManager(models.Manager):
    def get_last_score_value(self, company, score):

        last_score_value = CompanyScore.objects.filter(
            company=company, score=score
        ).order_by("-update_date", "-id")

        if last_score_value.exists():
            return last_score_value[0]

    def is_last_score_value_duplicate(self, score_value_to_test):

        last_score_value = self.get_last_score_value(
            company=score_value_to_test.company, score=score_value_to_test.score
        )
        if not last_score_value:
            return False

        for field in CompanyScore.VALUE_FIELDS:
            equality_test = getattr(score_value_to_test, field) == getattr(
                last_score_value, field
            )
            if not equality_test:
                return False

        return True

    def get_latest_scores(self):

        subquery = self.filter(
            company=OuterRef("company"), score=OuterRef("score")
        ).order_by("-update_date")

        queryset = self.annotate(
            latest_score_value=Subquery(subquery.values("score_value")[:1])
        )
        queryset = queryset.order_by("company", "score").distinct("company", "score")

        latest_scores = queryset.values(
            "company",
            "score",
            "update_date",
            "latest_score_value",
            "rating_value",
            "meta_value",
        )

        return latest_scores


class CompanyScore(models.Model):

    objects = CompanyScoreManager()

    id = models.BigAutoField(primary_key=True)
    update_date = models.DateField(auto_now=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE)

    score = models.ForeignKey("Score", on_delete=models.CASCADE)
    score_value = models.FloatField(blank=True, null=True)
    rating_value = models.CharField(max_length=100, blank=True, null=True)
    meta_value = models.JSONField(default=dict)

    VALUE_FIELDS = ["score_value", "rating_value", "meta_value"]

    class Meta:
        verbose_name_plural = "Scores Values"

    def __str__(self):
        return f"{self.company} - Score: {self.score.name} - Value: {self.score_value}"

    def get_blank_score(self, company_id, score_name):

        self.company = Corporate.objects.get(company_id=company_id)
        self.score = Score.objects.get(name=score_name)

        self.score_value = 0.0
        self.rating_value = "no"
        self.meta_value = {}

        return self


class LatestCompanyScoreManager(models.Manager):
    def import_latest_scores(self, latest_scores_queryset):
        records = []
        count = 0
        self.all().delete()

        for score_record in latest_scores_queryset:
            count += 1
            kwargs = {}
            # Expected Fields
            # ("company", "score", "latest_score_value", "rating_value", "meta_value")

            obj = Corporate.objects.get(**{"company_id": score_record["company"]})
            new_arg = {"company": obj}
            kwargs.update(new_arg)

            obj = Score.objects.get(**{"id": score_record["score"]})
            new_arg = {"score": obj}
            kwargs.update(new_arg)

            non_fk_fields = [
                "update_date",
                "latest_score_value",
                "rating_value",
                "meta_value",
            ]
            for field in non_fk_fields:
                new_arg = {field: score_record[field]}
                kwargs.update(new_arg)

            record = self.model(**kwargs)
            records.append(record)
            if len(records) > 5000:
                self.model.objects.bulk_create(records)
                records = []

        if records:
            self.model.objects.bulk_create(records)

    def get_latest_company_score_value(self, company_id, score_name):
        return self.filter(company__company_id=company_id, score__name=score_name)

    def get_rank(self, company_id, score_name):

        rank_by_score = Window(
            expression=Rank(),
            partition_by=F("score"),
            order_by=F("latest_score_value").desc(),
        )

        query = (
            LatestCompanyScore.objects.filter(score__name__in=[score_name])
            .annotate(rank=rank_by_score)
            .order_by("rank")
        )

        for record in query.values("company__company_id", "rank"):
            if record["company__company_id"] == company_id:
                return record["rank"]


class LatestCompanyScore(models.Model):

    objects = LatestCompanyScoreManager()

    id = models.BigAutoField(primary_key=True)
    update_date = models.DateField(blank=True, null=True)
    company = models.ForeignKey("Corporate", on_delete=models.CASCADE)
    score = models.ForeignKey("Score", on_delete=models.CASCADE)
    latest_score_value = models.FloatField(blank=True, null=True)
    score_pct = models.FloatField(blank=True, null=True)
    rating_value = models.CharField(max_length=100, blank=True, null=True)
    meta_value = models.JSONField(default=dict)

    VALUE_FIELDS = ["score_value", "rating_value", "meta_value"]

    class Meta:
        verbose_name_plural = "Latest Scores Values"

    def __str__(self):
        return f"{self.company} - {self.score.name}: {self.latest_score_value} ({self.update_date})"

    def get_blank_score(self, company_id, score_name):

        self.company = Corporate.objects.get(company_id=company_id)
        self.score = Score.objects.get(name=score_name)

        self.latest_score_value = 0.0
        self.rating_value = "no"
        self.meta_value = {}

        return self
