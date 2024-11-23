from django import template

register = template.Library()


@register.filter
def split(value, arg):
    return value.split(arg)


@register.filter
def zip1(list1, list2):
    return zip(list1, list2)
