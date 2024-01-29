from django.db import models

# Create your models here.


class Posting(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    nickname = models.CharField(max_length=50)
    date = models.DateTimeField()
    like_count = models.IntegerField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    posting_id = models.ForeignKey('Posting', on_delete=models.CASCADE)
    content = models.TextField()
    nickname = models.CharField(max_length=50)
    date = models.DateTimeField()


class Like(models.Model):
    posting_id = models.ForeignKey('Posting', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
