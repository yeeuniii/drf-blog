from django.urls import path

from board import views

app_name = 'board'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('<int:post_id>/', views.PostView.as_view(), name='post'),
    # path('<int:comment_id>/comment', views.CommentView.as_view(), name='comment'),
    # path('<int:like_id>/like', views.LikeView.as_view(), name='like'),
]