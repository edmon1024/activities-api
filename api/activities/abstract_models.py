from django.db import models
from django.utils.translation import ugettext_lazy as _



class AbstractCommonInfo(models.Model):
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("Title"),
    )
    status = models.CharField(
        max_length=35,
        null=False,
        blank=False,
        verbose_name=_("Status"),
    )

    class Meta:
        abstract = True


class AbstractCreatedUpdatedAt(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=False,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=False,
        verbose_name=_("Updated at"),
    )

    class Meta:
        abstract = True


