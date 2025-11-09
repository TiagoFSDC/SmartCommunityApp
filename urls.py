from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views as core_views

# Importação dos endpoints de autenticação JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Importação das views simplificadas para App Inventor
from core import auth_views

# O Router do DRF cria automaticamente as URLs para os ViewSets
router = DefaultRouter()
router.register(r'events', core_views.EventViewSet, basename='event')
router.register(r'registrations', core_views.RegistrationViewSet, basename='registration')
router.register(r'reports', core_views.EventReportViewSet, basename='report')

# URLs do Projeto
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Endpoints da API principal
    path('api/', include(router.urls)),
    
    # Endpoints de Autenticação JWT
    # O AppInventor fará um POST aqui com 'username' e 'password'
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # O AppInventor usará isso para renovar o token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Endpoints simplificados para App Inventor (formato mais fácil de processar)
    path('api/simple-login/', auth_views.simple_login, name='simple_login'),
    path('api/simple-refresh/', auth_views.simple_token_refresh, name='simple_refresh'),
]