from django import template

register = template.Library()


@register.simple_tag
def get_flr(data, name, y, x):
    for floor in data:
        if floor['name'] == str(name):
            for room in floor['rooms']:
                if room['y'] == y and room['x'] == x:
                    return room['flr']
    return None


@register.simple_tag
def get_rn(data, name, y, x):
    for floor in data:
        if floor['name'] == str(name):
            for room in floor['rooms']:
                if room['y'] == y and room['x'] == x:
                    return room['rn']
    return None
