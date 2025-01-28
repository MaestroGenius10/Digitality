from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('catalog/', views.catalog, name='catalog'),
    path('profile/', views.update_personal_data, name='view_personal_data'),
    path('update_personal_data/', views.update_personal_data, name='update_personal_data'),
    path('add_payment_card/', views.add_payment_card, name='add_payment_card'),
    path('delete_payment_card/', views.delete_payment_card, name='delete_payment_card'),
    path('view_user_cards/', views.view_user_cards, name='view_user_cards'),
    path('my_goods/', views.my_goods, name='my_goods'),
    path('add_good/', views.add_good, name='add_good'),
    path('update_good/<int:goods_id>/', views.update_good, name='update_good'),
    path('delete_good/<int:goods_id>/', views.delete_good, name='delete_good'),
    path('hide_good/<int:goods_id>/', views.hide_good, name='hide_good'),
    path('unhide_good/<int:goods_id>/', views.unhide_good, name='unhide_good'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('pay_order/', views.pay_order, name='pay_order'),
    path('purchases/', views.purchases, name='purchases'),
    path('logout/', views.logout_view, name='logout_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)