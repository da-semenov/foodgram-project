from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('<str:username>/<int:recipe_id>/edit/',
         views.recipe_edit, name='recipe_edit'),
    path('<str:username>/<int:recipe_id>/delete/',
         views.recipe_delete, name='recipe_delete'),
    path('favor/', views.favorites, name='favorites'),
    path('followers/', views.follow, name='followers'),
    path('shop/', views.purchases, name='my_purchases'),
    path('shop/download/', views.purchases_download, name='download'),
    path('ingredients/', views.ingredients),
]
