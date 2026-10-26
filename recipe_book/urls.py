from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token  
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = 'recipe_book'

urlpatterns = [
    # Авторизация и профиль
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    path('login/', TokenObtainPairView.as_view(), name='login'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('create_recipes/', views.RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),

]