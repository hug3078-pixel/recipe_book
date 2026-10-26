from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer, Recipe

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    phone_number = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User 
        fields = ('username', 'email', 'password', 'phone_number', 'address')
        

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number', '')
        address = validated_data.pop('address', '')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        Customer.objects.create(
            user=user,
            phone_number=phone_number,
            address=address
        )
        
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'image', 'first_name', 'last_name', 'description', 'phone_number', 'address')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer = getattr(instance, 'customer_profile', None)
        if customer:
            representation['phone_number'] = customer.phone_number
            representation['address'] = customer.address
            representation['description'] = customer.description
        else:
            representation['phone_number'] = ''
            representation['address'] = ''
            representation['description'] = ''
        return representation

    def update(self, instance, validated_data):

        phone_number = validated_data.pop('phone_number', None)
        address = validated_data.pop('address', None)
        description = validated_data.pop('description', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        customer, created = Customer.objects.get_or_create(user=instance)
        if phone_number is not None:
            customer.phone_number = phone_number
        if address is not None:
            customer.address = address
        if description is not None:
            customer.description = description
        customer.save()

        return instance

class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    instructions = serializers.CharField()
    example_image = serializers.ImageField(required=False, allow_null=True)
    cooking_time = serializers.IntegerField(required=False, allow_null=True, source='cokking_time') 
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    category = serializers.CharField(max_length=100, required=False, allow_blank=True)

    ingredients = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
        default=['no ingredients for this recipe'],
    )
    cost = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    tips = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
        default=['no tips for this recipe']
    )
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients', 'instructions', 'created_at', 'updated_at')