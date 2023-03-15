from django.contrib import admin
from django.urls import path
from prices_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('price/<str:name>/<int:nums>/', views.price),
]
