from django.utils import timezone
from rest_framework import serializers

from activities.models import (
    Property,
    Activity,
    Survey,
)


class SurveyRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id','answers',)


class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id','title','address','status',)


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id','title','address',)


class ActivitySerializer(serializers.ModelSerializer):
    property =  PropertySerializer(many=False)
    condition = serializers.SerializerMethodField()
    survey = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='survey-detail'
    )

    class Meta:
        model = Activity
        fields = (
            'id','schedule','title','created_at','status',
            'condition','property','survey',
        )
        read_only_fields = ('id','created_at',)


    def get_condition(self, obj):
        if obj.status == "done":
            return "Finalizada" 

        if obj.status == "active":
            now = timezone.now()

            if obj.schedule >= now:
                return "Pendiente a realizar"

            if obj.schedule < now:
                return "Atrasada"

        return ""


