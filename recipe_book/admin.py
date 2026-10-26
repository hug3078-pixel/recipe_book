from django.contrib import admin
from .models import Customer, Recipe

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at')
    search_fields = ('user__username', 'phone_number')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at') 
    search_fields = ('name', 'description', 'ingredients')  
    list_filter = ('created_at',)