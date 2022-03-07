from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from activities.models import (
    Property,
    Activity,
    Survey,
)
from activities.utils.validations import is_available_schedule


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id','answers',)
        read_only_fields = ('id',)


class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id','title','address','status',)


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id','title','address',)


class ActivityListSerializer(serializers.ModelSerializer):
    property_id =  PropertySerializer(many=False)
    survey = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='survey-detail'
    )

    class Meta:
        model = Activity
        fields = (
            'id','schedule','title','created_at','status',
            'condition','property_id','survey',
        )
        read_only_fields = ('id','condition','created_at',)


class ActivityCreateSerializer(serializers.ModelSerializer):
    property_id = serializers.PrimaryKeyRelatedField(
        many=False,
        allow_null=False,
        queryset=Property.objects.all(),
    )
    survey = SurveySerializer(many=False)

    class Meta:
        model = Activity
        fields = (
            'id','property_id','schedule','title','survey',
            'condition','created_at',
        )
        read_only_fields = ('id','condition','created_at',)

    def create(self, validated_data):
        survey_data = validated_data.pop("survey")
        property_data = validated_data.get("property_id")
        schedule = validated_data.get("schedule")

        if property_data.status != "active":
            raise serializers.ValidationError({
                "property_id": _("The activity cannot be created if the property is disabled"),
            })

        if not is_available_schedule(schedule, property_data):
            raise serializers.ValidationError(
                _("Activities cannot be created on the same date and time as another activity")
            )

        activity = Activity.objects.create(**validated_data)
        Survey.objects.create(activity=activity, **survey_data)

        return activity


class RescheduleActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id','schedule',)
        read_only_fields = ('id',)

class CancelledActivitySerializer(serializers.Serializer):
    pass

