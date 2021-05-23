from django.db.models import Q
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('main')
    
def signup_done(request):
    return render(request, 'signup_done.html')

def rank(request):
    return render(request, 'rank.html')

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
    return render(request, 'mypage.html')

def game(request):
    return render(request, 'game.html')

