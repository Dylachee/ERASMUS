
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import News
from .forms import NewsForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login/')
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_news')
    else:
        form = NewsForm()

    return render(request, 'add_news.html', {'form': form})

def all_news(request):
    news_list = News.objects.order_by('-published_date')
    context = {'news_list': news_list}
    return render(request, 'allnews.html', context)

