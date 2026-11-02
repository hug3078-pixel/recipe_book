from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, get_object_or_404 
from rest_framework import generics, status, permissions 
from rest_framework.authentication import SessionAuthentication, TokenAuthentication 
from rest_framework.response import Response
from .models import Recipe, Review  
from .serializers import ProfileSerializer, RegisterSerializer, RecipeSerializer, LogoutSerializer, ReviewSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


def recipe_list(request):
    recipes = Recipe.objects.all() 
    context = {'recipes': recipes}
    return render(request, 'recipe_book/recipe_list.html', context)


def recipe_detail(request, pk):
    single_recipe = get_object_or_404(Recipe, pk=pk) 
    context = {'recipe': single_recipe}
    return render(request, 'recipe_book/recipe_detail.html', context)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        user = serializer.save()
        return Response(
            {
                "message": f"Account created for {user.username} successfully.",
                "username": user.username,
                "email": user.email
            },
            status=status.HTTP_201_CREATED
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data["username"] = instance.username
        data["add_recipe_url"] = "/api/recipes/add/" 
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data["username"] = self.get_object().username
        response.data["add_recipe_url"] = "/api/recipes/add/"
        return response

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        
        if recipe.favorites.filter(id=user.id).exists():
            recipe.favorites.remove(user)
            message = "Recipe removed from favorites"
            is_favorite = False
        else:
            recipe.favorites.add(user)
            message = "Recipe added to favorites"
            is_favorite = True
            
        return Response(
            {"message": message, "is_favorite": is_favorite, "favorites_count": recipe.favorites.count()},
            status=status.HTTP_200_OK
        )

class ReviewCreateListAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        recipe_pk = self.kwargs.get('pk')
        return Review.objects.filter(recipe_id=recipe_pk)

    def perform_create(self, serializer):
        recipe_pk = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        serializer.save(author=self.request.user, recipe=recipe)


class ReviewDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]

    def get_object(self):
        obj = get_object_or_404(Review, pk=self.kwargs.get('pk'))
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and obj.author != self.request.user:
            self.permission_denied(self.request, message="You can only modify your own reviews.")
        return obj