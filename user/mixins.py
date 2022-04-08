from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
# class LoginOnlyView(LoginRequiredMixin):
#     login_url =  reverse_lazy('user:signin')

class LogoutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        # 임시방편으로 mypage로 이동
        return redirect('user:mypage')