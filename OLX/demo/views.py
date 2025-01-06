from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Product, Brand, Category, yearlyProducts, AreaWiseProduct, Wishlist
from .serializers import (
    UserSerializer,
    ProductSerializer,
    BrandSerializer,
    CategorySerializer,
    yearlyProductsSerializer,
    AreaWiseProductSerializer,
    WishlistSerializer,
    RegisterSerializer,
)
from django.contrib.auth.models import User
from rest_framework import filters

# Custom Token Obtain Pair View
class CustomTokenObtainPairView(TokenObtainPairView):
    pass  # Optionally customize response if needed

# Register View
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout View
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# User View
class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Brand Views
class BrandList(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# Category Views
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Product Views
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # filter_backends = [generics.filters.SearchFilter]
    search_fields = ['category']



class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Wishlist View
class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
            wishlist.products.add(product)
            return Response({'message': 'Product added to wishlist'})
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

    def delete(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist.products.remove(product)
            return Response({'message': 'Product removed from wishlist'})
        except (Product.DoesNotExist, Wishlist.DoesNotExist):
            return Response({'error': 'Product not found or not in wishlist'}, status=404)

# Like Product View
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Product  # Adjust the import as per your project structure

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if user in product.likes.all():
        product.likes.remove(user)  # Unlike the product
        product.like_count = product.likes.count()  # Update like count
        product.save()
        return JsonResponse({'message': 'Product unliked', 'likes': product.like_count})
    else:
        product.likes.add(user)  # Like the product
        product.like_count = product.likes.count()  # Update like count
        product.save()
        return JsonResponse({'message': 'Product liked', 'likes': product.like_count})
import logging
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Product

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        if user in product.likes.all():
            product.likes.remove(user)  # Unlike the product
            product.like_count = product.likes.count()  # Update like count
            product.save()
            return JsonResponse({'message': 'Product unliked', 'likes': product.like_count})
        else:
            product.likes.add(user)  # Like the product
            product.like_count = product.likes.count()  # Update like count
            product.save()
            return JsonResponse({'message': 'Product liked', 'likes': product.like_count})

    except Exception as e:
        logger.error(f"Error in liking/unliking product {product_id}: {str(e)}")
        return JsonResponse({'error': 'Something went wrong'}, status=500)
    
# def create_product(request):
#     if request.method == 'POST':
#         data = request.data
#         product = Product.objects.create(
#             name=data['name'],
#             description=data['description'],
#             brand=data['brand'],
#             category=Category.objects.get(id=data['category']),
#             product_pic=data['product_pic'],  # Saving image URL here
#         )
#         product.save()
#         return Response({"message": "Product created successfully"}, status=201)

@api_view(['POST'])
def add_product(request):
    if request.method == 'POST':
        data = request.data

        # Ensure you have the required fields
        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        brand = data.get('brand')
        product_pic = data.get('product_pic')

        # Validation or error handling for missing data
        if not name or not description or not category or not brand or not product_pic:
            return Response({'error': 'All fields are required!'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new product
        product = Product.objects.create(
            name=name,
            description=description,
            category_id=category,  # Assuming category is provided as ID
            brand=brand,
            product_pic=product_pic  # Storing the image URL
        )

        # Return a response with the created product
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

