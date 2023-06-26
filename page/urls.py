from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path('login',views.loginPage,name="login"),
    path('register',views.register,name="register"),
    path('logout',views.logoutUser,name='logout'),

    path('',views.home,name="index"),
    path('user',views.userPage,name='user'),
    path('account',views.accountSettings,name='account'),
    path('products',views.products,name="products"),
    path('customers/<str:pk_test>/',views.customers,name="customers"),
    path('createcustomer',views.createCustomer,name='create_customer'),
    path('createorder/<str:pk>/',views.createOrder,name='create_order'),
    path('updateorder/<str:pk>/',views.updateOrder,name='update_order'),
    path('deleteorder/<str:pk>/',views.deleteOrder,name='delete_order'),
    
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
         name="password_reset_done"),
    path('password_reset_<uidb64>_<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete")
]
