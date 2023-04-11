from django import template
from carsstat.models import Car

register = template.Library()

@register.inclusion_tag('carsstat/most_cheap_tpl.html')

def show_most_cheap(cnt=5):
    cars = Car.objects.order_by('price')[:cnt]
    return {'cars': cars }