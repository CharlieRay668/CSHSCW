from django import template

register = template.Library()

@register.filter(name='format_grade')
def format_grade(grade):
    if grade == 9:
        return "Freshman (9)"
    if grade == 10:
        return "Sophomore (10)"
    if grade == 11:
        return "Junior (11)"
    if grade == 12:
        return "Senior (12)"
