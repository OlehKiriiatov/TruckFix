from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .forms import OrderForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def index(request):
    return render(request, 'index.html')


@login_required
def mech_call(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False) # Не сохраняем в базу сразу
            order.user = request.user       # Привязываем заказ к текущему юзеру (Олегу)
            order.save()                    # Теперь сохраняем окончательно
            return redirect('index')
    else:
        form = OrderForm()
    return render(request, 'MechCall.html', {'form': form})

    return render(request, 'MechCall.html', {'order': order})

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
            login(request, user) # Автоматический вход после регистрации
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})