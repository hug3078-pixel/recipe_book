from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = 'recipe_book'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', TokenObtainPairView.as_view(), name='login'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_recipe/', views.RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipe_detail/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('<int:pk>/favorite/', views.ToggleFavoriteView.as_view(), name='recipe-favorite'),
    

    path('create_reviews/<int:pk>/', views.ReviewCreateListAPIView.as_view(), name='recipe-reviews'),
    path('reviews/<int:pk>/', views.ReviewDetailAPIView.as_view(), name='review-detail'),
]