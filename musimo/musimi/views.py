from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.db import connection

from musimi.models import User, Offer, Instrument, Category, Brand, Order, Payment, Delivery, Review, Wishlist
from .forms import RegisterForm, OfferForm 

#Реєстрація та синхронізація
def sync_sequence():
    """Функція для синхронізації послідовності автоінкремента"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT setval(pg_get_serial_sequence('musimi_user', 'id'), 
            (SELECT MAX(id) FROM musimi_user));
        """)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()  
            sync_sequence()  
            messages.success(request, "Реєстрація успішна!")
            return redirect('login')
    else:
        form = RegisterForm()  
    return render(request, 'register.html', {'form': form}) 

# Логін користувача
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')  
        else:
            messages.error(request, 'Неправильний логін або пароль.')
    return render(request, 'musimi/login.html')

# Список користувачів
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

# Перегляд доступних оферів
def user_offers(request):
    offers = Offer.objects.filter(status='available').order_by('price')
    return render(request, 'offers.html', {'offers': offers})

# Головна сторінка
def homepage_view(request):
    if not request.user.is_authenticated:
        return redirect('register')  
    return render(request, 'homepage.html')  

# Деталі інструменту
def instrument_detail(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    context = {
        'instrument': instrument,
        'brand': instrument.brand,
        'category': instrument.category,
    }
    return render(request, 'musimi/instrument_detail.html', context)

# Деталі категорії
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    instruments = Instrument.objects.filter(category=category)
    instrument_id = request.GET.get('instrument_id')

    return render(request, 'musimi/category_detail.html', {
        'category': category,
        'instruments': instruments,
        'instrument_id': instrument_id,
    })

# Деталі бренду
def brand_detail(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    instruments = Instrument.objects.filter(brand=brand)
    instrument_id = request.GET.get('instrument_id')

    return render(request, 'musimi/brand_detail.html', {
        'brand': brand,
        'instruments': instruments,
        'instrument_id': instrument_id,
    })

# Замовлення користувача
def user_orders(request):
    orders = Order.objects.filter(Q(buyer=request.user) | Q(seller=request.user))
    return render(request, 'musimi/user_orders.html', {'orders': orders})

# Деталі замовлення
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'payment': Payment.objects.filter(order=order).first(),
        'delivery': Delivery.objects.filter(order=order).first(),
        'reviews': Review.objects.filter(order=order),
    }
    return render(request, 'musimi/order_detail.html', context)

# Деталі доставки
def delivery_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'musimi/delivery_detail.html', {
        'order': order,
        'instrument': order.offer.instrument,
    })

# Деталі відгуків
def review_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    reviews = Review.objects.filter(order=order)
    return render(request, 'musimi/review_detail.html', {'order': order, 'reviews': reviews})

# Деталі платежу
def payment_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    payment = Payment.objects.filter(order=order).first()
    return render(request, 'musimi/payment_detail.html', {'order': order, 'payment': payment})

# Вішліст користувача
def user_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

# Повідомлення користувача
def user_notifications(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('instrument')
    instrument_categories = wishlist_items.values_list('instrument__category', flat=True).distinct()
    recommended_instruments = Instrument.objects.filter(
        category__in=instrument_categories
    ).exclude(
        id__in=wishlist_items.values_list('instrument_id', flat=True)
    ).order_by('price')[:10]

    return render(request, 'notifications.html', {
        'recommended_instruments': recommended_instruments
    })

# Бронювання оферів
def book_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    if offer.status == 'available':
        offer.status = 'booked'
        offer.save()

        Order.objects.create(
            offer=offer,
            buyer=request.user,
            seller=offer.seller
        )
        return redirect('user_orders')  # Правильне перенаправлення
    else:
        return render(request, 'offer_detail.html', {
            'offer': offer,
            'message': 'Ця офера вже заброньована чи продана.'
        })
    
#Початкова сторінка
def base_view(request):
    return render(request, 'base_generic.html')

#Створити офер
def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)  
            offer.seller = request.user  
            offer.save()
            return redirect('offer_success')  
    else:
        form = OfferForm()
    return render(request, 'create_offer.html', {'form': form})

#Успішний офер
def offer_success(request):
    return render(request, 'offer_success.html')
