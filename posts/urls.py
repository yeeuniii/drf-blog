from django.urls import path

from posts import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostingsView.as_view(), name='postings'),
    # path('<int:pk>/', views.PostingView.as_view(), name='posting'),
    # path('<int:pk>/comment', views.CommentView.as_view(), name='comment'),
    # path('<int:pk>/like', views.LikeView.as_view(), name='like'),
]