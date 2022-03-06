from django_filters import rest_framework as filters
from activities.models import Activity


class ActivityFilter(filters.FilterSet):
    schedule = filters.DateTimeFromToRangeFilter()
    status = filters.CharFilter(
        lookup_expr="exact",
    )

    class Meta:
        model = Activity
        fields = ['schedule','status',]
