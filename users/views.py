import random
import string

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView

from users.forms import UserRegisterForm, UserProfileForm, RestoreUserForm, ModeratorForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        secrets_token = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        new_user.token = secrets_token
        message = f'Для подтверждения вашего Е-mail перейдите по ссылке http://127.0.0.1:8000/users/verify/?token={secrets_token}'
        send_mail(
            subject='Вы зарегистрированы на нашей платформе',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


def activate_user(request):
    key = request.GET.get('token')
    current_user = User.objects.filter(is_active=False)
    for user in current_user:
        if str(user.token) == str(key):
            user.is_active = True
            user.token = None
            user.save()
    response = redirect(reverse_lazy('users:login'))
    return response


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = ModeratorForm
    template_name = 'users/profile.html'
    permission_required = 'users.set_is_active'

    def get_object(self, queryset=None):
        return self.request.user


def generate_random_password():
    length = 10
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


class RestoreUser(FormView):
    template_name = 'users/new_password.html'
    form_class = RestoreUserForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        new_password = generate_random_password()
        user.password = make_password(new_password)
        user.save()
        send_mail(
            subject='Смена пароля',
            message=f'У Вашего аккаунта новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
        return super().form_valid(form)


@login_required
@permission_required(['users.view_user', 'users.set_is_active'])
def get_users_list(request):
    users_list = User.objects.all()
    context = {
        'object_list': users_list,
        'title': 'Список пользователей сервиса',
    }
    return render(request, 'users/users_list.html', context)
