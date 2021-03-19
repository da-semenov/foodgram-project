from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель для хранения ингредиентов"""
    title = models.TextField(max_length=255,
                             verbose_name='Название ингредиента')
    unit = models.TextField(max_length=64,
                            verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.title} ({self.unit})'


class Tag(models.Model):
    """Модель тэгов"""
    title = models.CharField(max_length=20, verbose_name='Тэг')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.title}'


class Recipe(models.Model):
    """Модель для хранения рецептов"""
    title = models.CharField(max_length=255, verbose_name='Название рецепта',
                             blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    description = models.TextField(verbose_name='Описание рецепта',
                                   blank=True)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    image = models.ImageField(upload_to='recipes/', null=True, blank=True,
                              verbose_name='Изображение блюда')
    time = models.PositiveIntegerField(verbose_name='Время приготовления',
                                       validators=[MinValueValidator(1)])
    ingredients = models.ManyToManyField(Ingredient, through='Number',
                                         related_name='recipes', blank=True,
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, blank=True, related_name='recipes')
    favorite_by = models.ManyToManyField(User, through='Favorite',
                                         related_name='favorite_recipes',
                                         blank=True)
    purchase_by = models.ManyToManyField(User, through='Purchase',
                                         related_name='shop_list',
                                         blank=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.title}'


class Number(models.Model):
    """Модель связывающая ингредиенты с рецептом"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='numbers',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='numbers',
                                   verbose_name='Ингредиент')
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['ingredient', 'amount', 'recipe'],
            name='ingredient_unique')]
        verbose_name = 'Кол-во ингредиента в рецепте'
        verbose_name_plural = 'Кол-во ингредиентов в рецепте'

    def __str__(self):
        return f'{self.amount}'


class Favorite(models.Model):
    """Модель избранных рецептов"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='fans',
                               verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='favorite_unique')]
        ordering = ('-created',)
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class Purchase(models.Model):
    """Модель покупок"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='purchases')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='purchase_unique')]
        ordering = ('-created',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.recipe}'


class Follow(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='follow_unique')]
        ordering = ('-created',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.author}'
