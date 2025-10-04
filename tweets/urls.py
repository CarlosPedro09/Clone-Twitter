from django.urls import path
from . import views

app_name = 'tweets'

urlpatterns = [
    path('', views.home, name='home'),
    path('tweet/<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),
    path('tweet/<int:tweet_id>/comment/', views.comment_tweet, name='comment_tweet'),
    path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
]
