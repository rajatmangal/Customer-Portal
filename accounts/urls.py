from django.urls import path
from . import views
from django.http import HttpResponse


urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customers/<str:id>/', views.customers,name="customers")
]