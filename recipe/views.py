from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from core.models import Tag, Ingredient, Recipe
from recipe import serializers
from django.db.models import Q
from rest_framework.response import Response


class IngTestBase(viewsets.GenericViewSet, mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        used = self.request.query_params.get('used')
        queryset = self.queryset
        print(used)
        if used == '1':
            queryset = queryset.filter(recipe__isnull=False)
        elif used == '0':
            queryset = queryset.filter(recipe__isnull=True)

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(IngTestBase):

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(IngTestBase):

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated,)

    def _params_to_int(self, qs):
        if qs is None:
            return
        return [str(ids) for ids in qs.split(',')]

    def get_queryset(self):
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        ingredient_ids = self._params_to_int(ingredients)
        tag_ids = self._params_to_int(tags)
        if tags and ingredients:
            queryset = queryset.filter(Q(tags__id__in=tag_ids) | Q(ingredient__id__in=ingredient_ids))
        if tags and ingredients is None:
            # tag_ids = self._params_to_int(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients and tags is None:
            # ingredient_ids = self._params_to_int(ingredients)
            queryset = queryset.filter(ingredient__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.error, status=status.HTTP_400_BAD_REQUEST
        )




