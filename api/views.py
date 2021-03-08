from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import (FavoriteSerializer, FollowSerializer,
                             PurchaseSerializer)
from recipes.models import Favorite, Follow, Purchase, Recipe, User


@api_view(['POST'])
def api_favorites_add(request):
    serializer = FavoriteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user,
                        recipe=Recipe.objects.get(pk=request.data['id']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def api_favorites_delete(request, id):
    recipe = Recipe.objects.get(pk=id)
    favorite = get_object_or_404(Favorite, recipe=recipe, user=request.user)
    if request.user.is_authenticated:
        if favorite.user == request.user:
            favorite.delete()
            return Response('deleted')
        return Response('error', status=status.HTTP_403_FORBIDDEN)
    return Response('error', status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def api_follow_add(request):
    serializer = FollowSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            user=request.user, author=get_object_or_404(
                User, username=request.data['id']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def api_follow_delete(request, id):
    author = get_object_or_404(User, username=id)
    follow = get_object_or_404(Follow, author=author, user=request.user)
    if request.user.is_authenticated:
        if follow.user == request.user:
            follow.delete()
            return Response('deleted')
        return Response('error', status=status.HTTP_403_FORBIDDEN)
    return Response('error', status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def api_purchases_add(request):
    serializer = PurchaseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            user=request.user, recipe=Recipe.objects.get(
                pk=request.data['id']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def api_purchases_delete(request, id):
    recipe = Recipe.objects.get(pk=id)
    purchase = get_object_or_404(Purchase, recipe=recipe, user=request.user)
    if request.user.is_authenticated:
        if purchase.user == request.user:
            purchase.delete()
            return Response('deleted')
        return Response('error', status=status.HTTP_403_FORBIDDEN)
    return Response('error', status=status.HTTP_403_FORBIDDEN)
