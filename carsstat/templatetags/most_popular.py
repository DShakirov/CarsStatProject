from django import template
from carsstat.models import CarModel, Generation, Car

register = template.Library()

@register.inclusion_tag('carsstat/popular_tpl.html')

def most_popular(cnt=5):
    #сколько автомобилей какой марки, модели и поколения продается
    models = Generation.objects.raw(
            'SELECT gen.id, gen.name, COUNT(*) AS counter, model.name AS carmodel, model.id AS carmodel_id, mark.name AS markname FROM '
            'carsstat_car AS car JOIN carsstat_generation AS gen ON car.generation_id = gen.id JOIN carsstat_carmodel '
            'AS model ON car.car_model_id = model.id JOIN carsstat_mark AS mark ON car.mark_id=mark.id '
            'GROUP BY gen.id ORDER BY COUNT(*) DESC'
                                    )[:cnt]
    return {'models':models}


