from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class School(models.Model):
    name = models.CharField(max_length=127, unique=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"{self.school} {self.year}{self.group}"


class Village(models.Model):
    name = models.CharField(max_length=127, unique=True)

    def __str__(self):
        return self.name


class Contest(models.Model):
    class TypeChoices(models.TextChoices):
        MALE = ("male", "O'g'il bolalar uchun")
        FEMALE = ("female", "Qiz bolalar uchun")
        ALL = ("all", "Hamma uchun")

    title = models.CharField(max_length=255, unique=True)
    contest_type = models.CharField(
        choices=TypeChoices.choices, default=TypeChoices.ALL
    )

    def __str__(self):
        return self.title


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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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

    def __str__(self):
        return f"{self.condidate} - {self.contest} ({self.ball})"