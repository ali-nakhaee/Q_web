from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label=_("نام کاربری"),)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, label=_("رمز عبور"))


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("رمز عبور"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=_("رمز عبور نمی‌تواند مشابه دیگر اطلاعات کاربری شما باشد." '\n'
                    "رمز عبور باید حداقل ۸ کاراکتر داشته باشد." '\n'
                    "رمز عبور نمی‌تواند از رمزهای رایج باشد." '\n'
                    "رمز عبور نمی‌تواند تماما عدد باشد."),
    )
    password2 = forms.CharField(
        label=_("ورود مجدد رمز عبور"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("برای تایید رمز عبور مجددا آن را وارد کنید."),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')
        labels = {'username': 'نام کاربری', 'first_name': 'نام', 'last_name': 'نام خانوادگی'}