from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
#     path('validate-token/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    # path('wishlist/', UserWishlist.as_view(), name='user_wishlist'),
    # path('wishlist/add/', AddToWishlist.as_view(), name='add_to_wishlist'),
    # path('users/', UserList.as_view(), name='userList'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='userdetail'),
    # path('userprofile/', UserProfileList.as_view(), name='userprofileList'),
    # path('userprofile/<int:pk>/', UserProfileDetail.as_view(), name='userprofiledetail'),
    path('brands', BrandList.as_view(),name='brandlist'),
    path('brands/<int:pk>', BrandDetail.as_view(),name='branddetail'),
    path('category',CategoryList.as_view(),name='categorylist'),
    path('category/<int:pk>', CategoryDetail.as_view(), name='categorydetail'),
    path('products', ProductList.as_view(),name='productlist'),
    path('products/<int:pk>',ProductDetail.as_view(),name='productdetail'),
    # path('yearlyprod',YearlyProductsList.as_view(), name='yearlyprodlist'),
    # path('yearlyprod/<int:pk>', YearlyProductsDetail.as_view(),name='yearlyproddetail'),
    # path('areawiselist',AreaWiseList.as_view(), name='areawiselist'),
    # path('areawisedetail', AreaWiseDetail.as_view(), name='areawisedetail')
    path('products/<int:product_id>/like', like_product, name='like_product'),
] 
