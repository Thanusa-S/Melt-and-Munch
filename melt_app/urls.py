from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path("", home, name="home"),
    path("products/", product_list, name="products"),
   
    path( "products/<slug:slug>/",product_detail, name="product_detail", ),
 
    path("cart/", cart_view, name="cart"),
    path(
    "cart/add/<str:item_type>/<int:item_id>/",
    add_to_cart,
    name="add_to_cart"
),
    path("cart/update/<str:item_type>/<int:item_id>/",update_cart,name="update_cart"),
   
   
    path("checkout/", checkout, name="checkout"),
    path("register/", register, name="register"),
    path("login/", StoreLoginView.as_view(), name="login"),
    path("logout/", StoreLogoutView.as_view(), name="logout"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("my-orders/", my_orders, name="my_orders"),

    path("admin-login/", admin_login, name="admin_login"),
    path("admin-logout/", admin_logout, name="admin_logout"),
   # ADMIN DASHBOARD
   path("dashboard/", admin_dashboard, name="admin_dashboard"),

    # PRODUCTS
    path("dashboard/products/",dashboard_products, name="dashboard_products"),

    # ORDERS
    path( "dashboard/orders/",dashboard_orders,name="dashboard_orders"),

    path( "dashboard/orders/update/<int:pk>/",update_order_status,name="update_order_status"),

    # CUSTOMERS
    path(
        "dashboard/customers/",dashboard_customers,name="dashboard_customers"),

    # INVENTORY
    path(
        "dashboard/inventory/",dashboard_inventory, name="dashboard_inventory"),

    # MESSAGES
    path("dashboard/messages/",dashboard_messages, name="dashboard_messages" ),
   

    # Customer ice cream page
    path(
        'ice-creams/',ice_creams,  name='ice_creams' ),

    # Dashboard ice cream management
    path(
        'dashboard/icecreams/', dashboard_icecreams,name='dashboard_icecreams'),

    path(
        'dashboard/icecreams/add/',add_icecream, name='add_icecream'),

    path(
        'dashboard/icecreams/edit/<int:pk>/',edit_icecream,name='edit_icecream' ),

    path('dashboard/icecreams/delete/<int:pk>/',delete_icecream,name='delete_icecream'),

]

