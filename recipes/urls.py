from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:user_id>/', views.profile, name='profile'),
    path('recipes/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('new/', views.new_recipe, name='new'),
    path('recipes/<int:recipe_id>/edit/',
         views.recipe_edit, name='edit_recipe'),
    path('recipes/<int:recipe_id>/delete/',
         views.recipe_delete, name='delete_recipe'),
    path('favorites/', views.favorites, name='favorite'),
    path('followers/', views.follow, name='follows'),
    path('shop/', views.purchases, name='purchases'),
    path('shop/download/', views.purchases_download,
         name='download_purchases'),
    path('ingredients/', views.get_ingredients, name='ingredients'),
]
