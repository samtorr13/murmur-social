from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import ListView

from post.models import Post


@login_required(login_url='/login/')
def home(request):
    posts = Post.objects.all().order_by('-creat_date')  # ordenados por fecha
    return render(request, 'index.html', {'posts': posts})

class Login(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # o a donde quieras mandarlo
        return super().dispatch(request, *args, **kwargs)