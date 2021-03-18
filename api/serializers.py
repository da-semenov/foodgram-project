from rest_framework import serializers

from recipes.models import Favorite, Follow, Purchase, Recipe, User


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source='recipe', slug_field='id', queryset=Recipe.objects.all()
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ['id', 'user']
        model = Favorite


class PurchaseSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source='recipe', slug_field='id', queryset=Recipe.objects.all()
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ['id', 'user']
        model = Purchase


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source='author', slug_field='id', queryset=User.objects.all()
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ['id', 'user']
        model = Follow

    def validate(self, attrs):
        if attrs['author'] == attrs['user']:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        return super().validate(attrs)
