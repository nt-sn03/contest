from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class School(models.Model):
    name = models.CharField(max_length=127, unique=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="groups")
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(11)]
    )
    letter = models.CharField(max_length=1)

    class Meta:
        unique_together = ("school", "year", "letter")
        ordering = ["school", "year", "letter"]

    def __str__(self):
        return f"{self.school} - {self.year}{self.letter}"


class Village(models.Model):
    name = models.CharField(max_length=127, unique=True)

    def __str__(self):
        return self.name


class Contest(models.Model):
    class TypeChoices(models.TextChoices):
        MALE = ("male", "O‘g‘il bolalar uchun")
        FEMALE = ("female", "Qiz bolalar uchun")
        ALL = ("all", "Hamma uchun")

    title = models.CharField(max_length=255, unique=True)
    contest_type = models.CharField(
        max_length=10, choices=TypeChoices.choices, default=TypeChoices.ALL
    )
    date = models.DateField()
    description = models.TextField(blank=True)
    max_score = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "O‘g‘il bola")
        FEMALE = ("female", "Qiz bola")

    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    group = models.ForeignKey(
        Group, on_delete=models.PROTECT, related_name="candidates"
    )
    village = models.ForeignKey(
        Village, on_delete=models.PROTECT, related_name="candidates"
    )
    contests = models.ManyToManyField(Contest, related_name="candidates", blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Result(models.Model):
    contest = models.ForeignKey(
        Contest, on_delete=models.CASCADE, related_name="results"
    )
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="results"
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        unique_together = ("contest", "candidate")
        ordering = ["-score"]

    def clean(self):
        if self.contest.contest_type != Contest.TypeChoices.ALL:
            if self.contest.contest_type != self.candidate.gender:
                raise ValidationError("Bu ishtirokchi ushbu tanlovda qatnasha olmaydi.")

        if self.score > self.contest.max_score:
            raise ValidationError(
                f"Ball {self.contest.max_score} dan oshmasligi kerak."
            )

    def __str__(self):
        return f"{self.candidate} - {self.contest} ({self.score})"
