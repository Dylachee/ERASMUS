from django.urls import path
from .views import RegisterView, ActivationView , HomeView , custom_login , custom_logout


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    path('', HomeView.as_view(), name='home'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),

]
