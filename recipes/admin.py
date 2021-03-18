from django.contrib import admin

from recipes.models import (Favorite, Follow, Ingredient, Number, Purchase,
                            Recipe, Tag)


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('pk', 'title', 'unit')
    search_fields = ('title',)
    list_filter = ('title',)


class NumberAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'amount')


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('id', 'recipe', 'user')
    list_filter = ('recipe', 'user',)


class PurchaseAdmin(admin.ModelAdmin):
    model = Purchase
    list_display = ('id', 'recipe', 'user')
    list_filter = ('recipe', 'user',)


class FollowAdmin(admin.ModelAdmin):
    model = Follow
    list_display = ('id', 'author', 'user')
    list_filter = ('author', 'user',)


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('title', 'slug')


class IngredientInline(admin.TabularInline):
    model = Number
    min_num = 1
    extra = 0
    verbose_name = 'Ингредиент'


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('pk', 'author', 'title', 'pub_date', 'count_favor')
    list_filter = ('author', 'title', 'tags')
    empty_value_display = '-пусто-'
    inlines = [IngredientInline, ]

    def count_favor(self, obj):
        result = Favorite.objects.filter(recipe=obj).count()
        return result

    count_favor.short_description = 'Количество добавлений в избранное'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Number, NumberAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Tag, TagAdmin)
