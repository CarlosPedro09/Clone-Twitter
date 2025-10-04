from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Tweet, Comment
from users.models import User
from django.conf import settings

@login_required
def home(request):
    # Criar tweet
    if request.method == "POST" and "content" in request.POST:
        content = request.POST.get("content").strip()
        if content:
            Tweet.objects.create(user=request.user, content=content)
            messages.success(request, "Seu tweet foi publicado com sucesso!")

    # Exibe todos os tweets
    tweets = Tweet.objects.all().order_by("-created_at")

    tweets_with_avatar = []
    for tweet in tweets:
        avatar_url = tweet.user.avatar.url if tweet.user.avatar else settings.STATIC_URL + "default-avatar.png"
        is_following = tweet.user in request.user.following.all()
        # Comentários usando related_name definido no model
        comments = tweet.comment_set.all().order_by("created_at")  # ou tweet.comments.all() se related_name="comments"

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
            
            # Se for AJAX, retorna JSON
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "username": comment.user.username,
                    "content": comment.content,
                    "created_at": comment.created_at.strftime("%d/%m/%Y %H:%M"),
                })
            
            # Se não for AJAX, adiciona mensagem
            messages.success(request, "Comentário enviado com sucesso!")
            return redirect(request.META.get('HTTP_REFERER', 'tweets:home'))
    
    return redirect(request.META.get('HTTP_REFERER', 'tweets:home'))


@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.user == target_user:
        messages.error(request, "Você não pode seguir a si mesmo.")
        return redirect(request.META.get('HTTP_REFERER', 'tweets:home'))

    if target_user in request.user.following.all():
        request.user.following.remove(target_user)
    else:
        request.user.following.add(target_user)

    return redirect(request.META.get('HTTP_REFERER', 'tweets:home'))
