import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from client.forms import NewsletterForm, ServiceClientForm, MessageForm, NewsletterModeratorForm
from client.models import ServiceClient, Newsletter, Message


class HomeListView(ListView):
    model = Newsletter
    template_name = 'client/home_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['count_newsletter'] = len(Newsletter.objects.all())
        context_data['active_newsletter'] = len(Newsletter.objects.filter(status='started'))
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data['blog_list'] = blog_list[:3]
        context_data['service_client'] = len(ServiceClient.objects.all())
        return context_data


class ServiceClientListView(ListView):
    model = ServiceClient
    template_name = 'client/serviceclient_list.html'


class ServiceClientCreateView(LoginRequiredMixin, CreateView):
    model = ServiceClient
    form_class = ServiceClientForm
    success_url = reverse_lazy('client:home')

    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание клиента'
        return context

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ServiceClientDetailView(LoginRequiredMixin, DetailView):
    model = ServiceClient
    form_class = ServiceClientForm
    success_url = reverse_lazy('client:home')

    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подробности'
        return context


class ServiceClientUpdateView(LoginRequiredMixin, UpdateView):
    model = ServiceClient
    form_class = ServiceClientForm
    success_url = reverse_lazy('client:home')

    def get_success_url(self):
        from django.urls import reverse
        return reverse('client:view', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class ServiceClientDeleteView(LoginRequiredMixin, DeleteView):
    model = ServiceClient

    success_url = reverse_lazy('client:home')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class MessageListView(ListView):
    model = Message
    form_class = MessageForm
    template_name = 'client/message_list.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('client:message')

    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рассылок'
        return context

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подробности'
        return context


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('client:message')

    def get_success_url(self):
        from django.urls import reverse
        return reverse('client:view_message', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message

    success_url = reverse_lazy('client:message')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'client/newsletter_list.html'


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('client:newsletter')

    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рассылок'
        return context

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class NewsletterDetailView(DetailView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('client:newsletter')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подробности'
        return context


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('client:newsletter')

    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        from django.urls import reverse
        return reverse('client:view_newsletter', args=[self.kwargs.get('pk')])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object

    def test_func(self):
        user = self.request.user
        instance: Newsletter = self.get_object()
        custom_perms: tuple = (
            'client.set_is_activated',
        )

        if user == instance.owner:
            return True
        elif user.groups.filter(name='moderator') and user.has_perms(custom_perms):
            return True
        return self.handle_no_permission()


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('client:newsletter')

    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class NewsletterModeratorUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterModeratorForm
    success_url = reverse_lazy('client:newsletter')
    permission_required = 'client.set_is_activated'
