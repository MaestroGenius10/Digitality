from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, UserUpdateForm, AddPaymentCardForm, DeletePaymentCardForm, ProductForm, ChangePasswordForm
from .models import User, Product, PaymentCard, Category, CartItem, Cart, Order, OrderItem
from django.db.models import Q
from datetime import date
from django.contrib.auth import logout
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f" {error}")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    request.session['user_email'] = user.email
                    request.session['user_name'] = user.name
                    messages.success(request, 'Вы успешно вошли в систему.')
                    return redirect('catalog')  # Перенаправление на страницу профиля
                else:
                    messages.error(request, 'Неверный пароль.')
            except User.DoesNotExist:
                messages.error(request, 'Пользователь с такой почтой не существует.')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def catalog(request):
    query = Q()

    query &= Q(status='active')
    query &= ~Q(user_id=request.session.get('user_id'))

    good_name = request.GET.get('good_name')
    if good_name:
        query &= Q(name__icontains=good_name)

    category_name = request.GET.get('category_name')
    if category_name:
        query &= Q(category__name__icontains=category_name)

    price_range = request.GET.get('price_range')
    if price_range:
        if price_range == '0-250':
            query &= Q(price__gte=0) & Q(price__lte=250)
        elif price_range == '251-500':
            query &= Q(price__gte=251) & Q(price__lte=500)
        elif price_range == '501-1000':
            query &= Q(price__gte=501) & Q(price__lte=1000)
        elif price_range == '1001-2000':
            query &= Q(price__gte=1001) & Q(price__lte=2000)
        elif price_range == '2001+':
            query &= Q(price__gte=2001)

    goods = Product.objects.filter(query)
    categories = Category.objects.all()
    return render(request, 'catalog.html', {'goods': goods, 'categories': categories})

def update_personal_data(request):
    user_id = request.session.get('user_id')

    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Личные данные успешно обновлены.')
            return redirect('view_personal_data')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'personal_data.html', {'form': form, 'user': user})

def add_payment_card(request):
    user_id = request.session.get('user_id')

    if request.method == 'POST':
        form = AddPaymentCardForm(request.POST)
        if form.is_valid():
            card = PaymentCard(
                user_id=user_id,
                card_number=form.cleaned_data['card_number'],
                card_holder_name=form.cleaned_data['card_holder_name'],
                expiration_date=form.cleaned_data['expiration_date'],
                cvv=form.cleaned_data['cvv']
            )
            card.save()
            messages.success(request, 'Карта успешно добавлена.')
            return redirect('view_user_cards')
        else:
            messages.error(request, 'Ошибка при добавлении карты.')
    else:
        form = AddPaymentCardForm()
    return render(request, 'payment_cards.html', {'form': form})

def delete_payment_card(request):
    user_id = request.session.get('user_id')

    if request.method == 'POST':
        form = DeletePaymentCardForm(request.POST, user=user_id)
        if form.is_valid():
            card = form.cleaned_data['card']
            card.delete()
            messages.success(request, 'Карта успешно удалена.')
            return redirect('view_user_cards')
        else:
            messages.error(request, 'Ошибка при удалении карты.')
            print(form.errors)
    else:
        form = DeletePaymentCardForm(user=user_id)
    return render(request, 'payment_cards.html', {'form': form})

def view_user_cards(request):
    user_id = request.session.get('user_id')

    user = get_object_or_404(User, id=user_id)
    cards = PaymentCard.objects.filter(user_id=user_id).values_list('card_number', flat=True)
    add_form = AddPaymentCardForm()
    delete_form = DeletePaymentCardForm(user=user_id)
    return render(request, 'payment_cards.html', {'cards': cards, 'form': add_form, 'delete_form': delete_form, 'user': user})

def my_goods(request):
    user_id = request.session.get('user_id')
    goods = Product.objects.filter(user_id=user_id)
    return render(request, 'my_products.html', {'goods': goods})

def add_good(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user_id = request.session.get('user_id')
            product.save()
            return redirect('my_goods')
    else:
        form = ProductForm()
    categories = Category.objects.all()
    return render(request, 'add_product.html', {'form': form, 'categories': categories})

def update_good(request, goods_id):
    user_id = request.session.get('user_id')
    product = get_object_or_404(Product, id=goods_id, user_id=user_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('my_goods')
    else:
        form = ProductForm(instance=product)
    categories = Category.objects.all()
    return render(request, 'update_product.html', {'form': form, 'categories': categories, 'good': product})

def delete_good(request, goods_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        product = get_object_or_404(Product, id=goods_id, user_id=user_id)
        product.delete()
        return redirect('my_goods')

def hide_good(request, goods_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        product = get_object_or_404(Product, id=goods_id, user_id=user_id)
        product.status = 'hidden'
        product.save()
        return redirect('my_goods')

def unhide_good(request, goods_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        product = get_object_or_404(Product, id=goods_id, user_id=user_id)
        product.status = 'active'
        product.save()
        return redirect('my_goods')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'good': product})

def change_password(request):
    user = User.objects.get(id=request.session.get('user_id'))
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            return redirect('view_personal_data')
    else:
        form = ChangePasswordForm(user)
    return render(request, 'security.html', {'form': form, 'user': user})

def add_to_cart(request, product_id):
    user_id = request.session.get('user_id')
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user_id=user_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

def view_cart(request):
    user_id = request.session.get('user_id')
    cart = get_object_or_404(Cart, user_id=user_id)
    items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total_price': total_price})

def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('view_cart')

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('view_cart')

def checkout(request):
    user_id = request.session.get('user_id')

    cart = get_object_or_404(Cart, user_id=user_id)
    items = CartItem.objects.filter(cart=cart)
    if not items.exists():
        messages.info(request, 'Ваша корзина пуста.')
        return redirect('view_cart')

    total_price = sum(item.product.price * item.quantity for item in items)
    order = Order.objects.create(user_id=user_id, total_price=total_price)

    for item in items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
    items.delete()
    return redirect('order_detail', order_id=order.id)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user_id=request.session.get('user_id'))
    items = OrderItem.objects.filter(order=order)
    user_cards = PaymentCard.objects.filter(user_id=request.session.get('user_id'))
    return render(request, 'order.html', {'order': order, 'items': items, 'user_cards': user_cards})

def pay_order(request):
    user_id = request.session.get('user_id')

    order_id = request.POST.get('order_id') if request.method == 'POST' else request.GET.get('order_id')
    if not order_id:
        messages.error(request, 'Не указан идентификатор заказа.')
        return redirect('view_personal_data')

    order = get_object_or_404(Order, id=order_id, user_id=user_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        card = get_object_or_404(PaymentCard, id=payment_method, user_id=user_id)
        if card.expiration_date < date.today():
            messages.error(request, 'Срок действия карты истек.')
            return redirect('order_detail', order_id=order.id)

        order.status = 'paid'
        order.save()
        messages.success(request, 'Заказ успешно оплачен.')
        return redirect('view_personal_data')

    return redirect('order_detail', order_id=order.id)

def purchases(request):
    user_id = request.session.get('user_id')

    orders = Order.objects.filter(user_id=user_id, status='paid')
    purchases = []
    for order in orders:
        items = OrderItem.objects.filter(order=order)
        for item in items:
            purchases.append({
                'name': item.product.name,
                'description': item.product.description,
                'price': item.price,
                'product_picture': item.product.product_picture.url if item.product.product_picture else '/media/product_pictures/default.png',
                'quantity': item.quantity
            })

    return render(request, 'purchases.html', {'purchases': purchases, 'user': get_object_or_404(User, id=user_id)})

def logout_view(request):
    logout(request)
    return redirect('login')