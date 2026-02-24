from django.contrib import admin

from .models import School, Group, Village, Condidate, Contest, Result


@admin.register(School)
class SchoolModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Village)
class VillageModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Condidate)
class CondidateModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Contest)
class ContestModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Result)
class ResultModelAdmin(admin.ModelAdmin):
    pass
