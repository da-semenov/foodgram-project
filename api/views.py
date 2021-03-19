from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import (FavoriteSerializer, FollowSerializer,
                             PurchaseSerializer)
from recipes.models import Favorite, Follow, Purchase, User


class CreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):
    """
    Класс родитель с переопределенным методом DELETE
    для Favorite, Follow и Purchase
    """

    api_name = ''

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user)
        if self.api_name == 'favorite':
            obj = user.favorites.filter(recipe__id=kwargs['id'])
        elif self.api_name == 'follow':
            obj = user.follower.filter(author__id=kwargs['id'])
        else:
            obj = user.purchases.filter(recipe__id=kwargs['id'])
        if obj.delete():
            return Response({'Success': True})
        return Response({'Success': False})


class FavoritesView(CreateDestroyView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    api_name = 'favorite'


class FollowView(CreateDestroyView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    api_name = 'follow'


class PurchaseView(CreateDestroyView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    api_name = 'purchase'
