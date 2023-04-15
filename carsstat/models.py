from datetime import datetime
from autoslug import AutoSlugField

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


#тип двигателя - бензин, дизель, гибрид, электрокар
class Engine(models.Model):

    type = models.CharField(max_length=50, unique=True,blank=False, verbose_name='Тип двигателя')
    slug = models.SlugField(max_length=50,unique=True, blank=False)

    def __str__(self):
        engines = {
            "GASOLINE": "Бензиновый",
            "DIESEL": "Дизельный",
            "HYBRID": "Гибридный",
            "ELECTRO": "Электродвигатель",
            "LPG": "СНГ, сжиженный нефтяной газ"
        }
        return engines[self.type]

    def get_absolute_url(self):
        return reverse('engine', kwargs={'slug':self.slug})

    class Meta:
        verbose_name = 'Двигатель'
        verbose_name_plural = 'Двигатели'


#марка автомобиля - Мерседес, Фольксваген и так далее
class Mark(models.Model):

    name = models.CharField(max_length=50, unique=True, blank=False, verbose_name='Марка автомобиля')
    slug = models.SlugField(max_length=50,unique=True, blank=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mark', kwargs={'slug':self.slug})

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'


#Поколение автомобиля. Не целочисленные значения, т.к. поколения могут называться 'B7', 'mk.8' итп.
class Generation(models.Model):

    name = models.CharField(max_length=100, blank=True, verbose_name='Поколение')
    year_from = models.CharField(max_length=10, verbose_name='Год начала выпуска', blank=True)
    year_to = models.CharField(max_length=10, verbose_name='Год окончания выпуска', blank=True)
    car_model = models.ForeignKey('CarModel', on_delete=models.PROTECT, related_name='generation', verbose_name='Модель')

    def __str__(self):
        return f'{self.car_model.name} {self.name}'

    def get_absolute_url(self):
        return reverse('generation', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Поколение'
        verbose_name_plural = 'Поколения'


#Модель автомобиля. С одной стороны связана с производителем, с другой - с поколением
class CarModel(models.Model):

    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, related_name='mark', default=None, verbose_name='Марка')
    name = models.CharField(max_length=150, blank=False, verbose_name='Модель')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('car_model', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


#Коробка передач - автомат, робот, механика
class Transmission(models.Model):

    type = models.CharField(max_length=50, unique=True, blank=False, verbose_name='Тип коробки передач')
    slug = models.SlugField(max_length=50, blank=False, unique=True)

    def __str__(self):
        transmissions = {
            "AUTOMATIC": "Автомат",
            "VARIATOR": "Вариатор",
            "ROBOT": "Роботизированная",
            "MECHANICAL": "Механическая"
        }
        return transmissions[self.type]

    def get_absolute_url(self):
        return reverse('transmission', kwargs={'slug':self.slug})

    class Meta:
        verbose_name = 'Коробка передач'
        verbose_name_plural = 'Коробки передач'


#привод автомобиля - передний, задний, полный
class Gear(models.Model):

    type = models.CharField(max_length=100, unique=True, blank=False, verbose_name='Тип привода')
    slug = models.SlugField(max_length=50, blank=False, unique=True)

    def __str__(self):
        gears = {
            "ALL_WHEEL_DRIVE": "Полный привод",
            "FORWARD_CONTROL": "Передний привод",
            "REAR_DRIVE": "Задний привод"
        }
        return gears[self.type]

    def get_absolute_url(self):
        return reverse('gear', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Привод'
        verbose_name_plural = 'Приводы'


#регион, в котором продается автомобиль
class Region(models.Model):

    name = models.CharField(max_length=150, unique=True, blank=False, verbose_name='Регион')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('region', kwargs={'pk':self.pk})

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


#основная модель - объявление о продаже автомобиля.
class Car(models.Model):
    sell_id = models.IntegerField(primary_key=True, verbose_name='Идентификатор объявления')#идентификатор объявления на авто.ру
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, related_name='car', verbose_name='Марка' )
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car', verbose_name='Модель')
    transmission = models.ForeignKey(Transmission, on_delete=models.PROTECT, related_name='car', verbose_name='Коробка передач')
    gear = models.ForeignKey(Gear, on_delete=models.PROTECT, related_name='car', verbose_name='Привод')
    engine_type = models.ForeignKey(Engine, on_delete=models.PROTECT, related_name='car', verbose_name='Двигатель')
    engine_power = models.IntegerField(verbose_name='Мощность двигателя, л.с.')
    engine_displacement = models.FloatField(verbose_name='Объем двигателя')#объем двигателя
    price = models.IntegerField(verbose_name='Цена')
    year = models.IntegerField(verbose_name='Год выпуска')
    low_price = models.BooleanField(verbose_name='Цена сильно ниже рыночной', default=False)
    high_price = models.BooleanField(verbose_name='Цена сильно выше рыночной', default=False)
    avg_price = models.IntegerField(verbose_name='Средняя цена)')#средняя цена автомобиля аналогичной модели, года выпуска, с аналогичным двигателем и коробкой
    owners_count = models.IntegerField(verbose_name='Количество владельцев')#количество владельцев
    pts_original = models.BooleanField(verbose_name='ПТС оригинал') #оригинальный птс или нет
    mileage = models.IntegerField(verbose_name='Пробег')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    link = models.CharField(max_length=150, verbose_name='Ссылка на объявление')
    describe = models.TextField(verbose_name='Описание от продавца')#что пищут при продаже машины. Что ремонтировали, что надо сделать, почему продают.
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='car', verbose_name='Регион')
    color = models.CharField(max_length=150, verbose_name='Цвет')
    generation = models.ForeignKey(Generation, on_delete=models.PROTECT,related_name='car', verbose_name='Поколение')

    def get_absolute_url(self):
        return reverse('car', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class CarImageLinks(models.Model):

    image_link = models.CharField(max_length=150, verbose_name='Ссылка на изображение')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image_link


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    slug = models.SlugField(max_length=150, unique=True)
    on_top = models.BooleanField(default=False, verbose_name='Закрепленная запись')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-on_top','-updated_at']
