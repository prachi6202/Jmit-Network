"""Posts URLs"""

# Django
from django.urls import path
from django.contrib.auth.decorators import login_required

# Views
from posts import views


urlpatterns = [
    path(
        route='',
        view=login_required(views.PostFeedView.as_view()),
        name='feed'
    ),

    path(
        route='posts/new/',
        view=views.CreatePostView.as_view(),
        name='create_post'
    ),
    path('posts/like',views.like_post,name='like_post'),
    path('posts/update/<uuid:pk>/',views.PostUpdateView.as_view(),name='update'),
    path('posts/delete/<uuid:pk>/',views.PostDeleteView.as_view(),name='delete')
]
