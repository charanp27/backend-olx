from rest_framework import serializers
from .models import  Wishlist, Product, Brand, Category, yearlyProducts, AreaWiseProduct
from django.contrib.auth.models import User

# class RegistrationSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'password2')
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({'password': "Password fields didn't match."})

#         return attrs

#     def create(self, validated_data):
#         user = User(
#             username=validated_data['username'],
#             email=validated_data['email']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(style={'input_type': 'password'})
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['id', 'user', 'phone' , 'address']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'description'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description'
        ]

# class ProductSerializer(serializers.ModelSerializer):
#     brand = BrandSerializer(read_only=True)
#     category = CategorySerializer(read_only=True)
#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'name',
#             'description',
#             'price',
#             'brand',
#             'category',
#             'product_pic'
#         ]

from rest_framework import serializers
from .models import Product, Brand, Category

class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())  
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) 
    
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'brand',
            'category',
            'product_pic',
            'created_at'
        ]

class yearlyProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = yearlyProducts
        fields = [
            'id',
            'product',
            'year',
            'sales'
        ]

class AreaWiseProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = AreaWiseProduct
        fields = [
            'id',
            'product',
            'area',
            'quantity'
        ]

# class WishlistSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True, read_only=True) 

#     class Meta:
#         model = Wishlist
#         fields = ['products'] 

# class AddToWishlistSerializer(serializers.Serializer):
#     product_id = serializers.IntegerField()
class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True) 

    class Meta:
        model = Wishlist
        fields = ['id', 'products'] 

