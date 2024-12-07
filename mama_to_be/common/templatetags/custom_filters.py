from django import template
import timeago
from django.utils import timezone

register = template.Library()


@register.filter
def timeago_filter(value):
    # Make sure `value` is timezone-aware
    if timezone.is_naive(value):
        value = timezone.make_aware(value)

    # Get the current time in UTC (aware)
    now = timezone.now()

    # Return the formatted time ago string
    return timeago.format(value, now)
