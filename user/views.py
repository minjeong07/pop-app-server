from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic import FormView
from django.contrib import messages
from .mixins import LogoutOnlyView
from .forms import LoginForm, SignUpForm
from .models import User
import os
import requests
from django.contrib.auth import get_user_model
import re
from uuid import uuid4


# Create your views here.

def log_out(request):
    logout(request)
    return redirect(reverse('user:signin'))

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
        user.tag.clear()
        user.tag.add(*tags)
        user.save()
        return redirect('/mypage/')


    # true_user = auth.authenticate(request, username=username, password=password)
    # if true_user is not None:
    #     auth.login(request, true_user)
    #     return redirect('/main')
    # else:
    #     return render(request, 'user/edit_profile.html', {'error2': ' ID 또는 패스워드를 확인해주세요!'})


# def sign_in(request):
#     if request.method == 'GET':
#         return render(request, "user/signin.html", {})
#     username = request.POST.get('username','')
#     password = request.POST.get('password','')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect(reverse('user:mypage'))
#     else:
#         return render(request, "user/signin.html", {'msg':'아이디 혹은 비밀번호가 다릅니다.'})
#
# class LoginView(LogoutOnlyView, FormView):
#     form_class = LoginForm
#     success_url = reverse_lazy("user:mypage")
#     template_name = "user/signin.html"
#
#     def form_valid(self, form):
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(self.request, username=username, password=password)
#         if user is not None:
#             messages.success(self.request, f'어서오세요 {username}님 !')
#             login(self.request, user)
#             if user.tag.names():
#                 self.success_url = "/"
#         return super().form_valid(form)
#
#
#
# class SignUpView(LogoutOnlyView, FormView):
#     form_class = SignUpForm
#     success_url = reverse_lazy("user:mypage")
#     template_name = "user/signup.html"
#
#     def form_valid(self, form):
#         form.save()
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(self.request, username=username, password=password)
#         if user is not None:
#             messages.success(self.request, f'환영합니다 {username}님 !')
#             login(self.request, user)
#         return super().form_valid(form)
#
#
# def is_id(request):
#     username = request.POST.get('username', '')
#     try:
#         User.objects.get(username=username)
#         return JsonResponse({'msg': '이미 사용중인 아이디 입니다.'})
#     except:
#         return JsonResponse({'msg': '사용하셔도 좋습니다.'})
#
#
# def is_email(request):
#     email = request.POST.get('email', '')
#     try:
#         User.objects.get(email=email)
#         return JsonResponse({'msg': '이미 사용중인 이메일 입니다.'})
#     except:
#         return JsonResponse({'msg': '사용하셔도 좋습니다.'})


# def sign_up(request):

#     if request.method == 'GET':
#         return render(request, "user/signup.html")
#     username = request.POST.get('username','')
#     email = request.POST.get('email','')
#     password1 = request.POST.get('password1','')
#     password2 = request.POST.get('password2','')
#     #비밀번호 일치하지 않으면 돌려보냄
#     if password1 != password2:
#         return JsonResponse({'msg':'비밀번호가 일치하지 않습니다.'})
#     try:

#         #아이디가 존재하는지 확인 후 오류가 난다면 없다는 뜻
#         user = User.objects.get(username=username)
#         #아이디 존재
#         if user:
#             return JsonResponse({'msg':'아이디가 이미 사용중입니다. 중복확인을 해주세요.'})

#     #새로운 아이디를 만드는 곳        
#     except User.DoesNotExist:
#         try:
#             #이메일도 primary 해야하기에 다시한번 확인
#             user = User.objects.get(email=email)
#             if user:
#                 return JsonResponse({'msg':'이메일이 이미 사용중입니다. 중복확인을 해주세요.'})
#         except User.DoesNotExist:
#                 user = User.objects.create_user(username=username,password=password1,email=email)
#                 login(request,user)
#                 return JsonResponse({'ok':'ok'})


# def to_kakao(request):
#     # REST_API_KEY = os.environ.get('REST_API_KEY')
#     REST_API_KEY = 'bfdd7a7b9b1f9f256c089fceafbe03a4'
#     # REDIRECT_URI = 'https://paperonpresent.com/kakao/callback'
#     REDIRECT_URI = 'http://127.0.0.1:8000/kakao/callback'
#     return redirect(
#         f'https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code')
#
#
# def from_kakao(request):
#     # REST_API_KEY = os.environ.get('REST_API_KEY')
#     REST_API_KEY = 'bfdd7a7b9b1f9f256c089fceafbe03a4'
#     # REDIRECT_URI = 'https://paperonpresent.com/kakao/callback'
#     REDIRECT_URI = 'http://127.0.0.1:8000/kakao/callback'
#     code = request.GET.get('code', 'None')
#     if code is None:
#         # 코드 발급 x
#         error = "카카오 로그인 실패. 다시 한 번 시도해 주세요."
#         return render(request, 'user/no_use/signin.html', {"kakao_error": error})
#
#     headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
#     get_token = requests.post(
#         f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}',
#         headers=headers)
#     get_token = get_token.json()
#     if get_token.get('error', None) is not None:
#         # 에러발생
#         error = "카카오 로그인 실패. 다시 한 번 시도해 주세요."
#         return render(request, 'user/no_use/signin.html', {"kakao_error":error})
#     token = get_token.get('access_token', None)
#
#     headers = {'Authorization': f'Bearer {token}'}
#     get_info = requests.post(f'https://kapi.kakao.com/v2/user/me', headers=headers)
#     info = get_info.json()
#     properties = info.get('properties')
#     username = properties.get('nickname', None)
#     kakao_account = info.get('kakao_account')
#     profile_img = properties.get('profile_image', None)
#     email = kakao_account.get('email', None)
#     if email is None:
#         error = "이메일은 필수 동의 사항입니다."
#         return render(request, 'user/no_use/signin.html', {"kakao_error":error})
#     try:
#         user = User.objects.filter(email=email)
#         if user.login_method != User.LOGIN_KAKAO:
#             error = '이미 사용 중인 이메일 입니다.'
#             return render(request, 'user/no_use/signin.html', {"kakao_error":error})
#     except:
#         user = User.objects.create(username=username, profile_img=profile_img, email=email, login_method=User.LOGIN_KAKAO)
#         user.set_unusable_password()
#         user.save()
#
#     login(request, user)
#     return redirect('/mypage')


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 로그인 여부
        if user: # 로그인한 상태여서 회원가입 페이지 띄어줄 필요 없음
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:   # 비밀번호 확인이 틀렸을 때
            return render(request, 'user/signup.html', {'error': '패스워드를 확인해 주세요'})
        else:
            id_regex = re.compile('^[a-zA-Z가-힣]+[0-9a-zA-Z가-힣]')
            id_validation = id_regex.search(username.replace(" ", ""))

            if username.strip() == '' or password.strip() == '' or password2.strip() == '':    # 아이디나 비밀번호 입력이 공란일 때
                return render(request, 'user/signup.html', {'error': '아이디/패스워드는 필수 입력사항 입니다'})
            elif bio.strip() == '':
                return render(request, 'user/signup.html', {'error': '소개글을 작성해 주세요'})
            elif id_validation is None:
                return render(request, 'user/signup.html', {'error': '아이디가 유효하지 않습니다'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:  # 아이디 중복 확인
                return render(request, 'user/signup.html', {'error': '사용중인 이름 입니다.'})
            else:   # 유저 생성
                User.objects.create_user(username=username, password=password,  bio=bio)
                return redirect('/sign-in/')


def sign_in_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:    # 로그인한 상태여서 로그인하는 화면 띄어줄 필요 없음음
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        if me is not None: # username이란 사용자의 정보가 비어있지 않다 (있다)
            auth.login(request, me) # 그 정보로 로그인
            return redirect('/')

        else:
            return render(request, 'user/signin.html', {'error': '아이디와 패스워드를 확인해 주세요.'})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/sign-in/')