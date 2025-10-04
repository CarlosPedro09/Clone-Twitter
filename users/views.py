from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

# -----------------------------
# Register
# -----------------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        avatar_file = request.FILES.get("avatar")  # captura avatar enviado

        # Valida se usuário ou email já existem
        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe!")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email já cadastrado!")
            return redirect("register")

        # Cria usuário
        user = User.objects.create_user(username=username, email=email, password=password)

        # Se enviou avatar, salva usando o método do model
        if avatar_file:
            user.set_avatar(avatar_file)

        user.save()
        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect("login")
    
    return render(request, "users/register.html")


# -----------------------------
# Login
# -----------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("tweets:home")
        else:
            messages.error(request, "Usuário ou senha incorretos!")
            return redirect("login")
    
    return render(request, "users/login.html")


# -----------------------------
# Logout
# -----------------------------
def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu da conta com sucesso.")
    return redirect("login")


# -----------------------------
# Profile
# -----------------------------
@login_required
def profile_view(request, username=None):
    """
    Mostra o perfil do usuário.
    Se username não for passado, mostra o perfil do usuário logado.
    Permite atualizar username, senha e avatar.
    """
    if username:
        profile_user = get_object_or_404(User, username=username)
        is_own_profile = profile_user == request.user
    else:
        profile_user = request.user
        is_own_profile = True

    # Atualização do perfil
    if request.method == "POST" and is_own_profile:
        new_username = request.POST.get("username").strip()
        new_password = request.POST.get("password").strip()
        avatar_file = request.FILES.get("avatar")

        # Atualiza username
        if new_username and new_username != profile_user.username:
            if User.objects.filter(username=new_username).exclude(pk=profile_user.pk).exists():
                messages.error(request, "Nome de usuário já está em uso.")
            else:
                profile_user.username = new_username

        # Atualiza senha
        if new_password:
            profile_user.set_password(new_password)
            update_session_auth_hash(request, profile_user)  # mantém login ativo

        # Atualiza avatar no Cloudinary
        if avatar_file:
            profile_user.set_avatar(avatar_file)  # ✅ usa o método do model

        profile_user.save()
        messages.success(request, "Perfil atualizado com sucesso.")
        return redirect("profile", username=profile_user.username)

    # Tweets do usuário
    tweets = profile_user.tweet_set.all().order_by("-created_at") if hasattr(profile_user, "tweet_set") else []

    # Contagem de seguidores e seguindo
    followers_count = User.objects.filter(following=profile_user).count()
    following_count = profile_user.following.count() if hasattr(profile_user, "following") else 0

    # Monta tweets com avatar
    tweets_with_comments = []
    for tweet in tweets:
        comments = tweet.comment_set.all().order_by("created_at") if hasattr(tweet, "comment_set") else []

        tweets_with_comments.append({
            "tweet": tweet,
            "comments": comments,
            "avatar_url": tweet.user.avatar,  # ✅ usa propriedade do model
            "is_following": request.user.following.filter(pk=tweet.user.pk).exists()
        })

    return render(request, "tweets/profile.html", {
        "profile_user": profile_user,
        "tweets": tweets_with_comments,
        "is_own_profile": is_own_profile,
        "followers_count": followers_count,
        "following_count": following_count
    })
