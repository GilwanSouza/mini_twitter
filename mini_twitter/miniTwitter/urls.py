from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('tweet/new/', views.post_tweet, name='post'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('feed/', views.feed, name='feed'),
    
    path('tweet/<int:tweet_id>/curtir/', views.curtir_tweet, name='curtir_tweet'),
    path('tweet/<int:tweet_id>/editar/', views.editar_tweet, name='editar_tweet'),
    path('tweet/<int:tweet_id>/excluir/', views.excluir_tweet, name='excluir_tweet'),
    path('perfil/<str:username>/', views.perfil_usuario, name='perfil_usuario'),
    
    path('seguir/<str:username>/', views.seguir_usuario, name='seguir_usuario'),
    path('deixar_de_seguir/<str:username>/', views.deixar_de_seguir, name='deixar_de_seguir'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
