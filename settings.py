# Este é um exemplo parcial do seu settings.py
# Você precisará criar um projeto Django (django-admin startproject mutirao_project)
# e um app (python manage.py startapp core)

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',  # Adiciona o GeoDjango (PostGIS)
    'rest_framework',      # Adiciona o Django REST Framework
    'rest_framework_simplejwt', # Adiciona o JWT
    'core',                # Nosso app principal
]

# Configuração do Banco de Dados (PostGIS)
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'seu_banco_de_dados',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Configuração do Django REST Framework e JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# Configuração do Firebase (exemplo)
# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("path/to/your/firebase-service-account.json")
# firebase_admin.initialize_app(cred)