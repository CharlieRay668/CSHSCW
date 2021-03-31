from django import template

register = template.Library()

@register.filter(name='format_ability')
def format_ability(ability):
    if ability == 0:
        return "just learning"
    if ability == 1:
        return "a begginer"
    if ability == 2:
        return "intermediate"
    if ability == 3:
        return "advanced"
    if ability == 4:
        return "very advanced"

@register.filter(name="format_skills")
def format_skills(skills):
    return_str = ""
    for skill in skills:
        return_str += skill.name +", "
    return return_str[:-2]