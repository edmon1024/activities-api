from django.db import models
from django.utils import timezone
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

    STATUS_CHOICES = (
        ('active', _('Active')),
        ('disabled', _('Disabled')),
    )
    status = models.CharField(
        max_length=35,
        null=False,
        blank=False,
        verbose_name=_("Status"),
        choices=STATUS_CHOICES,
        default="active",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")


class Activity(AbstractCommonInfo, AbstractCreatedUpdatedAt):
    property_id = models.ForeignKey(
        "activities.Property",
        on_delete=models.CASCADE,
        null=False,
        related_name="activities",
        verbose_name=_("Property"),
        db_column="property_id",
        default=None,
    )
    schedule = models.DateTimeField(
        null=False,
        verbose_name=_("Schedule"),
    )

    STATUS_CHOICES = (
        ('active', _('Active')),
        ('done', _('Done')),
        ('cancelled', _('Cancelled')),
    )

    status = models.CharField(
        max_length=35,
        null=False,
        blank=False,
        verbose_name=_("Status"),
        choices=STATUS_CHOICES,
        default="active",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    def condition(self):
        if self.status == "done":
            return "Finalizada"

        if self.status == "active":
            now = timezone.now()

            if self.schedule >= now:
                return "Pendiente a realizar"

            if self.schedule < now:
                return "Atrasada"

        return ""

    condition.short_description = _("Condition")
    condition = property(condition)


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
    updated_at = None

    def __str__(self):
        return str(self.activity)

    class Meta:
        verbose_name = _("Survey")
        verbose_name_plural = _("Surveys")


