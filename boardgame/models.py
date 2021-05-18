from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=100) 
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=400)
    email = models.CharField(max_length=120)

    def __str__(self):
        return self.user_id

class Game(models.Model):
    name = models.CharField(max_length=200)
    l_participant = models.IntegerField()  # 최소 참가인원
    h_participant = models.IntegerField()  # 최대 참가인원
    age = models.IntegerField()  # 대상 연령(__세 이상)
    runtime = models.IntegerField()   # 게임 시간
    TYPE_LANGUAGE_CHOICES = (
        ('k', '한국어'),
        ('e', '영어'),
    )
    language = models.CharField(max_length=1, choices=TYPE_LANGUAGE_CHOICES)
    TYPE_GENRE_CHOICES = (
        (1, '전략게임'),
        (2, '테마게임'),
        (3, '가족게임'),
        (4, '어린이게임'),
        (5, '파티게임'),
        (6, '워게임'),
        (7, '기타'),
    )
    genre = models.IntegerField(choices=TYPE_GENRE_CHOICES)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Community(models.Model):
    writer_id = models.ForeignKey('Game', on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('r', '요청'),
        ('f', '자유'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    contents = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    writer_id = models.ForeignKey('Game', on_delete=models.CASCADE)
    community_id = models.ForeignKey('Community', on_delete=models.CASCADE)
    contents = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.contents