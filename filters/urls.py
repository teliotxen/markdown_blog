from django.contrib import admin
from django.urls import path
from filters import views

urlpatterns = [
    path('page_detail/<int:pk>/',views.page_detail, name='page_detail'),
    path('mypage/',views.my_page, name='mypage'),
    path('input/',views.test_input, name='input'),
    path('update/', views.test_update, name='update'),

    path('', views.LandingPage.as_view(), name='landing_page'),

]
