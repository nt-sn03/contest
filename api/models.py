from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class School(models.Model):
    name = models.CharField(max_length=127, unique=True)
    class Meta:
        verbose_name = "Maktab"
        verbose_name_plural = "Maktablar"
    


class Group(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="groups")
    year = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(11),
        ]
    )
    group = models.CharField(max_length=1)

    class Meta:
        unique_together = ("school", "year", "group")
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"


class Village(models.Model):
    name = models.CharField(max_length=127, unique=True)
    class Meta:
        verbose_name = "Qishloq"
        verbose_name_plural = "Qishloqlar"


class Contest(models.Model):
    class TypeChoices(models.TextChoices):
        MALE = ("male", "O'g'il bolalar uchun")
        FEMALE = ("female", "Qiz bolalar uchun")
        ALL = ("all", "Hamma uchun")

    title = models.CharField(max_length=255, unique=True)
    contest_type = models.CharField(
        choices=TypeChoices.choices, default=TypeChoices.ALL
    )
    
    class Meta:
        verbose_name = "Musobaqa"
        verbose_name_plural = "Musobaqalar"


class Condidate(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "O'g'il bola")
        FEMALE = ("female", "Qiz bola")

    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    gender = models.CharField(choices=GenderChoices.choices, default=GenderChoices.MALE)
    group = models.ForeignKey(
        Group, on_delete=models.DO_NOTHING, related_name="condidates"
    )
    village = models.ForeignKey(
        Village, on_delete=models.DO_NOTHING, related_name="condidates"
    )
    contests = models.ManyToManyField(Contest, related_name="condidates")
    
    class Meta:
        verbose_name = "Nomzod"
        verbose_name_plural = "Nomzodlar"


class Result(models.Model):
    contest = models.ForeignKey(
        Contest, on_delete=models.CASCADE, related_name="results"
    )
    condidate = models.ForeignKey(
        Condidate, on_delete=models.CASCADE, related_name="results"
    )
    ball = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100)]
    )
    class Meta:
        unique_together = ("contest", "condidate")
        verbose_name = "Natija"
        verbose_name_plural = "Natijalar"
