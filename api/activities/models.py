from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from activities.abstract_models import (
    AbstractCommonInfo,
    AbstractCreatedUpdatedAt,
)


class Property(AbstractCommonInfo, AbstractCreatedUpdatedAt):
    address = models.TextField(
        null=False,
        blank=False,
        verbose_name=_("Address"),
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name=_("Description"),
    )
    disabled_at = models.DateTimeField(
        null=True,
        verbose_name=_("Disabled at"),
    )


class Activity(AbstractCommonInfo, AbstractCreatedUpdatedAt):
    property = models.ForeignKey(
        "activities.Property",
        on_delete=models.CASCADE,
        null=False,
        related_name="activities",
        verbose_name=_("Property"),
    )
    schedule = models.DateTimeField(
        null=False,
        verbose_name=_("Schedule"),
    )


class Survey(AbstractCreatedUpdatedAt):
    activity = models.OneToOneField(
        "activities.Activity",
        on_delete=models.CASCADE,
        related_name="survey",
        null=False,
        verbose_name=_("Activity"),
    )
    answers = JSONField(
        null=False,
        verbose_name=_("Answers"),
    )



