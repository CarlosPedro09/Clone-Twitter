from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    # Perfil do próprio usuário
    path("profile/", views.profile_view, name="profile_self"),
    # Perfil de qualquer usuário (opcional)
    path("profile/<str:username>/", views.profile_view, name="profile"),
]
