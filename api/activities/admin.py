from django.contrib import admin
from activities.models import (
    Property,
    Activity,
    Survey,
)



@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "id","title","created_at","updated_at",
        "disabled_at","status",
    )
    fields = (
        "id","title","address","description","status",
        "disabled_at","created_at","updated_at",
    )
    readonly_fields = ("id","disabled_at","created_at","updated_at",)
    search_fields = ("title","status",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "id","property_id","schedule","title","status",
        "created_at","updated_at",
    )
    fields = (
        "id","property_id","schedule","title","status",
        "created_at","updated_at",
    )
    readonly_fields = ("id","created_at","updated_at",)
    search_fields = ("title","status",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("property_id")


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("id","activity","created_at",)
    fields = ("id","activity","answers","created_at",)
    readonly_fields = ("id","created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("activity")


