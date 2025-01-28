from django.contrib import admin
from .models import User, Category, Product, Cart, CartItem, Order, OrderItem, PaymentCard

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentCard)