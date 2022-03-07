from django.utils import timezone
import datetime
from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from activities.models import (
    Property,
    Activity,
    Survey,
)
from activities.serializers import (
    PropertyListSerializer,
    ActivityListSerializer,
    ActivityCreateSerializer,
    SurveySerializer,
    RescheduleActivitySerializer,
    CancelledActivitySerializer,
)
from activities.filters import ActivityFilter
from activities.utils.validations import is_available_schedule



class PropertyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Property.objects.filter(status__in=["active",])
    serializer_class = PropertyListSerializer


class ActivityViewSet(mixins.ListModelMixin, 
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivityListSerializer
    filter_class = ActivityFilter

    def get_serializer_class(self):
        if self.action == "create":
            return ActivityCreateSerializer

        if self.action == "reschedule":
            return RescheduleActivitySerializer

        if self.action == "cancelled":
            return CancelledActivitySerializer

        return self.serializer_class

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
        start_date = now - datetime.timedelta(days=3)
        end_date = now + datetime.timedelta(days=14)

        return self.queryset.filter(schedule__range=(start_date, end_date))

    @action(detail=True, methods=['patch'])
    def reschedule(self, request, pk=None):
        obj = Activity.objects.filter(pk=pk).first()

        serializer = self.get_serializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            if obj.status == "cancelled":
                return Response(
                    {
                        "status": _("Cancelled activities cannot be rescheduled"),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            verify = is_available_schedule(
                serializer.validated_data["schedule"], 
                obj.property_id, 
                excluded_ids=[obj.id]
            )

            if not verify:
                return Response(
                    {
                        "schedule": _("Activities cannot be created on the same date and time as another activity"),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            return Response(serializer.data)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancelled(self, request, pk=None):
        obj = Activity.objects.filter(pk=pk).first()

        if obj.status == "done":
            return Response(
                {
                    "status": _("The status cannot be changed, the activity has done"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if obj.status == "cancelled":
            return Response(
                {
                    "status": _("The status cannot be changed, the activity has cancelled"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj.status = "cancelled"
        obj.save()

        return Response({
            "status": obj.status,
        })


class SurveyViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer



