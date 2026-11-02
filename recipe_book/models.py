from django.conf import settings
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False, verbose_name="Verified / Checkbox")

    def __str__(self):
        return self.user.get_username()


class Recipe(models.Model):
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='favorite_recipes', 
        blank=True
    )
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0.0

    @property
    def reviews_count(self):
        return self.reviews.count()

    class CategoryChoices(models.TextChoices):
        BREAKFAST = 'breakfast', 'breakfast'
        LUNCH = 'lunch', 'lunch'
        DINNER = 'dinner', 'dinner'
        DESSERT = 'dessert', 'dessert'
        SNACK = 'snack', 'snack'

    class IngredientChoices(models.TextChoices):
        FLOUR = 'flour', 'Flour'
        SUGAR = 'sugar', 'Sugar'
        EGGS = 'eggs', 'Eggs'
        MILK = 'milk', 'Milk'
        BUTTER = 'butter', 'Butter'
        SALT = 'salt', 'Salt'
        BAKING_POWDER = 'baking_powder', 'Baking Powder'
        VANILLA_EXTRACT = 'vanilla_extract', 'Vanilla Extract'
        COCOA_POWDER = 'cocoa_powder', 'Cocoa Powder'
        CHOCOLATE_CHIPS = 'chocolate_chips', 'Chocolate Chips'
        Yeast = 'yeast', 'Yeast'
        WATER = 'water', 'Water'
        OIL = 'oil', 'Oil'
        HONEY = 'honey', 'Honey'
        NUTS = 'nuts', 'Nuts'
        FRUITS = 'fruits', 'Fruits'
        VEGETABLES = 'vegetables', 'Vegetables'
        CHEESE = 'cheese', 'Cheese'
        MEAT = 'meat', 'Meat'
        FISH = 'fish', 'Fish'

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ingredients = models.JSONField(default=list, blank=True)
    instructions = models.TextField()
    example_image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    cooking_time = models.IntegerField(blank=True, null=True) 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipes", blank=True, null=True)
    
    category = models.CharField(
        max_length=100, 
        choices=CategoryChoices.choices, 
        blank=True
    )
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tips = models.JSONField(default=list, blank=True)  
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Recipe"

class Review(models.Model):
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='Recipe'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='Author'
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name='Rating (from 1 to 5)'
    )
    text = models.TextField(verbose_name='Review Text')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = ('recipe', 'author')

    def __str__(self):
        return f'{self.author.username} -> {self.recipe.name} ({self.rating}/5)'