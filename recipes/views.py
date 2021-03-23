from urllib.parse import unquote

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.settings import ITEMS_FOR_PAGINATOR
from recipes.forms import RecipeForm
from recipes.models import Ingredient, Number, Recipe, Tag, User
from recipes.utils import add_subscription_status, extend_context, tag_filter


def index(request):
    tags = request.GET.getlist('tag')
    recipe_list = tag_filter(Recipe, tags)
    paginator = Paginator(recipe_list, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'tags': Tag.objects.all(),
        'page': page,
        'paginator': paginator
    }
    user = request.user
    if user.is_authenticated:
        context['active'] = 'recipe'
        extend_context(context, user)
    return render(request, 'index.html', context)


def profile(request, user_id):
    author = get_object_or_404(User, id=user_id)
    tags = request.GET.getlist('tag')
    recipe_list = tag_filter(Recipe, tags)
    paginator = Paginator(recipe_list.filter(author=author),
                          ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'tags': Tag.objects.all(),
        'author': author,
        'page': page,
        'paginator': paginator
    }
    user = request.user
    if user.is_authenticated:
        add_subscription_status(context, user, author)
        extend_context(context, user)
    return render(request, 'authorRecipe.html', context)


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = Ingredient.objects.filter(recipes=recipe)
    amounts = Number.objects.filter(recipe=recipe)
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'amounts': amounts,
    }
    user = request.user
    if user.is_authenticated:
        add_subscription_status(context, user, recipe.author)
        extend_context(context, user)
    return render(request, 'singlePage.html', context)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      initial={'author': request.user})
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'formRecipe.html', {'form': form})


@login_required()
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return redirect('recipe', id=recipe_id)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe, initial={'author': request.user})
    tags = recipe.tags.all()
    ingredients = Number.objects.filter(recipe=recipe)
    context = {'form': form,
               'is_created': True,
               'recipe_id': recipe.id,
               'tags': tags,
               'ingredients': ingredients}
    if form.is_valid():
        form.save()
        return redirect('recipe', recipe.id)
    return render(request, 'formRecipe.html', context)


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')


@login_required
def favorites(request):
    tags = request.GET.getlist('tag')
    user = request.user
    recipe_lists = user.favorite_recipes.all()
    if tags:
        recipe_list = recipe_lists.prefetch_related(
            'author', 'tags'
        ).filter(
            tags__slug__in=tags
        ).distinct()
    else:
        recipe_list = recipe_lists.prefetch_related(
            'author', 'tags'
        ).all()
    paginator = Paginator(recipe_list, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'tags': Tag.objects.all(),
        'page': page,
        'paginator': paginator
    }
    if user.is_authenticated:
        extend_context(context, user)
    return render(request, 'favourite.html', context)


@login_required
def follow(request):
    user = get_object_or_404(User, username=request.user)
    cards = user.followers.prefetch_related("author__recipes").order_by(
        "author__first_name"
    )
    paginator = Paginator(cards, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {'follow': follow,
                                             'page': page,
                                             'paginator': paginator})


@login_required
def purchases(request):
    user = request.user
    recipes = user.listed_recipes.all()
    return render(request, 'shopList.html', {'page': recipes})


@login_required
def purchases_download(request):
    recipes = Recipe.objects.filter(purchase__user=request.user)
    ing = {}
    for recipe in recipes:
        ingredients = recipe.ingredients.values_list('title', 'unit')
        numbers = recipe.numbers.values_list('amount', flat=True)

        for num in range(len(ingredients)):
            name = ingredients[num][0]
            unit = ingredients[num][1]
            amount = numbers[num]
            if name in ing:
                ing[name] = [ing[name][0] + amount, unit]
            else:
                ing[name] = [amount, unit]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shop_list.pdf"'
    p = canvas.Canvas(response)
    pdfmetrics.registerFont(TTFont('Marvin', 'Marvin.ttf'))
    p.setFont('Marvin', 16)
    a = [f'{str.title(k)} ({v[1]}) - {v[0]}' for k, v in ing.items()]
    p.drawString(200, 800, '')
    for i, item in enumerate(a):
        p.drawString(50, 700 + i*25, str(a[i]))
    p.showPage()
    p.save()
    return response


def get_ingredients(request):
    query = unquote(request.GET.get('query'))
    data = list(Ingredient.objects.filter(
        title__startswith=query
    ).values(
        'title', 'unit'))
    return JsonResponse(data, safe=False)
