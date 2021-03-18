from django.urls import path

from . import views

urlpatterns = [
    path('favorites/', views.FavoritesView.as_view(), name='favorites_add'),
    path('favorites/<int:id>/',
         views.FavoritesView.as_view(), name='favorites_delete'),
    path('subscriptions/', views.FollowView.as_view(), name='follow_add'),
    path('subscriptions/<str:id>/',
         views.FollowView.as_view(), name='follow_delete'),
    path('purchases/', views.PurchaseView.as_view(), name='purchases_add'),
    path('purchases/<int:id>/',
         views.PurchaseView.as_view(), name='purchases_delete'),
]
