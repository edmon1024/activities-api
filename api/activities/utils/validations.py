import datetime
from django.db.models import Q
from activities.models import Activity


def is_available_schedule(schedule, property_id, **kwargs):
    """ 
        Check if there is no schedule assigned to the property and at the same time 
        (Duration of activity of a maximum of one hour) 

        kwargs:
            excluded_ids: []
    """

    schedule_start = schedule - datetime.timedelta(minutes=60)
    schedule_end = schedule + datetime.timedelta(minutes=60)

    excluded_ids = kwargs.get("excluded_ids",[])

    
    if bool(excluded_ids):
        activities = Activity.objects.filter(
            Q(property_id=property_id),
            Q(schedule__range=(schedule_start, schedule_end)),
            ~Q(id__in=excluded_ids),
        )

    else:
        activities = Activity.objects.filter(
            Q(property_id=property_id),
            Q(schedule__range=(schedule_start, schedule_end)),
        )

    count = activities.count()
    if count == 0:
        return True

    return False


