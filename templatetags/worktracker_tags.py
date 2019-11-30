from django import template

register = template.Library()

@register.filter(name='hhmm')
def hhmm(duration):
    total_secs = int(duration.total_seconds())
    mins, secs = divmod(total_secs, 60)
    hours, mins = divmod(mins, 60)
    return '{hours:02d}:{mins:02d}'.format(**locals())
