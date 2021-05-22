# Generated by Django 3.2 on 2021-05-20 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('l_participant', models.IntegerField()),
                ('h_participant', models.IntegerField()),
                ('age', models.IntegerField()),
                ('runtime', models.IntegerField()),
                ('language', models.CharField(choices=[('k', '한국어'), ('e', '영어')], max_length=1)),
                ('genre', models.IntegerField(choices=[(1, '전략게임'), (2, '테마게임'), (3, '가족게임'), (4, '어린이게임'), (5, '파티게임'), (6, '워게임'), (7, '기타')])),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('nickname', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=400)),
                ('email', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('r', '요청'), ('f', '자유')], max_length=1)),
                ('title', models.CharField(max_length=200)),
                ('contents', models.TextField()),
                ('date', models.DateTimeField()),
                ('writer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardgame.game')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField()),
                ('date', models.DateTimeField()),
                ('community_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardgame.community')),
                ('writer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardgame.game')),
            ],
        ),
    ]