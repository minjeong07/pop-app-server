from django import forms
from .models import User
from django.contrib.auth import password_validation



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "아이디"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 일치하지 않습니다."))

        except User.DoesNotExist:
            self.add_error("username", forms.ValidationError("아이디가 존재하지 않습니다."))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "아이디"}),
            "email": forms.EmailInput(attrs={"placeholder": "이메일"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"})
    )
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("이메일이 존재합니다.")
        except User.DoesNotExist:
            return email
    def clean_password1(self):
        pw1 = self.cleaned_data.get("password")
        pw2 = self.cleaned_data.get("password1")

        password_validation.validate_password(pw2, self.instance)

        if pw1 != pw2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

    def save(self):
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)
        user.set_password(password)
        user.save()
