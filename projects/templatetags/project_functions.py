from django import template

register = template.Library()

@register.filter(name='format_relative_skills')
def format_relative_skills(skills):
    return_str = ""
    for item in skills:
        if item == "":
            pass
        else:
            return_str += str(item) + ", "
    return return_str[:-2]

@register.filter(name="format_leader")
def format_leader(leader):
    if leader is None:
        return False
    return True

@register.filter(name="format_members")
def format_members(members):
    members = members.all()
    if len(members) == 0:
        return False
    return True
    
@register.filter(name="format_difficulty")
def format_difficulty(difficulty):
    if difficulty == 1:
        return "Very Easy"
    if difficulty == 2:
        return "Easy"
    if difficulty == 3:
        return "Medium"
    if difficulty == 4:
        return "Hard"
    if difficulty == 5:
        return "Very Hard"
    return "Unkown Difficulty"

@register.filter(name="format_active")
def format_active(active):
    if active:
        return "checked"
    return ""