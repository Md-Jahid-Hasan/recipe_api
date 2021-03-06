from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_field = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(many=True,
                                                    queryset=Ingredient.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredient', 'tags', 'time_minutes',
                  'price', 'link')
        read_only = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Inherit all the functionality of RecipeSerializer and override some of it"""
    ingredient = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
