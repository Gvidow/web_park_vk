from django import forms
from .models import Profile, User, Question
from django.db.models import ObjectDoesNotExist


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login"


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    upload_avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login"

    def clean_repeat_password(self):
        password = self.cleaned_data["password"]
        repeat_password = self.cleaned_data["repeat_password"]
        if password != repeat_password:
            raise forms.ValidationError("Passwords must match")
        return repeat_password

    def save(self):
        self.cleaned_data.pop("repeat_password")
        avatar = self.cleaned_data.pop("upload_avatar")
        user = User.objects.create_user(**self.cleaned_data)
        if avatar is None:
            Profile(user=user).save()
        else:
            Profile(user=user, avatar=avatar).save()


class ProfileEditForm(forms.ModelForm):
    upload_avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login"
        self.user_id = user_id

    def clean(self):
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = None
        if isinstance(user, User) and user.id != self.user_id:
            raise forms.ValidationError("A user with that username already exists.")
        return username

    def save(self):
        user = User.objects.get(id=self.user_id)
        if user.username != self.cleaned_data["username"] or \
                user.first_name != self.cleaned_data["first_name"] or \
                user.last_name != self.cleaned_data["last_name"] or \
                user.email != self.cleaned_data["email"]:
            user.username = self.cleaned_data["username"]
            user.first_name = self.cleaned_data["first_name"]
            user.last_name = self.cleaned_data["last_name"]
            user.email = self.cleaned_data["email"]
            user.save()
        profile = user.profile
        avatar = self.cleaned_data["upload_avatar"]
        if avatar is not None:
            if not avatar:
                avatar = Profile.avatar.field.default
            profile.avatar = avatar
            profile.save()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "text", "tags"]

