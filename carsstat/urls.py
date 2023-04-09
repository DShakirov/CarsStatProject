from django.urls import path
from .views import *


urlpatterns = [
    path('', ViewMainPage.as_view(), name='main'),
    path('mark/<str:slug>', GetCarsByMark.as_view(), name= 'mark'),
    path('news/<str:slug>', GetNewsSingle.as_view(), name='news'),
    path('cars/<int:pk>', GetCarSingle.as_view(), name='car'),
    path('car_model/<int:pk>', CarModelView.as_view(), name='car_model'),
    path('search/', GetSearchResults.as_view(), name='search'),
    path('news/', GetNews.as_view(), name='news_list'),
    path('generation/<int:pk>', GetCarsByGeneration.as_view(), name='generation'),
    path('cheaper/', GetCarsCheaperThanUsual.as_view(), name='cheaper'),
    path('expensive/', GetCarsExpensiveThanUsual.as_view(), name='expensive'),
    path('most_expensive', GetMostExpensiveCars.as_view(), name='most_expensive'),
    path('most_cheap', GetMostCheapCars.as_view(), name='most_cheap'),
    path('most_popular', GetPopularCarModels.as_view(), name='most_popular'),
    path('stats', GetCarsStats.as_view(), name='stats'),
]
