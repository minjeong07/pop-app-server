from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import User
from uuid import uuid4


@login_required
def mypage(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "GET":
        tag_list = list(user.tag.names())
        return render(request, "user/edit_profile.html", {'tag_list': tag_list})
    if request.method == "POST":
        tags = []
        tagcount = int(request.POST.get('tag_count', '0'))
        for i in range(tagcount):
            tag = request.POST.get(f'taginput{i}', '')
            tag = tag[:-1][1:]
            tags.append(tag)
        if request.FILES:
            upload_file = request.FILES.get("profile_img")
            file_name = str(uuid4().hex)
            upload_file.name = file_name + '.' + upload_file.name.split('.')[-1]
            user.profile_img = upload_file
        user.bio = request.POST.get('bio', '')
        user.tag.clear()
        user.tag.add(*tags)
        user.save()
        return redirect('/mypage/')


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        bio = request.POST.get('bio', '')
        exist_user = get_user_model().objects.filter(username=username)
        if exist_user:  # 아이디 중복 확인
            return render(request, 'user/signup.html', {'error': '사용중인 이름 입니다.'})
        else:  # 유저 생성
            User.objects.create_user(username=username, password=password, bio=bio)
            return redirect('/sign-in/')


def sign_in_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:  # 로그인한 상태여서 로그인하는 화면 띄어줄 필요 없음음
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')

        else:
            return render(request, 'user/signin.html', {'error': '아이디와 패스워드를 확인해 주세요.'})


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/sign-in/')