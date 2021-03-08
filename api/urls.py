from django.urls import path

from . import views

urlpatterns = [
    path('favorites/', views.api_favorites_add, name="favorites_add"),
    path('favorites/<int:id>/',
         views.api_favorites_delete, name='favorites_delete'),
    path('subscriptions/', views.api_follow_add, name='follow_add'),
    path('subscriptions/<str:id>/',
         views.api_follow_delete, name='follow_delete'),
    path('purchases/', views.api_purchases_add, name='purchases_add'),
    path('purchases/<int:id>/',
         views.api_purchases_delete, name='purchases_delete'),
]
