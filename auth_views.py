"""
Views de autenticação simplificadas para App Inventor
Retornam formato mais simples que não requer parse JSON complexo
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def simple_login(request):
    """
    Login simplificado para App Inventor
    Retorna apenas o token de acesso como string simples
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {"error": "Username e password são obrigatórios"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {"error": "Credenciais inválidas"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Gerar tokens JWT
    refresh = RefreshToken.for_user(user)
    
    # Retornar formato simplificado
    return Response({
        "token": str(refresh.access_token),  # Token de acesso
        "refresh": str(refresh),  # Token de refresh
        "username": user.username
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def simple_token_refresh(request):
    """
    Renovação de token simplificada
    """
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        return Response(
            {"error": "Token de refresh é obrigatório"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            "token": str(refresh.access_token)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": "Token inválido"},
            status=status.HTTP_401_UNAUTHORIZED
        )

