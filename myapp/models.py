from django.db import models
import bcrypt
from django.dispatch import receiver
from django.db.models.signals import post_save
from .utils import resize_image
from django.utils.deconstruct import deconstructible
import os, uuid


@deconstructible
class UniqueImagePath:
    def __init__(self, subdir):
        self.subdir = subdir

    def __call__(self, instance, filename):
        # Генерация уникального имени файла, чтобы избежать дублирования
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        # Путь будет уникальным для каждого товара
        return os.path.join(self.subdir, unique_filename)


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/',default='profile_pictures/default.png', null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def set_password(self, raw_password):
        self.password_hash = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=50, default='active')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.name}'s cart"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

class PaymentCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=19)
    card_holder_name = models.CharField(max_length=100)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"Card of {self.card_holder_name}"


class ProductAvatar(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name='avatar')
    image = models.ImageField(upload_to=UniqueImagePath('product_avatars/'))

    def __str__(self):
        return f"Avatar for {self.product.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=UniqueImagePath('product_pictures/'), default='static/default.png')

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Получаем существующее изображение (если есть)
            existing_image = ProductImage.objects.get(pk=self.pk)

            # Если изображение изменилось, применяем resize
            if existing_image.image != self.image:
                if self.image:  # Если новое изображение задано
                    self.image = resize_image(self.image)
                else:
                    # Если изображение не задано, устанавливаем дефолтное изображение
                    self.image = 'static/default.png'
        else:
            # Если изображение новое (при создании записи), проверяем его
            if self.image:
                self.image = resize_image(self.image)
            else:
                # Если изображение не задано, устанавливаем дефолтное
                self.image = 'static/default.png'

        # Сохраняем модель
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name}"


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)