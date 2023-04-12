from django.shortcuts import render, redirect 
from django.views import View
from .forms import RegisterForm , CustomLoginForm
from django.contrib import messages
from .models import CustomUser
from django.urls import reverse
from .utils import send_activation_code , create_activation_code
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            create_activation_code(user)
            activation_link = request.build_absolute_uri(reverse('activate', args=[user.activation_code]))
            send_activation_code(user, activation_link)
            messages.success(request, 'Регистрация прошла успешно! Пожалуйста, проверьте свой почтовый ящик для активации аккаунта.')
            return render(request, 'registration_complete.html')
        return render(request, 'register.html', {'form': form})    
 
class ActivationView(View):
    def get(self, request, activation_code):
        try:
            user = CustomUser.objects.get(activation_code=activation_code)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Код активации неверен или устарел.')
            return redirect('home')
        else:
            user.is_active = True
            user.activation_code = ''
            user.save()
            messages.success(request, 'Поздравляем, ваш аккаунт был успешно активирован!')
            return redirect('home')
        
class HomeView(TemplateView):
    template_name = 'home.html'

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # замените `home` на имя вашего представления для домашней страницы
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')