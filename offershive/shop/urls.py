from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.HOME, name='home'),
    path('product/<slug:slug>',views.PRODUCT_DETAIL, name='product_detail'),
    path('404',views.NOT_FOUND404, name='not_found404'),      #404 page not found

    path('account/register',views.REGISTER, name='hendleregister'),             #account form detail url
    path('account/login',views.LOGIN, name='hendlelogin'),                      #login form detail url
    path('accounts/', include('django.contrib.auth.urls')),                     # login page url
    path('accounts/signin',views.SIGNIN, name='signin'),                        # registration page url
    path('accounts/profile',views.PROFILE, name='profile'),
    path('accounts/profile/update', views.PROFILE_UPDATE, name='profile_update'),

    path('my-order', views.MY_ORDER, name='my_order'),
    path('about-us', views.ABOUT_US, name='about_us'),
    path('contact-us', views.CONTACT_US, name='contact_us'),
    path('FAQs', views.FAQS, name='faqs'),
    path('shop', views.SHOP, name='shop'),
    path('shop/filter-data',views.filter_data,name="filter-data"),            # filter data category wise  - show column wise
    path('shop/filter-product',views.filter_product,name="filter-product"),   # 2 filter data category wise  - show row wise

    path('cart/add/<int:id>/',views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/',views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear',views.cart_clear, name='cart_clear'),
    path('cart/cart-detail',views.cart_detail, name='cart_detail'),        #cart page url

    path('checkout',views.CHECKOUT, name='checkout'),
    path('blog/', include('blog.urls')),          #blog app url
    path('track-order',views.TRACK_ORDER, name='track_order'),

] +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
