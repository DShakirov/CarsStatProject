from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    # TODO: make webhook more secure
    path('super_secret_webhook/', csrf_exempt(views.TelegramBotWebhookView.as_view())),
]