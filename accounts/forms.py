from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
    )
    email = forms.EmailField(
        label=_("Email"),
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
    )

    def clean_username(self) -> str:
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        return username

    def clean_email(self) -> str:
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        return email

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match."))
        return password2

    def clean(self) -> dict:
        cleaned_data = super().clean()
        password = cleaned_data.get("password2")
        if password:
            unsaved_user = User(
                username=cleaned_data.get("username", ""),
                email=cleaned_data.get("email", ""),
            )
            try:
                validate_password(password, user=unsaved_user)
            except forms.ValidationError as exc:
                self.add_error("password2", exc)
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
    )
