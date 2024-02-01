from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    nickname = models.CharField(max_length=50)
    password = models.CharField(max_length=4)
    date = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    nickname = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="likes")
    nickname = models.CharField(max_length=50)
