from django import template

from carsstat.models import Mark

register = template.Library()

@register.inclusion_tag('carsstat/footer_tpl.html')

def show_footer():
    marks = Mark.objects.all()
    return {'marks': marks}