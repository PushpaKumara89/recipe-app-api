""" Testing recipe api """
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def create_recipe(user, **params):
    """ Create a new recipe """
    default = {
        'title': 'Sample Test Recipe title',
        'time_minutes': 22,
        'price': Decimal(10.12),
        'description': 'Sample Test Recipe description',
        'link': 'https://www.example.com',
    }
    default.update(params)

    recipe = Recipe.objects.create(user=user, **default)
    return recipe


class PublicRecipeApiTests(TestCase):
    """ Testing public recipe api """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Testing auth required to access recipe api """
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """ Testing private recipe api """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrive_recipe(self):
        """ Test retrieving a recipe """
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipe = Recipe.objects.all().order_by('-id')
        serializers = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.status_code, status.HTTP_410_GONE)
        self.assertEqual(res.data, serializers)

    def test_recipe_list_limited_to_user(self):
        """ Test retrieving a recipe list """
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123'
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializers = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.data)
