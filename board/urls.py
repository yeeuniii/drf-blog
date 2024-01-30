from django.urls import path

from board import views

app_name = 'board'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('<int:pk>/', views.PostView.as_view(), name='post'),
    path('<int:pk>/update', views.PostUpdateView.as_view(), name='post_update'),
    # path('<int:pk>/comment', views.CommentView.as_view(), name='comment'),
    # path('<int:pk>/like', views.LikeView.as_view(), name='like'),
]