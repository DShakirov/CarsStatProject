from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from carsstat.models import CarModel, Transmission, Generation, Gear, Engine, Region, Mark, Car, CarImageLinks, News

class CarModelView(ListView):

    model = Car
    template_name = 'carsstat/list.html'
    context_object_name = 'cars'
    paginate_by = 10
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counter'] = Car.objects.filter(car_model__pk=self.kwargs['pk']).count()
        context['title'] = CarModel.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        object_list = Car.objects.filter(car_model__pk=self.kwargs['pk'])
        return object_list

#класс для контекста на главной странице
class ViewMainPage(ListView):

    model = Car
    template_name = 'carsstat/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

    #Это заглушка, без кверисета класс не отработает
    def get_queryset(self):
        object_list = Car.objects.first()


#результаты поиска из формы
class GetSearchResults(ListView):

    model = Car
    template_name = 'carsstat/list.html'
    context_object_name = 'cars'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Car.objects.filter(
            Q(car_model__name__icontains=query) | Q(mark__name__icontains=query))
        return object_list


class GetNews(ListView):

    model = News
    template_name = 'carsstat/news.html'
    context_object_name = 'news'
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости автопортала'
        return context

    def get_queryset(self):
        return News.objects.all()


class GetCarsByGeneration(ListView):

    model = Car
    template_name = 'carsstat/list.html'
    context_object_name = 'cars'
    paginate_by = 10
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counter'] = Car.objects.filter(generation__pk=self.kwargs['pk']).count()
        context['title'] = Generation.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        object_list = Car.objects.filter(generation__pk=self.kwargs['pk'])
        return object_list


class GetCarsCheaperThanUsual(ListView):

    model = Car
    template_name = 'carsstat/list.html'
    context_object_name = 'cars'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        object_list = Car.objects.filter(low_price=True)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Автомобили дешевле рынка'
        return context


class GetCarsExpensiveThanUsual(ListView):

    model = Car
    template_name = 'carsstat/list.html'
    context_object_name = 'cars'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        object_list = Car.objects.filter(high_price=True)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Автомобили дороже рынка'
        return context


class GetMostExpensiveCars(ListView):

    model = Car
    template_name = 'carsstat/list.html'
    context_object_name = 'cars'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        object_list = Car.objects.order_by('-price')[:10]
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Самые дорогие автомобили'
        return context


class GetMostCheapCars(ListView):

    model = Car
    template_name = 'carsstat/list.html'
    context_object_name = 'cars'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        object_list = Car.objects.order_by('price')[:10]
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Самые дешевые автомобили'
        return context


class GetPopularCarModels(ListView):

    model = Generation
    template_name = 'carsstat/car_models.html'
    context_object_name = 'models'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        object_list = Generation.objects.raw(
            'SELECT gen.id, gen.name, COUNT(*) AS counter, model.name AS carmodel, model.id AS carmodel_id, mark.name AS markname FROM '
            'carsstat_car AS car JOIN carsstat_generation AS gen ON car.generation_id = gen.id JOIN carsstat_carmodel '
            'AS model ON car.car_model_id = model.id JOIN carsstat_mark AS mark ON car.mark_id=mark.id WHERE '
            'gen.name<>"n/a" GROUP BY gen.id ORDER BY COUNT(*) DESC'
                                    )
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Самые популярные модели'
        return context


class GetNewsSingle(DetailView):

    model = News
    template_name = 'carsstat/single_news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = News.objects.get(slug=self.kwargs['slug']).title
        return context


class GetCarSingle(DetailView):

    model = Car
    template_name = 'carsstat/single_car.html'
    context_object_name = 'car'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = Car.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'{car.mark} {car.car_model} {car.year} года'
        context['start_image'] = CarImageLinks.objects.filter(car__pk=self.kwargs['pk']).first()
        context['images'] = CarImageLinks.objects.filter(car__pk=self.kwargs['pk'])[1:]
        return context


class GetCarsByMark(ListView):

    model = Car
    template_name = 'carsstat/list.html'
    context_object_name = 'cars'
    paginate_by = 10
    allow_empty = True

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Car.objects.filter(mark__slug=self.kwargs['slug']).first().mark
        context['counter'] = Car.objects.filter(mark__slug=self.kwargs['slug']).count()
        return context

    def get_queryset(self):
        object_list = Car.objects.filter(mark__slug=self.kwargs['slug'])
        return object_list


#Статистика - сколько автомобилей каких марок, моделей и поколений продается и по какой цене
class GetCarsStats(ListView):

    model = Mark
    template_name = 'carsstat/stats.html'
    context_object_name = 'marks'
    paginate_by = 20
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статистика продаж автомобилей'
        return context
    def get_queryset(self):
        object_list = Mark.objects.raw(
            'SELECT mark.id, mark.name AS markname, model.id AS modelname_id,model.name AS modelname, gen.id AS gen_id, gen.name AS genname, gen.year_from AS year_from, gen.year_to AS year_to, COUNT(*) AS counter,SUM(car.price)/COUNT(*) AS avg_price FROM carsstat_car AS car JOIN carsstat_mark AS mark ON car.mark_id = mark.id JOIN carsstat_carmodel AS model ON car.car_model_id = model.id JOIN carsstat_generation AS gen ON car.generation_id = gen.id GROUP BY genname ORDER BY markname, modelname, year_to')
        return object_list

