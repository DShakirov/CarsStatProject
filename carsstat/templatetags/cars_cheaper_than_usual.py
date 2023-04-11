from django import template
from carsstat.models import Car
import random

register = template.Library()

@register.inclusion_tag('carsstat/cars_cheaper_tpl.html')

def cars_cheaper_than_usual(cnt=10):
    cars = Car.objects.filter(low_price=True)[:cnt]
    cars = random.sample(list(cars), cnt)
    return {'cars': cars }