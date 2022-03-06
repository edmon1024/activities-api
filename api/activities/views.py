from django.utils import timezone
import datetime
from django.shortcuts import render
from rest_framework import mixins, viewsets

from activities.models import (
    Property,
    Activity,
    Survey,
)
from activities.serializers import (
    PropertyListSerializer,
    ActivitySerializer,
    SurveyRetrieveSerializer,
)
from activities.filters import ActivityFilter



class PropertyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Property.objects.filter(status__in=["active",])
    serializer_class = PropertyListSerializer


class ActivityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_class = ActivityFilter

    def get_queryset(self):
        pk = self.kwargs.get("pk",None)

        if pk:
            return self.queryset.filter(id=pk)

        status = self.request.query_params.get("status", None)
        schedule_after = self.request.query_params.get("schedule_after", None)
        schedule_before = self.request.query_params.get("schedule_before", None)

        if status != None or schedule_after != None or schedule_before != None:
            return self.queryset.all()

        now = timezone.now()
        start_date = now - datetime.timedelta(3)
        end_date = now + datetime.timedelta(14)

        return self.queryset.filter(schedule__range=(start_date, end_date))


class SurveyViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveyRetrieveSerializer



