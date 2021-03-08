from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.settings import ITEMS_FOR_PAGINATOR, TAGS
from recipes.forms import RecipeForm
from recipes.models import (Favorite, Follow, Ingredient, Number, Purchase,
                            Recipe, Tag, User)


def index(request):
    tags = request.GET.getlist('tag', TAGS)
    recipe_list = Recipe.objects.filter(
        tags__title__in=tags).select_related(
            'author').distinct()
    tags = Tag.objects.all()
    paginator = Paginator(recipe_list, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'indexAuth.html', {'recipe_list': recipe_list,
                           'tags': tags, 'page': page, 'paginator': paginator}
    )


def profile(request, username):
    tags = request.GET.getlist('tag', TAGS)
    recipe_list = Recipe.objects.filter(
        author__username=username,
        tags__title__in=tags).prefetch_related('tags').distinct()
    profile = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(author__username=username,
                                   user__username=request.user)
    tags = Tag.objects.all()
    paginator = Paginator(recipe_list, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'authorRecipe.html', {'recipe_list': recipe_list,
                              'profile': profile, 'tags': tags, 'page': page,
                              'paginator': paginator, 'follow': follow,
                              }
    )


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        ing = [v for k,
               v in request.POST.items()
               if k.startswith('nameIngredient_')]
        form = RecipeForm(request.POST, files=request.FILES or None)
        if len(ing) == 0:
            error = 'Нужно выбрать хотя бы один ингредиент'
            return render(request, 'formRecipe.html', {'form': form,
                          'error': error})

    if not form.is_valid():
        return render(request, 'formRecipe.html', {'form': form})
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    form.save_m2m()

    request_dict = request.POST
    numbers = [k[15:] for k, v in request_dict.items()
               if 'nameIngredient' in k]

    for number in numbers:
        name = 'nameIngredient_' + str(number)
        value = 'valueIngredient_' + str(number)

        ingredient = get_object_or_404(Ingredient, title=request_dict[name])
        number_create = Number.objects.create(
            recipe=recipe, ingredient=ingredient, amount=request_dict[value])
    return redirect('index')


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    author = recipe.author
    ingredients = Ingredient.objects.filter(recipes=recipe)
    favorite = Favorite.objects.filter(
        recipe=recipe, user__username=request.user).exists()
    follow = Follow.objects.filter(
        author__username=username, user__username=request.user)
    amounts = Number.objects.filter(recipe=recipe)
    purchase = Purchase.objects.filter(recipe=recipe,
                                       user__username=request.user)
    tags = Tag.objects.filter(recipe=recipe)
    return render(request, 'singlePage.html', {'recipe': recipe,
                                               'author': author,
                                               'ingredients': ingredients,
                                               'favorite': favorite,
                                               'follow': follow,
                                               'amounts': amounts,
                                               'tags': tags,
                                               'purchase': purchase})


@login_required()
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    amounts = Number.objects.filter(recipe=recipe)
    if request.user != recipe.author:
        return redirect(reverse('recipe', args=(username, recipe_id)))
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe)
    if not form.is_valid():
        return render(request, 'formChangeRecipe.html', {'recipe': recipe,
                                                         'form': form,
                                                         'amounts': amounts})
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    form.save_m2m()

    request_dict = request.POST
    numbers = [k[15:] for k, v in request_dict.items() if (
        'nameIngredient' in k and v != '')
    ]

    for number in numbers:
        name = 'nameIngredient_' + str(number)
        value = 'valueIngredient_' + str(number)
        ingredient = get_object_or_404(Ingredient, title=request_dict[name])
        number_create = Number.objects.create(
            recipe=recipe, ingredient=ingredient, amount=request_dict[value])
    return redirect(reverse('recipe', args=(username, recipe_id)))


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.author:
        return redirect('index')
    recipe.delete()
    return redirect('index')


def favorites(request):
    tags = request.GET.getlist('tag', TAGS)
    favorite = Favorite.objects.filter(
        user__username=request.user,
        recipe__tags__title__in=tags).select_related('recipe').distinct()
    tags = Tag.objects.all()
    paginator = Paginator(favorite, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favourite.html', {'favorite': favorite,
                                              'tags': tags,
                                              'page': page,
                                              'paginator': paginator})


@login_required
def follow(request):
    follow = User.objects.filter(
        following__user=request.user).\
        prefetch_related('authors').order_by('id')
    paginator = Paginator(follow, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {'follow': follow,
                                             'page': page,
                                             'paginator': paginator})


@login_required
def purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'shopList.html', {'purchases': purchases})


@login_required
def purchases_download(request):
    recipes = Recipe.objects.filter(purchase__user=request.user)
    ing = {}
    for recipe in recipes:
        ingredients = recipe.ingredient.values_list('title', 'dimension')
        numbers = recipe.numbers.values_list('amount', flat=True)

        for num in range(len(ingredients)):
            name = ingredients[num][0]
            unit = ingredients[num][1]
            amount = numbers[num]
            if name in ing:
                ing[name] = [ing[name][0] + amount, unit]
            else:
                ing[name] = [amount, unit]

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="shop_list.pdf"'
    p = canvas.Canvas(response)
    pdfmetrics.registerFont(TTFont('Marvin', 'Marvin.ttf'))
    p.setFont('Marvin', 16)
    a = [f'•  {str.title(k)} ({v[1]}) - {v[0]} ' for k, v in ing.items()]
    p.drawString(200, 800, '')
    for i, item in enumerate(a):
        p.drawString(50, 700 + i*25, str(a[i]))
    p.showPage()
    p.save()
    return response


def ingredients(request):
    title = request.GET.get('query')
    result = list(Ingredient.objects.filter(
        title__istartswith=title).values('title', 'dimension')
        )
    return JsonResponse(result, safe=False)
