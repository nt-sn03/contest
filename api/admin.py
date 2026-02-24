from django.contrib import admin

from .models import School, Group, Village, Condidate, Contest, Result


@admin.register(School)
class SchoolModelAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ("school", "year", "group")
    list_filter = ("school", "year")


@admin.register(Village)
class VillageModelAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Condidate)
class CondidateModelAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "gender", "group")
    list_filter = ("gender", "group__school", "group__year")
    search_fields = ("first_name", "last_name") 


@admin.register(Contest)
class ContestModelAdmin(admin.ModelAdmin):
    list_display = ("title", "contest_type")
    list_filter = ("contest_type",)


@admin.register(Result)
class ResultModelAdmin(admin.ModelAdmin):
    list_display = ("contest", "condidate", "ball")
