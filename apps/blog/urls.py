from django.urls import path
from blog.views import (
    Home,
    PostsByCategory,
    GetPost,
    PostsByTag,
)

urlpatterns = [
    # path('', index, name='home'),
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag_posts'),
]
