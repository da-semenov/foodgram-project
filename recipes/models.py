from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель для хранения ингредиентов"""
    title = models.TextField(max_length=255,
                             verbose_name='Название ингредиента')
    dimension = models.TextField(max_length=64,
                                 verbose_name='Единицы измерения')

    def __str__(self):
        return f'{self.title} ({self.dimension})'

    class Meta:
        verbose_name = "Ингредиент"


class Tag(models.Model):
    """Модель тэгов"""
    title = models.CharField(max_length=20, verbose_name='Тэг')
    color = models.CharField(max_length=20, verbose_name='Цвет')
    name = models.CharField(max_length=20, verbose_name='Имя тэга')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тэг"


class Recipe(models.Model):
    """Модель для хранения рецептов"""
    name = models.CharField(max_length=255, verbose_name='Название рецепта')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='authors',
                               verbose_name='Автор рецепта')
    description = models.TextField(verbose_name='Описание рецепта')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    image = models.ImageField(upload_to='recipes/', null=True, blank=True,
                              verbose_name='Изображение блюда')
    time = models.PositiveIntegerField(verbose_name='Время приготовления',
                                       validators=[MinValueValidator(1)])
    ingredient = models.ManyToManyField(Ingredient, through='Number',
                                        related_name='recipes',
                                        verbose_name='Ингредиенты',
                                        through_fields=('recipe',
                                                        'ingredient'))
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.name


class Number(models.Model):
    """Модель связывающая ингредиенты с рецептом"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='numbers',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='numbers',
                                   verbose_name='Ингредиент')
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = "Кол-во ингредиента в рецепте"


class Favorite(models.Model):
    """Модель избранных рецептов"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite',
                               verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='favorite_unique')]
        ordering = ('-created',)
        verbose_name = 'Избранные рецепты'


class Purchase(models.Model):
    """Модель покупок"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='purchase',
                               verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='owner',
                             verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='purchase_unique')]
        ordering = ('-created',)
        verbose_name = "Покупки"


class Follow(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follow",
                             verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='follow_unique')]
        ordering = ('-created',)
        verbose_name = 'Подписки'
