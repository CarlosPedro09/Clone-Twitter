from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Tweet, Comment
from users.models import User

@login_required
def home(request):
    # Criar tweet
    if request.method == "POST" and "content" in request.POST:
        content = request.POST.get("content", "").strip()
        if content:
            Tweet.objects.create(user=request.user, content=content)
            messages.success(request, "Seu tweet foi publicado com sucesso!")

    # Exibe todos os tweets
    tweets = Tweet.objects.all().order_by("-created_at")

    tweets_with_avatar = []
    for tweet in tweets:
        # Avatar do usuário, se existir
        avatar_url = tweet.user.avatar_url if hasattr(tweet.user, "avatar_url") else None

        # Verifica se o usuário logado segue o autor do tweet
        is_following = tweet.user in request.user.following.all() if hasattr(request.user, "following") else False

        # Comentários
        comments = tweet.comments.all().order_by("created_at")  # related_name="comments" no model Comment

        tweets_with_avatar.append({
            "tweet": tweet,
            "avatar_url": avatar_url,
            "is_following": is_following,
            "comments": comments
        })

    return render(request, "tweets/home.html", {"tweets": tweets_with_avatar})


@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"likes_count": tweet.likes.count()})
    
    return redirect(request.META.get('HTTP_REFERER', 'tweets:home'))


@login_required
def comment_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            comment = Comment.objects.create(tweet=tweet, user=request.user, content=content)
            
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "username": comment.user.username,
                    "content": comment.content,
                    "created_at": comment.created_at.strftime("%d/%m/%Y %H:%M"),
                })
            
            messages.success(request, "Comentário enviado com sucesso!")
            return redirect(request.META.get('HTTP_REFERER', 'tweets:home'))
    
    return redirect(request.META.get('HTTP_REFERER', 'tweets:home'))


@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.user == target_user:
        messages.error(request, "Você não pode seguir a si mesmo.")
        return redirect(request.META.get('HTTP_REFERER', 'tweets:home'))

    if hasattr(request.user, "following"):
        if request.user.following.filter(id=target_user.id).exists():
            request.user.following.remove(target_user)
        else:
            request.user.following.add(target_user)

    return redirect(request.META.get('HTTP_REFERER', 'tweets:home'))
