from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .forms import OrderForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    return render(request, 'index.html')



def user_login(request):
    error_message = None
    if request.method == 'POST':
        # Получаем данные из полей name="username" и name="password"
        u = request.POST.get('username')
        p = request.POST.get('password')

        # Печатаем в консоль для отладки (увидишь в Logs на Render)
        print(f"--- Пытаемся войти: логин={u} ---")

        user = authenticate(request, username=u, password=p)

        if user is not None:
            login(request, user)
            print("--- Вход выполнен успешно! ---")
            return redirect('index')  # Убедись, что 'index' это имя главной страницы в urls.py
        else:
            print("--- Ошибка: Пользователь не найден или пароль неверен ---")
            error_message = "Неверный логин или пароль"

    return render(request, 'login.html', {'error': error_message})

def mechanic_dashboard(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'mechanic_dashboard.html', {'orders': orders})

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('mechanic_dashboard')

def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_accepted = True
    order.save()
    return redirect('mechanic_dashboard')

def check_status(request):
    order_id = request.session.get('last_order_id')
    if order_id:
        order = Order.objects.filter(id=order_id).first()
        if order and order.is_accepted:
            return JsonResponse({'is_accepted': True})
    return JsonResponse({'is_accepted': False})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})