from itertools import product
import requests
from django.db.models import Avg
from django.shortcuts import render
from time import sleep
import datetime
from random import randint
from carsstat.models import *
from carsstatproject.celery import app


@app.task
def parse():
    print('Start!')
    # Список наиболее популярных марок автомобилей
    marks = [
        'Audi', 'BMW', 'Ford', 'Mazda', 'Kia', 'Hyundai', 'Volkswagen', 'Skoda', 'Toyota', 'Honda', 'Mitsubishi',
        'Chery', 'Chevrolet', 'Citroen', 'Geely', 'Haval', 'VAZ', 'Land_Rover', 'Nissan', 'Opel', 'Peugeot',
        'Renault', 'Porsche', 'Subaru', 'Suzuki', 'Volvo', 'UAZ', 'Mercedes'
    ]
    # Для каждой марки в Крыму не более 15 страниц поисковых запросов.
    for mark, page in product(marks, range(1, 20)):
        sleep(randint(1,10))
        URL = 'https://auto.ru/-/ajax/desktop/listing/'  # URL на который будет отправлен запрос
        # Параметры запроса
        PARAMS = {
            'catalog_filter': [{"mark": mark.upper()}],
            'section': "used",
            'region': "krym",
            'category': "cars",
            'sort': "fresh_relevance_1-desc",
            'page': page}
        # Заголовки страницы
        HEADERS = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Length': '137',
            'content-type': 'application/json',
            #рабочий куки
            'Cookie': '_csrf_token=1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24; autoru_sid=a%3Ag5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270%7C1580931467355.604800.8HnYnADZ6dSuzP1gctE0Fw.cd59AHgDSjoJxSYHCHfDUoj-f2orbR5pKj6U0ddu1G4; autoruuid=g5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270; suid=48a075680eac323f3f9ad5304157467a.bc50c5bde34519f174ccdba0bd791787; from_lifetime=1580933172327; from=yandex; X-Vertis-DC=myt; crookie=bp+bI7U7P7sm6q0mpUwAgWZrbzx3jePMKp8OPHqMwu9FdPseXCTs3bUqyAjp1fRRTDJ9Z5RZEdQLKToDLIpc7dWxb90=; gids=977; cmtchd=MTU4MDkzMTQ3MjU0NQ==; yandexuid=1758388111580931457; bltsr=1; navigation_promo_seen-recalls=true',
            #'Cookie':'_csrf_token=58b9bf17d302f4fbbf3287a2bf30dda4fe2fb72585b563f2; autoru_sid=a%3Ag5fcb8bc02sbhlh52qn9n4lu0pp9j5un.554b8700bc90755ef49149fec0c1286a%7C1607175104363.604800.f9IX1HCBLa9YqgknRnpRWg.JIZvbONlVKA_4r9c5mZnaTm-onpLMj1zz5lcbgVw2uQ; autoruuid=g5fcb8bc02sbhlh52qn9n4lu0pp9j5un.554b8700bc90755ef49149fec0c1286a; suid=afbc21b5f67f69334d1804ebb97ba74d.b539c93b813155527740bdb39af11ec6; from_lifetime=1607175327785; from=google-search; counter_ga_all7=1; yuidcs=1; X-Vertis-DC=myt; yuidlt=1; yandexuid=493122311571839213; my=YwA%3D; crookie=fjp0nU5rP3C5KUj8EbcOnpYc8V1fb2zvfGJu5b1Dt0lkSY6EG3ml6+uV6Tc2PpdLX0xQkhebFuoJCZedFlNlexUqHvc=; cmtchd=MTYwNzE3NTExMDUxNQ==; bltsr=1',
            'Referer': f'https://auto.ru/krym/cars/{mark.lower()}/used/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'x-client-app-version': '202002.03.092255',
            '#x-client-date': '1580933207763',
            #рабочий токен
            'x-csrf-token': '1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24',
            #'x-csrf-token': '58b9bf17d302f4fbbf3287a2bf30dda4fe2fb72585b563f2',
            'x-page-request-id': '60142cd4f0c0edf51f96fd0134c6f02a',
            'x-requested-with': 'fetch'
        }

        try:
            response = requests.post(URL, json=PARAMS, headers=HEADERS)  # Делаем post запрос на url

        except:
            continue

        data = response.json()['offers']

        i = 0  # Переменная для перехода по объявлениям
        for i in range(len(data)):  # len(data)-1 это количество пришедших объявлений
            sleep(1)
            # Цвет автомобиля (возвращается в формате hex) - Done
            try:
                color_hex = str(data[i]['color_hex'])
            except:
                color_hex = None

            # Описание автомобиля - Done
            try:
                description = str(data[i]['description'])
            except:
                description = ''

            # Количество владельцев автомобиля - Done
            try:
                owners_count = int(data[i]['documents']['owners_number'])
            except:
                owners_count = 0

            # PTS автомобиля - Done
            try:
                pts_original = bool(data[i]['documents']['pts_original'])
            except:
                pts_original = False

            # Год выпуска автомобиля - Done
            try:
                year = str(data[i]['documents']['year'])
            except:
                year = ''

            # Цена в рублях - Done
            try:
                price = int(data[i]['price_info']['RUR'])
            except:
                price = 0

            # Город, в котором находится автомобиль - Done
            try:
                region = str(data[i]['seller']['location']['region_info']['name'])
                r = Region.objects.filter(name=region)
                if not r.exists():
                    r = Region.objects.create(name=region)
                    r.save()
            except:
                region = ''
            print(region)

            # Пробег автомобиля - Done
            try:
                mileage = str(data[i]['state']['mileage'])
            except:
                mileage = None

            # Марка автомобиля - Done
            try:
                mark_info = str(data[i]['vehicle_info']['mark_info']['name'])
                mi = Mark.objects.filter(name=mark_info, slug=mark_info)
                if not mi.exists():
                    mi = Mark.objects.create(name=mark_info, slug=mark_info)
                    mi.save()
            except:
                continue

            # Год начала выпуска - Done
            try:
                year_from = str(data[i]['vehicle_info']['super_gen']['year_from'])
            except:
                year_from = ' '

            # Год конца выпуска - Done
            try:
                year_to = str(data[i]['vehicle_info']['super_gen']['year_to'])
            except:
                year_to = ' '

            # Модель автомобиля - Done
            # Попробуем записать модели автомобилей в ДБ
            try:
                model_info_en = str(data[i]['vehicle_info']['model_info']['code'])
                model_info_ru = str(data[i]['vehicle_info']['model_info']['name'])
                # в словарь передаем объекты классов Mark и Generation для создания связи через FK
                cm = CarModel.objects.filter(name=model_info_ru, mark=Mark.objects.get(name=mark_info, slug=mark_info))
                if not cm.exists():
                    cm = CarModel.objects.create(name=model_info_ru,
                                                 mark=Mark.objects.get(name=mark_info, slug=mark_info))
                    cm.save()
                print(mark, model_info_ru)
            except:
                print('Запись в файл не удалась', model_info_ru)

            # Поколение. Записываем в базу.
            try:
                gen = str(data[i]['vehicle_info']['super_gen']['name'])
            except:
                gen = str(model_info_ru)
            try:
                g = Generation.objects.filter(name=gen, car_model__name=model_info_ru)
                if not g.exists():
                    g = Generation.objects.create(
                        name=gen, year_to=year_to, year_from=year_from,
                        car_model=CarModel.objects.get(name=model_info_ru)
                    )
                    g.save()
            except:
                print('Запись поколения не удалась')
                continue

            # Привод автомобиля - Done
            try:
                gear_type = str(data[i]['vehicle_info']['tech_param']['gear_type'])
                gear = Gear.objects.filter(type=gear_type, slug=gear_type)
                if not gear.exists():
                    gear = Gear.objects.create(type=gear_type, slug=gear_type)
                    gear.save()
            except:
                continue

            # Двигатель автомобиля - Done
            try:
                engine_type = str(data[i]['vehicle_info']['tech_param']['engine_type'])
                engine = Engine.objects.filter(type=engine_type, slug=engine_type)
                if not engine.exists():
                    engine = Engine.objects.create(type=engine_type, slug=engine_type)
                    engine.save()
            except:
                continue

            # Объем двигателя - Done
            try:
                displacement = float(data[i]['vehicle_info']['tech_param']['displacement'])
            except:
                displacement = 0

            # Мощность двигателя, л.с. - Done
            try:
                power = int(data[i]['vehicle_info']['tech_param']['power'])
            except:
                power = 0

            # Коробка передач автомобиля - Done
            # Попробуем записать данные в ДБ
            try:
                transmission_type = str(data[i]['vehicle_info']['tech_param']['transmission'])
                t = Transmission.objects.filter(type=transmission_type, slug=transmission_type)
                if not t.exists():
                    t = Transmission.objects.create(type=transmission_type, slug=transmission_type)
                    t.save()
            except:
                continue

            # Информация об автомобиле - Done
            try:
                describe = str(data[i]['lk_summary'])
            except:
                describe = ''

            # Код  и объявления модели для продажи
            try:
                id_and_hash = str(data[i]['saleId'])
            except:
                model_short = ''

            # cсылка на объявление о продаже  - Переделать
            link = f'https://auto.ru/cars/used/sale/{mark.lower()}/{str(model_info_en.lower())}/{id_and_hash}'

            # средняя цена подобного автомобиля
            try:
                avg_price = Car.objects.filter(
                    generation__name=gen, car_model__name=model_info_ru).aggregate(Avg('price'))
                # Ответ возвращается в форме словаря, нам нужно вытянуть из него значение
                avg_price = int(list(avg_price.values())[0])
                if avg_price is None:
                    avg_price = price
            except:
                avg_price = price
            print(avg_price, price)

            # продается ли автомобиль сильно дешевле рынка
            try:
                if price <= 0.8 * avg_price:
                    low_price = True
                    high_price = False
                elif price >= 1.2 * avg_price:
                    high_price = True
                    low_price = False
                else:
                    high_price = False
                    low_price = False
            except:
                continue

            # для записи в модель, собираем данные в словарь
            try:
                car_description = {
                    'describe': describe, 'color': color_hex, 'region': Region.objects.get(name=region),
                    'link': link, 'mileage': mileage, 'pts_original': pts_original, 'owners_count': owners_count,
                    'price': price, 'avg_price': avg_price, 'low_price': low_price, 'year': year,
                    'engine_displacement': displacement, 'engine_power': power,
                    'engine_type': Engine.objects.get(type=engine_type),
                    'gear': Gear.objects.get(type=gear_type),
                    'transmission': Transmission.objects.get(type=transmission_type),
                    'car_model': CarModel.objects.get(name=model_info_ru),
                    'mark': Mark.objects.get(name=mark_info),
                    'generation': Generation.objects.get(name=gen, car_model__name=model_info_ru),
                    'high_price': high_price}
                print('Запись в базу успешна')
            except:
                print('Запись в базу не удалась')

            # идентификатор объявления на авто.ру - PK нашей модели
            sell_id = int(data[i]['id'])

            # Пробуем записать данные в БД
            try:
                car = Car.objects.update_or_create(sell_id=sell_id, defaults=car_description)
            except:
                continue
            # Картинки автомобиля
            # Возвращается несколько фото, мы их добавляем в модель image_link
            for img in data[i]['state']['image_urls']:
                CarImageLinks.objects.update_or_create(image_link=str(img['sizes']['1200x900']),
                                                       car=Car.objects.get(sell_id=sell_id))
            

        print(f'Mark:{mark}, Page: {str(page)}')  # Выводим сообщение, какая страница записалась
    print('Done')  # Выводим информацию об успешном выполнении

# удаляем устаревшие объявления
@app_task
def remove_depricated_cars():
    try:
        time_to_die = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)
        delete_list = Car.objects.filter(updated_at__lte=time_to_die)
        delete_list.delete()
        print('Устаревшие объявления удалены')
    except:
        pass
        print('Объявления не были удалены')
    
