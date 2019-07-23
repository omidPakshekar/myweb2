from django.urls import path
from django.conf.urls import url
from . import views

app_name='images'
urlpatterns = [
	path('create/', views.image_create, name='create'),
    path('detail/<int:id>/<str:slug>/', views.image_detail, name='detail'),
	path('like/', views.image_like, name='like'),
	path('', views.image_list, name='list'),
	path('ranking/', views.image_ranking, name='create'),

]
