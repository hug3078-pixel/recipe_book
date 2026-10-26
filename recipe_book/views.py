from django.shortcuts import render, get_object_or_404 
from rest_framework import generics, status, permissions 
from rest_framework.authentication import SessionAuthentication, TokenAuthentication 
from rest_framework.response import Response
from .models import Recipe  
from .serializers import ProfileSerializer, RegisterSerializer, RecipeSerializer


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
    authentication_classes = [SessionAuthentication, TokenAuthentication]

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
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]