import os
from dotenv import load_dotenv
from datetime import timedelta

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

     # Configuración para JWT en Cookies
    JWT_TOKEN_LOCATION = ["cookies"]  # 🔥 Guardar el token en cookies en lugar de headers
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"  # Nombre de la cookie
    JWT_COOKIE_CSRF_PROTECT = False  # 🔥 Desactiva protección CSRF por ahora (puedes activarla luego)
    JWT_ACCESS_COOKIE_PATH = "/"  # La cookie será accesible en todas las rutas
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 🔥 Token de acceso expira en 1 hora
    JWT_REFRESH_COOKIE_NAME = "refresh_token_cookie"  # Nombre de la cookie de refresh token
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)  # 🔥 Refresh token expira en 7 días