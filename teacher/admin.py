from django.contrib import admin

from .models import (
    Teacher, Academic,
    ExtraInformation, ProfessionalExperience, Batch
)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["__str__"]


@admin.register(Academic)
class AcademicAdmin(admin.ModelAdmin):
    list_display = ["__str__"]


admin.site.register(ExtraInformation)
admin.site.register(ProfessionalExperience)
admin.site.register(Batch)
