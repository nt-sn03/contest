from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count

from .models import (
    School,
    Group,
    Village,
    Contest,
    Candidate,
    Result,
)

APP_LABEL = "contest"


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "group_count", "candidate_count")
    search_fields = ("name",)
    ordering = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            group_total=Count("groups", distinct=True),
            candidate_total=Count("groups__candidates", distinct=True),
        )

    def group_count(self, obj):
        return obj.group_total

    group_count.short_description = "Sinflar soni"

    def candidate_count(self, obj):
        return obj.candidate_total

    candidate_count.short_description = "O‘quvchilar soni"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("school", "year", "letter", "candidate_count")
    list_filter = ("school", "year")
    search_fields = ("school__name",)
    ordering = ("school", "year", "letter")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(total=Count("candidates"))

    def candidate_count(self, obj):
        return obj.total

    candidate_count.short_description = "O‘quvchilar"


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ("name", "candidate_count")
    search_fields = ("name",)
    ordering = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(total=Count("candidates"))

    def candidate_count(self, obj):
        return obj.total

    candidate_count.short_description = "Ishtirokchilar"


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "contest_type_colored",
        "candidate_count",
        "result_count",
        "date",
    )
    list_filter = ("contest_type",)
    search_fields = ("title",)
    ordering = ("title",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            c_total=Count("candidates", distinct=True),
            r_total=Count("results", distinct=True),
        )

    def contest_type_colored(self, obj):
        colors = {
            "male": "#0d6efd",
            "female": "#d63384",
            "all": "#6c757d",
        }
        return format_html(
            '<b style="color:{}">{}</b>',
            colors[obj.contest_type],
            obj.get_contest_type_display(),
        )

    contest_type_colored.short_description = "Turi"

    def candidate_count(self, obj):
        return obj.c_total

    candidate_count.short_description = "Ishtirokchilar"

    def result_count(self, obj):
        return obj.r_total

    result_count.short_description = "Natijalar"


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "gender_colored",
        "group",
        "school",
        "village",
        "contest_count",
    )
    list_filter = (
        "gender",
        "group__school",
        "group__year",
        "village",
    )
    search_fields = (
        "first_name",
        "last_name",
        "group__school__name",
        "village__name",
    )
    autocomplete_fields = ("group", "village", "contests")
    list_select_related = ("group", "group__school", "village")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(total=Count("contests"))

    def full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"

    full_name.short_description = "F.I."

    def gender_colored(self, obj):
        return format_html(
            '<span style="color:{}">{}</span>',
            "#0d6efd" if obj.gender == "male" else "#d63384",
            obj.get_gender_display(),
        )

    gender_colored.short_description = "Jinsi"

    def school(self, obj):
        return obj.group.school

    school.short_description = "Maktab"
    school.admin_order_field = "group__school__name"

    def contest_count(self, obj):
        return obj.total

    contest_count.short_description = "Tanlovlar"


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "contest",
        "candidate_link",
        "score",
        "school",
        "group_name",
        "gender_icon",
    )
    list_filter = (
        "contest",
        "candidate__gender",
        "candidate__group__school",
        "candidate__group__year",
    )
    search_fields = (
        "candidate__first_name",
        "candidate__last_name",
        "contest__title",
    )
    autocomplete_fields = ("contest", "candidate")
    list_select_related = (
        "contest",
        "candidate",
        "candidate__group",
        "candidate__group__school",
    )

    def candidate_link(self, obj):
        opts = obj.candidate._meta
        url = reverse(
            f"admin:{opts.app_label}_{opts.model_name}_change",
            args=[obj.candidate.pk],
        )
        return format_html('<a href="{}">{}</a>', url, obj.candidate)

    candidate_link.short_description = "Ishtirokchi"

    def school(self, obj):
        return obj.candidate.group.school

    school.short_description = "Maktab"
    school.admin_order_field = "candidate__group__school__name"

    def group_name(self, obj):
        g = obj.candidate.group
        return f"{g.year}{g.letter}"

    group_name.short_description = "Sinfi"

    def gender_icon(self, obj):
        return "♂" if obj.candidate.gender == "male" else "♀"

    gender_icon.short_description = "Jinsi"
