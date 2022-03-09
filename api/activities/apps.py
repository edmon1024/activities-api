from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ActivitiesConfig(AppConfig):
    name = 'activities'
    verbose_name = _("Activity")
    verbose_name_plural = _("Activities")

