from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all/', views.all_news, name='all_news'),
    path('add/', views.add_news, name='add_news'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


