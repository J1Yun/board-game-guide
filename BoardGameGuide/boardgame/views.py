from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse_lazy

# Create your views here.


def comment_write(request, details_pk):
    if request.method == 'POST':
        community = get_object_or_404(Community, pk=details_pk)
        contents =request.POST.get('contents')
        date = timezone.now()
        
        
        writer = User.objects.get(user_id = community.writer_id)
        

        if not contents:
            messages.info(request, 'You dont write anything ...')
            return redirect('/comu_list/' + str(community.id))
        
        Comment.objects.create(community=community, writer=writer, contents=contents, date=date)
        return redirect('/comu_list/' + str(community.id))


def comu_delete(request, community_id):
    community = get_object_or_404(Community, pk = community_id)

    userid = request.session.get('user')
    user = User.objects.get(pk = userid)

    if user != community.writer_id:
        messages.info(request, '삭제권한이 없습니다.')
        return redirect('/comu_list/' + str(community.id))
    else :
        community.delete()
        
    return redirect('comu_list')

def comu_update(request, community_id):
    community = get_object_or_404(Community, pk = community_id)

    userid = request.session.get('user')
    user = User.objects.get(pk = userid)

    if user != community.writer_id:
        messages.info(request, '수정권한이 없습니다.')
        return redirect('/comu_list/' + str(community.id))

    if request.method == "POST":
        community.title = request.POST['title']
        community.contents = request.POST['contents']
        community.date = timezone.datetime.now()
       
        community.save()
        return redirect('/comu_list/' + str(community.id))

    else:
        return render(request, 'comu_update.html', {'community' : community})



def comu_detail(request, community_id):
    try:
        details = get_object_or_404(Community, pk=community_id)
    except Community.DoesNotExist:
        raise Http404('해당 게시물을 찾을 수 없습니다.')
    
    return render(request, 'comu_detail.html', {'details':details})

def comu_write(request):
    

    return render(request, 'comu_write.html')

    
def create(request):
    if not request.session.get('user'):
        return redirect('login')

    
    community = Community()
    writer_id = request.session.get('user')
    user = User.objects.get(pk = writer_id)
    community.type = request.POST.get('type')
    community.title = request.POST.get('title',False)
    community.contents = request.POST.get('contents', False)
    community.date = timezone.datetime.now()
    community.writer_id = user
    community.save()
    return redirect('/comu_list/' + str(community.id))


def comu_list(request):
    lists = Community.objects.all().order_by('-date') 
    page_number = request.GET.get('page', '1')
    paginator = Paginator(lists, 8)
    page_obj = paginator.get_page(page_number)
    return render(request, 'comu_list.html', context = {'posts': page_obj})


def logout(request):
    
    if request.session.get('user'):
        del(request.session['user'])
        
    return redirect('main')
    
def signup_done(request):
    return render(request, 'signup_done.html')

def rank(request):
    popular = Game.objects.all().order_by('-likes')[:10]
    return render(request, 'rank.html', {'gameList' : popular})

def main(request):
    gameList = Game.objects.all()
    return render(request, 'main.html', {'gameList': gameList})

def search(request):
    if 'search_value' in request.POST:
        word = request.POST['search_value']
        gameList = Game.objects.all().filter(name__icontains=word).distinct()
    return render(request, 'search.html', {'word' : word, 'gameList': gameList})

def login(request):
    if request.method== 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user_id = request.POST.get('user_id', None)
        password = request.POST.get('password', None)
  
    res_data = {}
    if not (user_id and password):
        res_data['error'] = '모든 값을 입력해야 합니다.'
        return render(request, 'login.html', res_data)
        
    else:
        user = User.objects.get(user_id = user_id)
        if check_password(password, user.password):
            request.session['user'] = user.id
            return redirect('main')
        else:
            res_data['error'] = '비밀번호가 틀렸습니다.'
    
            return render(request, 'login.html', res_data)

    if user is not None:
        self.request.session['user_id'] = user_id
        login(self.request, user)
        remember_session = self.request.POST.get('remember_session', False)
        if remember_session:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    return redirect("main")

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        
            user_id = request.POST['user_id']
            nickname = request.POST['nickname']
            email = request.POST['email']
            name = request.POST['name']
            password = request.POST['password']
            re_password = request.POST['re-password']

            res_data = {} #응답 메시지를 담을 변수(딕셔너리)

            if not (user_id and password and re_password and nickname and email and name):
                res_data['error'] = '모든 값을 입력해야 합니다.'
                return render(request, 'signup.html', res_data)
            elif password != re_password:
                res_data['error'] = '비밀번호가 다릅니다'
                return render(request, 'signup.html', res_data)
            elif User.objects.filter(user_id = request.POST['user_id']).exists():
                res_data['error'] = '이미 존재하는 아이디입니다.'
                return render(request, 'signup.html', res_data)
            elif User.objects.filter(email = request.POST['email']).exists():
                res_data['error'] = '이미 존재하는 이메일입니다.'
                return render(request, 'signup.html', res_data)
            elif User.objects.filter(nickname = request.POST['nickname']).exists():
                res_data['error'] = '이미 존재하는 닉네임입니다.'
                return render(request, 'signup.html', res_data)
            else:
                user = User( # 모델에서 생성한 User 클래스를 가져와 객체 생성
                    user_id = user_id,
                    nickname = nickname,
                    email = email,
                    name = name,
                    password = make_password(password),
                )

                user.save() #데이터베이스에 저장
                return render(request, 'signup_done.html', {'message': '회원가입을 완료하였습니다.'})
        
        
def mypage(request):
    u_id = request.session.get('user')
    if u_id:
        userInfo = User.objects.get(pk=u_id)
        try:
            userPost = Community.objects.filter(writer_id=u_id)
        except Community.DoesNotExist:
            userPost = None
        try:
            userLike = Recommend.objects.select_related('game_id').filter(user_id=u_id)
        except Recommend.DoesNotExist:
            userLike = None
        try:
            userComment = Comment.objects.filter(writer=u_id)
        except Comment.DoesNotExist:
            userComment = None
        return render(request, 'mypage.html', { 'userInfo':userInfo, 'userLike':userLike, 'userPost':userPost, 'userComment':userComment})
    return render(request, 'mypage.html')

def game(request, game_id):
    try:
        games = get_object_or_404(Game, pk=game_id)
    except Community.DoesNotExist:
        raise Http404('해당 게임 페이지를 찾을 수 없습니다.')
    return render(request, 'game.html', {'game': games})

