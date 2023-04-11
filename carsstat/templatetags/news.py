from django import template
from carsstat.models import News

register = template.Library()

@register.inclusion_tag('carsstat/news_tpl.html')

def show_news(cnt=3):
    news = News.objects.all()[:cnt]
    return {'news': news}
